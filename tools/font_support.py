"""System-font discovery for the documentation generators (no bundled font files).

Arial and Liberation Sans have compatible metrics. Set KIVI_FONT_REGULAR and
KIVI_FONT_BOLD to use an explicit installed font pair on any operating system.
"""
from functools import lru_cache
import os
from pathlib import Path
import sys

from PIL import ImageFont


def _font_directories():
    user = Path.home()
    if sys.platform == "win32":
        system = Path(os.environ.get("WINDIR", os.environ.get("SystemRoot", "C:/Windows")))
        return [system / "Fonts", Path(os.environ.get("LOCALAPPDATA", user / "AppData/Local")) / "Microsoft/Windows/Fonts"]
    if sys.platform == "darwin":
        return [Path("/System/Library/Fonts"), Path("/Library/Fonts"), user / "Library/Fonts"]
    return [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), user / ".local/share/fonts", user / ".fonts"]


@lru_cache(maxsize=1)
def _installed_fonts():
    files = {}
    for directory in _font_directories():
        if directory.exists():
            for path in sorted(directory.rglob("*")):
                if path.suffix.lower() in {".ttf", ".otf", ".ttc"}:
                    files.setdefault(path.name.lower(), path)
    return files


@lru_cache(maxsize=2)
def font_path(bold=False):
    variable = "KIVI_FONT_BOLD" if bold else "KIVI_FONT_REGULAR"
    override = os.environ.get(variable)
    if override:
        path = Path(override).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"{variable} does not name a font file: {path}")
        return path
    names = ("arialbd.ttf", "arial bold.ttf", "liberationsans-bold.ttf") if bold else (
        "arial.ttf", "liberationsans-regular.ttf")
    installed = _installed_fonts()
    for name in names:
        if name in installed:
            return installed[name]
    raise RuntimeError(
        "No Arial or Liberation Sans font pair found. Install Liberation Sans "
        "(for example the fonts-liberation package on Debian/Ubuntu), or set "
        "KIVI_FONT_REGULAR and KIVI_FONT_BOLD to installed TrueType/OpenType fonts. "
        "Different font metrics may change wrapping; review regenerated diagrams."
    )


@lru_cache(maxsize=None)
def font(size, bold=False):
    return ImageFont.truetype(str(font_path(bold)), int(size))


def svg_font_family():
    family = font(12).getname()[0]
    return f"{family}, Arial, Helvetica, Liberation Sans, sans-serif"


if __name__ == "__main__":
    for label, bold in [("regular", False), ("bold", True)]:
        print(f"{label}: {font_path(bold)}")
