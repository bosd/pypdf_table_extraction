import ctypes
import sys
import ghostscript
from ctypes.util import find_library


def installed_posix():
    library = find_library("gs")
    return library is not None


def installed_windows():
    try:
    #    import ghostscript
         library = ghostscript.gs.__win32_finddll()
    #        library = find_library(
    #            "C:\ProgramData\\".join(("gsdll.dll"))
    #        )
    except RuntimeError:
        return None
    #        library = find_library(
    #            "C:\ProgramData\\".join(("gsdll64.dll"))
    #        )
    return library is not None


class GhostscriptBackend:
    def installed(self):
        if sys.platform in ["linux", "darwin"]:
            return installed_posix()
        elif sys.platform == "win32":
            return installed_windows()
        else:
            return installed_posix()

    def convert(self, pdf_path, png_path, resolution=300):
        if not self.installed():
            raise OSError(
                "Ghostscript is not installed. You can install it using the instructions"
                " here: https://pypdf-table-extraction.readthedocs.io/en/latest/user/install-deps.html"
            )

        import ghostscript

        gs_command = [
            "gs",
            "-q",
            "-sDEVICE=png16m",
            "-o",
            png_path,
            f"-r{resolution}",
            pdf_path,
        ]
        ghostscript.Ghostscript(*gs_command)
