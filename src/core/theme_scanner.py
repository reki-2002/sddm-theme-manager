
from pathlib import Path
import configparser

THEMES_DIR = Path("/usr/share/sddm/themes")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
PREVIEW_NAMES = ("preview", "screenshot", "screen", "thumbnail")


def find_previews(theme_dir):
    images = []

    # Prefer images intended as screenshots or previews.
    for path in sorted(theme_dir.iterdir()):
        if (
            path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
            and any(word in path.stem.lower() for word in PREVIEW_NAMES)
        ):
            images.append(str(path))

    return images


def scan_themes():
    themes = []

    if not THEMES_DIR.exists():
        return themes

    for theme_dir in sorted(THEMES_DIR.iterdir()):
        if not theme_dir.is_dir():
            continue

        metadata = theme_dir / "metadata.desktop"
        if not metadata.is_file():
            continue

        name = theme_dir.name
        description = ""
        author = ""

        config = configparser.ConfigParser(interpolation=None)

        try:
            config.read(metadata, encoding="utf-8")

            if config.has_section("SddmGreeterTheme"):
                section = config["SddmGreeterTheme"]
                name = section.get("Name", name)
                description = section.get("Description", "")
                author = section.get("Author", "")
        except (OSError, configparser.Error):
            pass

        themes.append({
            "id": theme_dir.name,
            "name": name,
            "description": description,
            "author": author,
            "path": str(theme_dir),
            "previews": find_previews(theme_dir),
        })

    return themes
