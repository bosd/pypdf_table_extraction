"""Creates a pdfium backend class to convert a pdf to a png file."""

from camelot.backends.base import ConversionBackend


PDFIUM_EXC = None

try:
    import pypdfium2 as pdfium

    # return True
except ModuleNotFoundError as e:
    # pdfium = None
    PDFIUM_EXC = e
    # raise ModuleNotFoundError from e

# else:
#     PDFIUM_EXC = None


class PdfiumBackend(ConversionBackend):
    """Classmethod to create PdfiumBackend."""

    def installed(self) -> bool:  # noqa D102
        if not PDFIUM_EXC:
            return True
        return False

    def convert(self, pdf_path: str, png_path: str, resolution: int = 300) -> None:
        """Convert PDF to png.

        Parameters
        ----------
        pdf_path : str
            Path where to read the pdf file.
        png_path : str
            Path where to save png file.

        Raises
        ------
        OSError
            Raise an error if pdfium is not installed
        """
        if not self.installed():
            # return None
            raise OSError(f"pypdfium2 is not available: {PDFIUM_EXC!r}")
            # or ModuleNotFoundError
        doc = pdfium.PdfDocument(pdf_path)
        doc.init_forms()
        image = doc[0].render(scale=resolution / 72).to_pil()
        image.save(png_path)
