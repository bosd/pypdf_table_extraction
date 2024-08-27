This page of the wiki aims to compare pypdf_table_extraction's output (qualitatively) with other open-source libraries and tools. Chances are that you've already used one of the libraries/tools mentioned below, have had problems with getting the desired output and are here to see if pypdf_table_extraction can extract tables from your PDFs better.

We believe that pypdf_table_extraction works better than other open-source alternatives out there, we try to avoid bias though, and be fair and accurate here, by listing down advantages other tools might have over pypdf_table_extraction. (While also listing down steps with which pypdf_table_extraction makes up for them using one or more of the configuration parameters.)

We would like your help to keep this document up-to-date. If notice any inconsistency, please let us know by [opening an issue](https://github.com/py-pdf/pypdf_table_extraction/issues/new?title=Inconsistency+on+comparison+page).

**Table of contents**

* [Tabula](#Tabula)
* [pdfplumber](#pdfplumber)
* [pdftables](#pdftables)
* [pdf-table-extract](#pdf-table-extract)

# [Tabula](https://github.com/tabulapdf/tabula)

The naming for parsing methods inside pypdf_table_extraction (i.e. Lattice and Stream) was inspired from Tabula. Lattice is used to parse tables that have demarcated lines between cells, while Stream is used to parse tables that have whitespaces between cells to simulate a table structure.

We took 10 PDFs of each type (lines, for Lattice and whitespaces between tables cells, for Stream) and passed them through Tabula's web interface and pypdf_table_extraction's command-line interface. The CSV outputs were pushed to this repo as is. We found that pypdf_table_extraction works better than Tabula in all Lattice cases. Tabula does better table detection for Stream cases, but it still fails to give good parsing output, which pypdf_table_extraction solves for with its configuration parameters.


We put a ✔️ in the "Table detected correctly?" column if the table was detected accurately and ❌ if it was not (providing an image of the detected table in both cases). The reasoning behind which output is better is provided in the "Comments" column.

## Lattice

<table>
  <tr>
    <th>n</th>
    <th>PDF</th>
    <th>Notes</th>
    <th colspan="2">Table detected correctly?</th>
    <th colspan="2">Extra configuration used?</th>
    <th colspan="2">Result</th>
    <th>Which has better output?</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td>Tabula</td>
    <td>pypdf_table_extraction</td>
    <td>Tabula</td>
    <td>pypdf_table_extraction</td>
    <td>Tabula</td>
    <td>pypdf_table_extraction</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>1.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat.pdf">agstat.pdf</a></td>
    <td>Header text is vertical, columns span multiple cells.</td>
    <td>:x: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula doesn't output all the header text. pypdf_table_extraction gets all the headers in the correct cells, albeit in reverse order in some cases.</td>
  </tr>
  <tr>
    <td>2.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_1/background_lines_1.pdf">background_lines_1.pdf</a></td>
    <td>The lines are in background.</td>
    <td>:x: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_1/background_lines_1-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_1/background_lines_1-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td><pre>-back</pre></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_1/background_lines_1-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_1/background_lines_1-data-camelot-page-1-table-2.csv">csv</a></td>
    <td>Both</td>
    <td></td>
  </tr>
  <tr>
    <td>3.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_2/background_lines_2.pdf">background_lines_2.pdf</a></td>
    <td>The lines are in background.</td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_2/background_lines_2-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_2/background_lines_2-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td><pre>-scale 40</pre> <pre>-back</pre></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_2/background_lines_2-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/background_lines_2/background_lines_2-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula shifts some of the data points towards the left. pypdf_table_extraction gets the table as is.</td>
  </tr>
  <tr>
    <td>4.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1.pdf">column_span_1.pdf</a></td>
    <td>Columns spans multiple cells.</td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula moves some headers on the top-right to the left. pypdf_table_extraction gets them in the correct cells.</td>
  </tr>
  <tr>
    <td>5.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_2/column_span_2.pdf">column_span_2.pdf</a></td>
    <td>Columns spans multiple cells.</td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_2/column_span_2-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_2/column_span_2-table-detection-tabula.png">image</a></td>
    <td>NA</td>
    <td><pre>-scale 40</pre></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_2/column_span_2-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_2/column_span_2-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula shifts some of the data points towards the left. pypdf_table_extraction gets the table as is. (For ex: The number 1728)</td>
  </tr>
  <tr>
    <td>6.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/electoral_roll/electoral_roll.pdf">electoral_roll.pdf</a></td>
    <td>Very unusual table.</td>
    <td>:heavy_check_mark: (almost) <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/electoral_roll/electoral_roll-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/electoral_roll/electoral_roll-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td><pre>-scale 40</pre> <pre>-I 1</pre></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/electoral_roll/electoral_roll-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/electoral_roll/electoral_roll-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula doesn't give an output. pypdf_table_extraction is able to get all text out while preserving the table structure, which is usable by cleaning after some patter matching.</td>
  </tr>
  <tr>
    <td>7.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated.pdf">rotated.pdf</a></td>
    <td>The table is rotated counter-clockwise.</td>
    <td>:x: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula output is unusable, pypdf_table_extraction gets the table out as is.</td>
  </tr>
  <tr>
    <td>8.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/row_span/row_span.pdf">row_span_1.pdf</a></td>
    <td>Rows span multiple cells.</td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/row_span/row_span-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/row_span/row_span-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td><pre>-scale 40</pre> <pre>-block 99</pre> <pre>-const -20</pre></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/row_span/row_span-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/row_span/row_span-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula shifts some of the data points towards the left. pypdf_table_extraction gets the table as is. Check out the totals near the bottom-right.</td>
  </tr>
  <tr>
    <td>9.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1.pdf">twotables_1.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td>:heavy_check_mark: (almost) <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-table-detection-camelot.png">image</a></td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-tabula.csv">csv</a></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula output is unusable, pypdf_table_extraction gets the tables out as they are.</td>
  </tr>
  <tr>
    <td>10.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2.pdf">twotables_2.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-table-detection-tabula.png">image</a></td>
    <td>:heavy_check_mark: <a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-table-detection-camelot.png">image</a></td>
    <td></td>
    <td>No</td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-tabula-0.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-tabula-1.csv">csv2</a></li></ul></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>Both</td>
    <td></td>
  </tr>
</table>

## Stream

<table>
  <tr>
    <th>n</th>
    <th>PDF</th>
    <th>Notes</th>
    <th colspan="2">Table detected correctly?</th>
    <th colspan="2">Extra configuration used?</th>
    <th colspan="2">Result</th>
    <th>Which has better output?</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td>Tabula</td>
    <td>pypdf_table_extraction</td>
    <td>Tabula</td>
    <td>pypdf_table_extraction</td>
    <td>Tabula</td>
    <td>pypdf_table_extraction</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>1.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/12s0324/12s0324.pdf">12s0324.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/12s0324/12s0324-data-tabula-0.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/12s0324/12s0324-data-tabula-1.csv">csv2</a></li></ul></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/12s0324/12s0324-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/12s0324/12s0324-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>Both</td>
    <td></td>
  </tr>
  <tr>
    <td>2.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/birdisland/birdisland.pdf">birdisland.pdf</a></td>
    <td>PDF is encrypted.</td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/birdisland/birdisland-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/birdisland/birdisland-data-camelot-page-1-table-2.csv">csv</a></td>
    <td>Tabula</td>
    <td>pypdf_table_extraction detects two tables, and even though the structure is correct, duplicate strings are found in the same cells. Bug filed. <a href="https://github.com/socialcopsdev/camelot/issues/103">#103</a>.</td>
  </tr>
  <tr>
    <td>3.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget.pdf">budget.pdf</a></td>
    <td></td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula merges the last two columns into one, pypdf_table_extraction gets them correctly.</td>
  </tr>
  <tr>
    <td>4.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health.pdf">district_health.pdf</a></td>
    <td></td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula merges all the columns. pypdf_table_extraction assigns the data points to the correct cells.</td>
  </tr>
  <tr>
    <td>5.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health.pdf">health.pdf</a></td>
    <td></td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Same as above.</td>
  </tr>
  <tr>
    <td>6.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/m27/m27.pdf">m27.pdf</a></td>
    <td>The text is very close. (difficult to differentiate between columns)</td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td><pre>-C 72,95,209,327,442,529,566,606,683</pre> <pre>-split</pre></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/m27/m27-data-tabula-0.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/m27/m27-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula merges some columns. pypdf_table_extraction uses its "-split" feature along with column separators to cut the text strings at those coordinates and put them in the correct cells.</td>
  </tr>
  <tr>
    <td>7.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns.pdf">mexican_towns.pdf</a></td>
    <td></td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>Both</td>
    <td></td>
  </tr>
  <tr>
    <td>8.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values.pdf">missing_values.pdf</a></td>
    <td>Two columns don't have any values.</td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula merges some columns, pypdf_table_extraction gets them correctly.</td>
  </tr>
  <tr>
    <td>9.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/population_growth/population_growth.pdf">population_growth.pdf</a></td>
    <td></td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td>No</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/population_growth/population_growth-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/population_growth/population_growth-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>Both</td>
    <td></td>
  </tr>
  <tr>
    <td>10.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/superscript/superscript.pdf">superscript.pdf</a></td>
    <td>A number has another number in superscript. (Refer the 2nd column for row starting with Kerala)</td>
    <td>:heavy_check_mark:</td>
    <td>NA</td>
    <td>NA</td>
    <td><pre>-flag</pre></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/superscript/superscript-data-tabula.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/superscript/superscript-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>Tabula merges the superscript with the number, which doesn't matter in this case due to the decimal point but can change the number by 10x without the point. pypdf_table_extraction uses a configuration parameter to delimit the superscripts with <pre>&lt;s&gt;&lt;/s&gt;</pre> tags, so that they can be handled during cleaning.</td>
  </tr>
</table>

# [pdfplumber](https://github.com/jsvine/pdfplumber)

5 PDFs of each type were used from the table above, for which pypdf_table_extraction required no extra configuration. Tables from the selected PDFs were parsed using [this script](https://gist.github.com/vinayak-mehta/8a3bf37350b241b966483d202a5109b9) (which uses pdfplumber) and pypdf_table_extraction's command-line-interface.

The reasoning behind which output is better is provided in the "Comments" column.

<table>
  <tr>
    <th>n</th>
    <th>PDF</th>
    <th>Notes</th>
    <th colspan="2">Result</th>
    <th>Which has better output?</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td>pdfplumber</td>
    <td>pypdf_table_extraction</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>1.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat.pdf">agstat.pdf</a></td>
    <td>Header text is vertical, columns span multiple cells.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-pdfplumber.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdfplumber messes up header text.</td>
  </tr>
  <tr>
    <td>2.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1.pdf">column_span_1.pdf</a></td>
    <td>Columns spans multiple cells.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-pdfplumber.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>Both</td>
    <td></td>
  </tr>
  <tr>
    <td>3.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated.pdf">rotated.pdf</a></td>
    <td>The table is rotated counter-clockwise.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-pdfplumber.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdfplumber output unusable.</td>
  </tr>
  <tr>
    <td>4.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1.pdf">twotables_1.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-pdfplumber.csv">csv</a></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>pypdf_table_extraction</td>
    <td>pdfplumber doesn't identify two tables and output is unusable.</td>
  </tr>
  <tr>
    <td>5.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2.pdf">twotables_2.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-pdfplumber.csv">csv</a></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>pypdf_table_extraction</td>
    <td>pdfplumber doesn't identify two tables and output is unusable.</td>
  </tr>
  <tr>
    <td>6.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget.pdf">budget.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/jsvine/pdfplumber/issues/96">errored</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td></td>
  </tr>
  <tr>
    <td>7.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health.pdf">district_health.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-pdfplumber.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdfplumber output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>8.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health.pdf">health.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-pdfplumber.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdfplumber output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>9.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns.pdf">mexican_towns.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/jsvine/pdfplumber/issues/96">errored</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td></td>
  </tr>
  <tr>
    <td>10.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values.pdf">missing_values.pdf</a></td>
    <td>Two columns don't have any values.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-pdfplumber.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdfplumber output unusable, merged columns.</td>
  </tr>
</table>

# [pdftables](https://github.com/drj11/pdftables)

The open-source development for pdftables was stopped in September 2013, when it became a [closed-source paid tool](https://pdftables.com/).

Again, 5 PDFs of each type were used from the table above, for which pypdf_table_extraction required no extra configuration. Tables from the selected PDFs were parsed using [this script](https://gist.github.com/vinayak-mehta/9e134715793c70845d0c84fce264e0ec) (which uses pdftables) and pypdf_table_extraction's command-line-interface.

Again, the reasoning behind which output is better is provided in the "Comments" column.

<table>
  <tr>
    <th>n</th>
    <th>PDF</th>
    <th>Notes</th>
    <th colspan="2">Result</th>
    <th>Which has better output?</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td>pdftables</td>
    <td>pypdf_table_extraction</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>1.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat.pdf">agstat.pdf</a></td>
    <td>Header text is vertical, columns span multiple cells.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>2.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1.pdf">column_span_1.pdf</a></td>
    <td>Columns spans multiple cells.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>3.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated.pdf">rotated.pdf</a></td>
    <td>The table is rotated counter-clockwise.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable.</td>
  </tr>
  <tr>
    <td>4.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1.pdf">twotables_1.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables doesn't combine multi-line rows.</td>
  </tr>
  <tr>
    <td>5.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2.pdf">twotables_2.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>6.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget.pdf">budget.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>7.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health.pdf">district_health.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>8.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health.pdf">health.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable, merged columns.</td>
  </tr>
  <tr>
    <td>9.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns.pdf">mexican_towns.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>Both</td>
    <td></td>
  </tr>
  <tr>
    <td>10.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values.pdf">missing_values.pdf</a></td>
    <td>Two columns don't have any values.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-pdftables-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pdftables output unusable, merged columns.</td>
  </tr>
</table>

# [pdf-table-extract](https://github.com/ashima/pdf-table-extract)

5 PDFs of each type were used from the table above, for which pypdf_table_extraction required no extra configuration. Tables from the selected PDFs were parsed using [this script](https://gist.github.com/vinayak-mehta/b042ce545779cf7565e6530036e7a9de) (which uses pdf-table-extract) and pypdf_table_extraction's command-line-interface.

The reasoning behind which output is better is provided in the "Comments" column.

<table>
  <tr>
    <th>n</th>
    <th>PDF</th>
    <th>Notes</th>
    <th colspan="2">Result</th>
    <th>Which has better output?</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td></td>
    <td>pdf-table-extract (pte)</td>
    <td>pypdf_table_extraction</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>1.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat.pdf">agstat.pdf</a></td>
    <td>Header text is vertical, columns span multiple cells.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/agstat/agstat-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>Both</td>
    <td>pypdf_table_extraction puts vertical headers in reverse order. Bug filed. [#105]</td>
  </tr>
  <tr>
    <td>2.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1.pdf">column_span_1.pdf</a></td>
    <td>Columns spans multiple cells.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/column_span_1/column_span_1-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pte gives extra columns.</td>
  </tr>
  <tr>
    <td>3.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated.pdf">rotated.pdf</a></td>
    <td>The table is rotated counter-clockwise.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/rotated/rotated-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pte doesn't account for table rotation.</td>
  </tr>
  <tr>
    <td>4.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1.pdf">twotables_1.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_1/twotables_1-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>pypdf_table_extraction</td>
    <td>pte output unusable.</td>
  </tr>
  <tr>
    <td>5.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2.pdf">twotables_2.pdf</a></td>
    <td>There are two tables on a single page.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><ul><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-1.csv">csv1</a></li><li><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/lattice/twotables_2/twotables_2-data-camelot-page-1-table-2.csv">csv2</a></li></ul></td>
    <td>pypdf_table_extraction</td>
    <td>pte detects one table and merges first row with header.</td>
  </tr>
  <tr>
    <td>6.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget.pdf">budget.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/budget/budget-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pte output unusable.</td>
  </tr>
  <tr>
    <td>7.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health.pdf">district_health.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/district_health/district_health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pte output unusable.</td>
  </tr>
  <tr>
    <td>8.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health.pdf">health.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/health/health-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pte output unusable.</td>
  </tr>
  <tr>
    <td>9.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns.pdf">mexican_towns.pdf</a></td>
    <td></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/mexican_towns/mexican_towns-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pte output unusable.</td>
  </tr>
  <tr>
    <td>10.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values.pdf">missing_values.pdf</a></td>
    <td>Two columns don't have any values.</td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-pdf-table-extract-page-1-table-1.csv">csv</a></td>
    <td><a href="https://github.com/socialcopsdev/camelot/blob/master/docs/benchmark/stream/missing_values/missing_values-data-camelot-page-1-table-1.csv">csv</a></td>
    <td>pypdf_table_extraction</td>
    <td>pte output unusable.</td>
  </tr>
</table>