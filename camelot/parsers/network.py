"""Implementation of network table parser."""

from __future__ import annotations

import copy
import math
from typing import Any

import numpy as np
from pdfminer.layout import LTTextLineHorizontal
from pdfminer.layout import LTTextLineVertical

from ..core import ALL_ALIGNMENTS
from ..core import HORIZONTAL_ALIGNMENTS
from ..core import VERTICAL_ALIGNMENTS
from ..core import TextAlignments
from ..utils import bbox_from_str
from ..utils import bbox_from_textlines
from ..utils import boundaries_to_split_lines
from ..utils import find_columns_boundaries
from ..utils import text_in_bbox
from ..utils import text_in_bbox_per_axis
from ..utils import textlines_overlapping_bbox
from .base import TextBaseParser


# maximum number of columns over which a header can spread
MAX_COL_SPREAD_IN_HEADER = 3

# Minimum number of textlines in a table
MINIMUM_TEXTLINES_IN_TABLE = 6


class TextLine:
    """A placeholder class to represent a text line with bounding box attributes.

    Attributes
    ----------
    x0 : float
        The x-coordinate of the left edge of the text line.
    x1 : float
        The x-coordinate of the right edge of the text line.
    y0 : float
        The y-coordinate of the bottom edge of the text line.
    y1 : float
        The y-coordinate of the top edge of the text line.
    """

    def __init__(self, x0: float, y0: float, x1: float, y1: float):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


def column_spread(left, right, col_anchors):
    """Get the number of columns crossed by a segment [left, right]."""
    index_left = 0
    while index_left < len(col_anchors) and col_anchors[index_left] < left:
        index_left += 1
    index_right = index_left
    while index_right < len(col_anchors) and col_anchors[index_right] < right:
        index_right += 1

    return index_right - index_left


def find_closest_tls(  # noqa: C901
    bbox: list[float], tls: list[LTTextLineHorizontal | LTTextLineVertical]
) -> dict[str, LTTextLineHorizontal | LTTextLineVertical | None]:
    """Search for textlines that are closest to the bounding box but outside in all four directions.

    Parameters
    ----------
    bbox : list of float
        A list containing the coordinates of the bounding box in the order
        [left, bottom, right, top].
    tls : list of TextLine
        A list of textline objects to search for the closest lines.

    Returns
    -------
    dict
        A dictionary with keys "left", "right", "top", and "bottom",
        each mapping to the closest textline object in that direction or None if not found.
    """
    left: LTTextLineHorizontal | LTTextLineVertical | None = None
    right: LTTextLineHorizontal | LTTextLineVertical | None = None
    top: LTTextLineHorizontal | LTTextLineVertical | None = None
    bottom: LTTextLineHorizontal | LTTextLineVertical | None = None

    (bbox_left, bbox_bottom, bbox_right, bbox_top) = bbox

    for textline in tls:
        if textline.x1 < bbox_left:
            # Left: check if it overlaps horizontally
            if textline.y0 > bbox_top or textline.y1 < bbox_bottom:
                continue
            if left is None or left.x1 < textline.x1:
                left = textline
        elif bbox_right < textline.x0:
            # Right: check if it overlaps horizontally
            if textline.y0 > bbox_top or textline.y1 < bbox_bottom:
                continue
            if right is None or right.x0 > textline.x0:
                right = textline
        else:
            # Either bottom or top: must overlap vertically
            if textline.x0 > bbox_right or textline.x1 < bbox_left:
                continue
            if textline.y1 < bbox_bottom:
                # Bottom
                if bottom is None or bottom.y1 < textline.y1:
                    bottom = textline
            elif bbox_top < textline.y0:
                # Top
                if top is None or top.y0 > textline.y0:
                    top = textline

    return {
        "left": left,
        "right": right,
        "top": top,
        "bottom": bottom,
    }


def search_header_from_body_bbox(body_bbox, textlines, col_anchors, max_v_gap):
    """Expand a bbox vertically up by looking for plausible headers.

    The core algorithm is based on fairly strict alignment of text. It works
    for the table body, but might fail on tables' headers since they tend to be
    in a different font, alignment (e.g. vertical), etc.
    This method evalutes the area above the table body's bbox for
    characteristics of a table header: close to the top of the body, with cells
    that fit within the horizontal bounds identified.
    """
    new_bbox = body_bbox
    (left, bottom, right, top) = body_bbox
    zones = []

    keep_searching = True
    while keep_searching:
        keep_searching = False
        # a/ first look for the closest text element above the bbox.
        # It will be the anchor for a possible new row.
        closest_above = None
        all_above = []
        for textline in textlines:
            # higher than the table, >50% within its bounds
            textline_center = 0.5 * (textline.x0 + textline.x1)
            if textline.y0 > top and left < textline_center < right:
                all_above.append(textline)
                if closest_above is None or closest_above.y0 > textline.y0:
                    closest_above = textline

        if closest_above and closest_above.y0 < top + max_v_gap:
            # b/ We have a candidate cell that is within the correct
            # vertical band, and directly above the table. Starting from
            # this anchor, we list all the textlines within the same row.
            tls_in_new_row = []
            top = closest_above.y1
            pushed_up = True
            while pushed_up:
                pushed_up = False
                # Iterate and extract elements that fit in the row
                # from our list
                for i in range(len(all_above) - 1, -1, -1):
                    textline = all_above[i]
                    if textline.y0 < top:
                        # The bottom of this element is within our row
                        # so we add it.
                        tls_in_new_row.append(textline)
                        all_above.pop(i)
                        if textline.y1 > top:
                            # If the top of this element raises our row's
                            # band, we'll need to keep on searching for
                            # overlapping items
                            top = textline.y1
                            pushed_up = True

            # Get the x-ranges for all the textlines, and merge the
            # x-ranges that overlap
            zones = zones + list(
                map(lambda textline: [textline.x0, textline.x1], tls_in_new_row)
            )
            zones.sort(key=lambda z: z[0])  # Sort by left coordinate
            # Starting from the right, if two zones overlap horizontally,
            # merge them
            merged_something = True
            while merged_something:
                merged_something = False
                for i in range(len(zones) - 1, 0, -1):
                    zone_right = zones[i]
                    zone_left = zones[i - 1]
                    if zone_left[1] >= zone_right[0]:
                        zone_left[1] = max(zone_right[1], zone_left[1])
                        zones.pop(i)
                        merged_something = True

            max_spread = max(
                list(
                    map(
                        lambda zone: column_spread(zone[0], zone[1], col_anchors), zones
                    )
                )
            )

            # Accept textlines that cross columns boundaries, as long as they
            # cross less than MAX_COL_SPREAD_IN_HEADER, and half the number of
            # columns.
            # This is to avoid picking unrelated paragraphs.
            if max_spread <= min(
                MAX_COL_SPREAD_IN_HEADER, math.ceil(len(col_anchors) / 2)
            ):
                # Combined, the elements we've identified don't cross more
                # than the authorized number of columns.
                # We're trying to avoid
                # 0: <BAD: Added header spans too broad>
                # 1: <A1>    <B1>    <C1>    <D1>    <E1>
                # 2: <A2>    <B2>    <C2>    <D2>    <E2>
                # if len(zones) > TEXTEDGE_REQUIRED_ELEMENTS:
                new_bbox = (left, bottom, right, top)

                # At this stage we've identified a plausible row (or the
                # beginning of one).
                keep_searching = True
    return new_bbox


class AlignmentCounter:
    """
    For a given textline, represent all other textlines aligned with it.

    A textline can be vertically aligned with others if their bbox match on
    left, right, or middle coord, and horizontally aligned if they match top,
    bottom, or center coord.

    """

    def __init__(self):
        self.alignment_to_occurrences = {}
        for alignment in ALL_ALIGNMENTS:
            self.alignment_to_occurrences[alignment] = []

    def __getitem__(self, key):
        """Get the value of a property to the given value."""
        return self.alignment_to_occurrences[key]

    def __setitem__(self, key, value):
        """Set the value of a property to the given value."""
        self.alignment_to_occurrences[key] = value
        return value

    def max_alignments(self, alignment_ids=None):
        """Get the alignment dimension with the max number of textlines."""
        alignment_ids = alignment_ids or self.alignment_to_occurrences.keys()
        alignment_items = map(
            lambda alignment_id: (
                alignment_id,
                self.alignment_to_occurrences[alignment_id],
            ),
            alignment_ids,
        )
        return max(alignment_items, key=lambda item: len(item[1]))

    def max_v(self):
        """Tuple (alignment_id, textlines) of largest vertical row."""
        # Note that the horizontal alignments (left, center, right) are aligned
        # vertically in a column, so max_v is calculated by looking at
        # horizontal alignments.
        return self.max_alignments(HORIZONTAL_ALIGNMENTS)

    def max_h(self):
        """Tuple (alignment_id, textlines) of largest horizontal col."""
        return self.max_alignments(VERTICAL_ALIGNMENTS)

    def max_v_count(self):
        """Maximum vertical count.

        Return the maximum number of alignments along
        one of the vertical axis (left/right/middle).
        """
        return len(self.max_v()[1])

    def max_h_count(self):
        """Maximum horizontal count.

        Return the maximum number of alignments along
        one of the horizontal axis (bottom/top/center).
        """
        return len(self.max_h()[1])

    def alignment_score(self):
        """Return the alignment score.

        We define the alignment score of a textline as the product of the
        number of aligned elements - 1. The -1 is to avoid favoring
        singletons on a long line.
        """
        return (self.max_v_count() - 1) * (self.max_h_count() - 1)


class TextNetworks(TextAlignments):
    """Text elements connected by vertical AND horizontal alignments.

    The alignment dict has six keys based on the hor/vert alignments,
    and each key's value is a list of camelot.core.TextAlignment objects.
    """

    def __init__(self):
        super().__init__(ALL_ALIGNMENTS)
        # For each textline, dictionary "alignment type" to
        # "number of textlines aligned"
        self._textline_to_alignments = {}

    def _update_alignment(self, alignment, coord, textline):
        alignment.register_aligned_textline(textline, coord)

    def _register_all_text_lines(self, textlines):
        """Add all textlines to our network repository to identify alignments."""
        # Identify all the alignments
        for textline in textlines:
            if len(textline.get_text().strip()) > 0:
                self._register_textline(textline)

    def _compute_alignment_counts(self):
        """Build a dictionary textline -> alignment object."""
        for align_id, textedges in self._text_alignments.items():
            for textedge in textedges:
                for textline in textedge.textlines:
                    alignments = self._textline_to_alignments.get(textline, None)
                    if alignments is None:
                        alignments = AlignmentCounter()
                        self._textline_to_alignments[textline] = alignments
                    alignments[align_id] = textedge.textlines

    def remove_unconnected_edges(self):
        """Remove elements which are only connected on one dimension.

        Elements should be connected to others both vertically
        and horizontally.
        """
        removed_singletons = True
        while removed_singletons:
            removed_singletons = False
            for text_alignments in self._text_alignments.values():
                # For each alignment edge, remove items if they are singletons
                # either horizontally or vertically
                for text_alignment in text_alignments:
                    for i in range(len(text_alignment.textlines) - 1, -1, -1):
                        textline = text_alignment.textlines[i]
                        alignments = self._textline_to_alignments[textline]
                        if (
                            alignments.max_h_count() <= 1
                            or alignments.max_v_count() <= 1
                        ):
                            del text_alignment.textlines[i]
                            removed_singletons = True
            self._textline_to_alignments = {}
            self._compute_alignment_counts()

    def most_connected_textline(self):
        """Retrieve the textline that is most connected."""
        # Find the textline with the highest alignment score, with a tie break
        # to prefer textlines further down in the table.  Starting the search
        # from the table's bottom allows the algo to collect data on more cells
        # before going to the header, typically harder to parse.
        return max(
            self._textline_to_alignments.keys(),
            key=lambda textline: (
                self._textline_to_alignments[textline].alignment_score(),
                -textline.y0,
                -textline.x0,
            ),
            default=None,
        )

    def compute_plausible_gaps(self):
        """Evaluate plausible gaps between cells.

        Both horizontally and vertically
        based on the textlines aligned with the most connected textline.

        Returns
        -------
        gaps_hv : tuple
            (horizontal_gap, horizontal_gap) in pdf coordinate space.

        """
        # Determine the textline that has the most combined
        # alignments across horizontal and vertical axis.
        # It will serve as a reference axis along which to collect the average
        # spacing between rows/cols.
        most_aligned_tl = self.most_connected_textline()
        if most_aligned_tl is None:
            return None

        # Retrieve the list of textlines it's aligned with, across both
        # axis
        best_alignment = self._textline_to_alignments[most_aligned_tl]
        __, ref_h_textlines = best_alignment.max_h()
        __, ref_v_textlines = best_alignment.max_v()
        if len(ref_v_textlines) <= 1 or len(ref_h_textlines) <= 1:
            return None

        h_textlines = sorted(
            ref_h_textlines, key=lambda textline: textline.x0, reverse=True
        )
        v_textlines = sorted(
            ref_v_textlines, key=lambda textline: textline.y0, reverse=True
        )

        h_gaps, v_gaps = [], []
        for i in range(1, len(v_textlines)):
            v_gaps.append(v_textlines[i - 1].y0 - v_textlines[i].y0)
        for i in range(1, len(h_textlines)):
            h_gaps.append(h_textlines[i - 1].x0 - h_textlines[i].x0)

        if not h_gaps or not v_gaps:
            return None
        percentile = 75
        gaps_hv = (
            2.0 * np.percentile(h_gaps, percentile),
            2.0 * np.percentile(v_gaps, percentile),
        )
        return gaps_hv

    def search_table_body(
        self,
        gaps_hv: tuple[float, float],
        parse_details: list[Any] | None,
    ) -> list[float] | None:
        """Build a candidate bounding box for the body of a table using network algorithm.

        Parameters
        ----------
        gaps_hv : tuple of float
            The maximum distance allowed to consider surrounding lines/columns
            as part of the same table.
        parse_details : list
            Optional parameter list, in which to store extra information
            to help later visualization of the table creation.

        Returns
        -------
        list of float or None
            The bounding box of the table body as a list of four floats
            [x0, y0, x1, y1] or None if not enough textlines are found.
        """
        most_aligned_tl = self.most_connected_textline()
        max_h_gap, max_v_gap = gaps_hv

        parse_details_search: dict[str, Any] | None = None
        if parse_details is not None:
            parse_details_search = {
                "max_h_gap": max_h_gap,
                "max_v_gap": max_v_gap,
                "iterations": [],
            }
            parse_details.append(parse_details_search)

        bbox = [
            most_aligned_tl.x0,
            most_aligned_tl.y0,
            most_aligned_tl.x1,
            most_aligned_tl.y1,
        ]

        tls_search_space = list(self._textline_to_alignments.keys())
        tls_search_space.remove(most_aligned_tl)
        tls_in_bbox = [most_aligned_tl]
        last_bbox = None
        last_cols_bounds = [(most_aligned_tl.x0, most_aligned_tl.x1)]

        while last_bbox != bbox:
            if parse_details_search is not None:  # is not None
                parse_details_search["iterations"].append(bbox)

            last_bbox = bbox
            closest_tls = find_closest_tls(bbox, tls_search_space)
            bbox, last_cols_bounds, tls_in_bbox, tls_search_space = self.expand_bbox(
                bbox,
                closest_tls,
                tls_search_space,
                gaps_hv,
                last_cols_bounds,
                tls_in_bbox,
            )

        if len(tls_in_bbox) >= MINIMUM_TEXTLINES_IN_TABLE:
            return bbox
        return None

    def expand_bbox(
        self,
        bbox: list[float],
        closest_tls: dict[str, Any],
        tls_search_space: list[Any],
        gaps_hv: tuple[float, float],
        last_cols_bounds: list[Any],
        tls_in_bbox: list[Any],
    ) -> tuple[list[float], list[Any], list[Any], list[Any]]:
        """Expand the bounding box based on closest textlines.

        Parameters
        ----------
        bbox : list of float
            The current bounding box.
        closest_tls : dict
            The closest textlines found.
        tls_search_space : list
            The list of textlines available for searching.
        gaps_hv : tuple of float
            The maximum allowed horizontal and vertical gaps.
        last_cols_bounds : list of tuple
            The boundaries of the last found columns.
        tls_in_bbox : list
            The textlines currently in the bounding box.

        Returns
        -------
        tuple
            The updated bounding box, column boundaries, textlines in bbox, and search space.
        """
        cand_bbox = bbox.copy()

        for direction, textline in closest_tls.items():
            if textline is None or not self.can_expand_bbox(
                cand_bbox, textline, gaps_hv, direction
            ):
                continue

            expanded_cand_bbox = self.get_expanded_bbox(cand_bbox, textline, direction)
            new_tls = text_in_bbox(expanded_cand_bbox, tls_search_space)
            tls_in_new_box = new_tls + tls_in_bbox

            if not self.is_valid_expansion(direction, tls_in_new_box, last_cols_bounds):
                continue

            bbox = cand_bbox = list(bbox_from_textlines(tls_in_new_box))
            last_cols_bounds = find_columns_boundaries(tls_in_new_box)
            tls_in_bbox.extend(new_tls)
            self.update_search_space(tls_search_space, new_tls)

        return bbox, last_cols_bounds, tls_in_bbox, tls_search_space

    def can_expand_bbox(
        self,
        cand_bbox: list[float],
        textline: Any,
        gaps_hv: tuple[float, float],
        direction: str,
    ):
        #  -> bool TODO
        #  typeguard.TypeCheckError: the return value (numpy.bool_) is not an instance of bool
        """Check if the bounding box can be expanded in the given direction.

        Parameters
        ----------
        cand_bbox : list of float
            The candidate bounding box.
        textline : Any
            The textline to check against.
        gaps_hv : tuple of float
            The maximum allowed horizontal and vertical gaps.
        direction : str
            The direction to check for expansion.

        Returns
        -------
        bool
            True if the bounding box can be expanded, otherwise False.
        """
        if direction == "left":
            return cand_bbox[0] - textline.x1 <= gaps_hv[0]
        elif direction == "right":
            return textline.x0 - cand_bbox[2] <= gaps_hv[0]
        elif direction == "bottom":
            return cand_bbox[1] - textline.y1 <= gaps_hv[1]
        elif direction == "top":
            return textline.y0 - cand_bbox[3] <= gaps_hv[1]
        return False

    def get_expanded_bbox(
        self, cand_bbox: list[float], textline: Any, direction: str
    ) -> list[float]:
        """Get the expanded bounding box based on the textline in the specified direction.

        Parameters
        ----------
        cand_bbox : list of float
            The candidate bounding box.
        textline : Any
            The textline to expand the bounding box with.
        direction : str
            The direction to expand.

        Returns
        -------
        list of float
            The expanded bounding box.
        """
        expanded_cand_bbox = cand_bbox.copy()
        if direction == "left":
            expanded_cand_bbox[0] = textline.x0
        elif direction == "right":
            expanded_cand_bbox[2] = textline.x1
        elif direction == "bottom":
            expanded_cand_bbox[1] = textline.y0
        elif direction == "top":
            expanded_cand_bbox[3] = textline.y1
        return expanded_cand_bbox

    def is_valid_expansion(
        self,
        direction: str,
        tls_in_new_box: list[Any],
        last_cols_bounds: list[Any],
    ) -> bool:
        """Check if the new expansion is valid.

        Parameters
        ----------
        direction : str
            The direction of expansion.
        tls_in_new_box : list
            The textlines in the new bounding box.
        last_cols_bounds : list of tuple
            The boundaries of the last found columns.

        Returns
        -------
        bool
            True if the expansion is valid, otherwise False.
        """
        cols_bounds = find_columns_boundaries(tls_in_new_box)
        return not (
            direction in ["bottom", "top"] and len(cols_bounds) < len(last_cols_bounds)
        )

    def update_search_space(
        self, tls_search_space: list[Any], new_tls: list[Any]
    ) -> None:
        """Update the search space by removing textlines in the new bounding box.

        Parameters
        ----------
        tls_search_space : list
            The current search space of textlines.
        new_tls : list
            The new textlines added to the bounding box.
        """
        for i in range(len(tls_search_space) - 1, -1, -1):
            textline = tls_search_space[i]
            if textline in new_tls:
                del tls_search_space[i]

    def generate(self, textlines: list[Any]) -> None:
        """Generate the text edge dictionaries based on the input textlines.

        Parameters
        ----------
        textlines : list
            List of textline objects to be processed.
        """
        self._register_all_text_lines(textlines)
        self._compute_alignment_counts()


class Network(TextBaseParser):
    """Network method looks for spaces between text to parse the table.

    If you want to specify columns when specifying multiple table
    areas, make sure that the length of both lists are equal.

    Parameters
    ----------
    table_regions : list, optional (default: None)
        List of page regions that may contain tables of the form x1,y1,x2,y2
        where (x1, y1) -> left-top and (x2, y2) -> right-bottom
        in PDF coordinate space.
    table_areas : list, optional (default: None)
        List of table area strings of the form x1,y1,x2,y2
        where (x1, y1) -> left-top and (x2, y2) -> right-bottom
        in PDF coordinate space.
    columns : list, optional (default: None)
        List of column x-coordinates strings where the coordinates
        are comma-separated.
    split_text : bool, optional (default: False)
        Split text that spans across multiple cells.
    flag_size : bool, optional (default: False)
        Flag text based on font size. Useful to detect
        super/subscripts. Adds <s></s> around flagged text.
    strip_text : str, optional (default: '')
        Characters that should be stripped from a string before
        assigning it to a cell.
    edge_tol : int, optional (default: 50)
        Tolerance parameter for extending textedges vertically.
    row_tol : int, optional (default: 2)
        Tolerance parameter used to combine text vertically,
        to generate rows.
    column_tol : int, optional (default: 0)
        Tolerance parameter used to combine text horizontally,
        to generate columns.

    """

    def __init__(
        self,
        table_regions=None,
        table_areas=None,
        columns=None,
        flag_size=False,
        split_text=False,
        strip_text="",
        edge_tol=None,
        row_tol=2,
        column_tol=0,
        debug=False,
        **kwargs,
    ):
        super().__init__(
            "network",
            table_regions=table_regions,
            table_areas=table_areas,
            columns=columns,
            flag_size=flag_size,
            split_text=split_text,
            strip_text=strip_text,
            edge_tol=edge_tol,
            row_tol=row_tol,
            column_tol=column_tol,
            debug=debug,
        )

    def _generate_table_bbox(self):
        user_provided_bboxes = self._get_user_provided_bboxes()
        all_textlines = self._get_filtered_textlines()
        textlines_processed = {}
        self.table_bbox_parses = {}

        parse_details_network_searches, parse_details_bbox_searches = (
            self._initialize_parse_details()
        )

        while True:
            bbox_body = self._find_bbox_body(
                user_provided_bboxes,
                all_textlines,
                parse_details_network_searches,
                parse_details_bbox_searches,
            )
            if bbox_body is None:
                break

            tls_in_bbox = textlines_overlapping_bbox(bbox_body, all_textlines)
            cols_boundaries = find_columns_boundaries(tls_in_bbox)
            cols_anchors = boundaries_to_split_lines(cols_boundaries)

            bbox_full = self._find_full_bbox(
                user_provided_bboxes, tls_in_bbox, cols_anchors
            )

            table_parse = {
                "bbox_body": bbox_body,
                "cols_boundaries": cols_boundaries,
                "cols_anchors": cols_anchors,
                "bbox_full": bbox_full,
            }
            self.table_bbox_parses[bbox_full] = table_parse

            if self.parse_details is not None:
                self.parse_details["col_searches"].append(table_parse)

            self._mark_processed_textlines(
                tls_in_bbox, textlines_processed, all_textlines
            )

    def _get_user_provided_bboxes(self):
        if self.table_areas is not None:
            return [bbox_from_str(area_str) for area_str in self.table_areas]
        return None

    def _get_filtered_textlines(self):
        all_textlines = [
            t
            for t in self.horizontal_text + self.vertical_text
            if len(t.get_text().strip()) > 0
        ]
        return self._apply_regions_filter(all_textlines)

    def _initialize_parse_details(self):
        if self.parse_details is not None:
            self.parse_details["network_searches"] = []
            self.parse_details["bbox_searches"] = []
            self.parse_details["col_searches"] = []
            return (
                self.parse_details["network_searches"],
                self.parse_details["bbox_searches"],
            )
        return None, None

    def _find_bbox_body(
        self,
        user_provided_bboxes,
        textlines,
        parse_details_network_searches,
        parse_details_bbox_searches,
    ):
        if user_provided_bboxes:
            return user_provided_bboxes.pop() if user_provided_bboxes else None
        else:
            text_network = TextNetworks()
            text_network.generate(textlines)
            text_network.remove_unconnected_edges()
            gaps_hv = text_network.compute_plausible_gaps()
            if gaps_hv is None:
                return None

            edge_tol_hv = (
                gaps_hv[0],
                gaps_hv[1] if self.edge_tol is None else self.edge_tol,
            )
            bbox_body = text_network.search_table_body(
                edge_tol_hv, parse_details=parse_details_bbox_searches
            )

            if parse_details_network_searches is not None:
                parse_details_network_searches.append(copy.deepcopy(text_network))

            return bbox_body

    def _find_full_bbox(self, user_provided_bboxes, tls_in_bbox, cols_anchors):
        if user_provided_bboxes is not None:
            return tls_in_bbox  # Assuming bbox_body is the full bbox here as per the logic.
        else:
            bbox_body = bbox_from_textlines(tls_in_bbox)
            # Apply heuristic to salvage headers
            return search_header_from_body_bbox(
                bbox_body, tls_in_bbox, cols_anchors, gaps_hv[1]
            )

    def _mark_processed_textlines(
        self, tls_in_bbox, textlines_processed, all_textlines
    ):
        for textline in tls_in_bbox:
            textlines_processed[textline] = None
        all_textlines[:] = [
            textline
            for textline in all_textlines
            if textline not in textlines_processed
        ]

    def _generate_columns_and_rows(self, bbox, user_cols):
        # select elements which lie within table_bbox
        self.t_bbox = text_in_bbox_per_axis(
            bbox, self.horizontal_text, self.vertical_text
        )

        all_tls = list(
            sorted(
                filter(
                    lambda textline: len(textline.get_text().strip()) > 0,
                    self.t_bbox["horizontal"] + self.t_bbox["vertical"],
                ),
                key=lambda textline: (-textline.y0, textline.x0),
            )
        )
        text_x_min, text_y_min, text_x_max, text_y_max = bbox_from_textlines(all_tls)
        # FRHTODO:
        # This algorithm takes the horizontal textlines in the bbox, and groups
        # them into rows based on their bottom y0.
        # That's wrong: it misses the vertical items, and misses out on all
        # the alignment identification work we've done earlier.
        rows_grouped = self._group_rows(all_tls, row_tol=self.row_tol)
        rows = self._join_rows(rows_grouped, text_y_max, text_y_min)

        if user_cols is not None:
            cols = [text_x_min] + user_cols + [text_x_max]
            cols = [(cols[i], cols[i + 1]) for i in range(0, len(cols) - 1)]
        else:
            parse_details = self.table_bbox_parses[bbox]
            col_anchors = parse_details["cols_anchors"]
            cols = list(
                map(
                    lambda idx: [col_anchors[idx], col_anchors[idx + 1]],
                    range(0, len(col_anchors) - 1),
                )
            )

        return cols, rows, None, None
