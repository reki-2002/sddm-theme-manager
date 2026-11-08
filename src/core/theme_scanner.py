
from pathlib import Path
import configparser


THEMES_DIR = Path("/usr/share/sddm/themes")


def scan_themes():
    """Find installed SDDM themes."""

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

        config = configparser.ConfigParser(
            interpolation=None
        )

        try:
            config.read(metadata, encoding="utf-8")

            if config.has_section("SddmGreeterTheme"):
                section = config["SddmGreeterTheme"]
                name = section.get("Name", name)
                description = section.get(
                    "Description", ""
                )

        except (OSError, configparser.Error):
            pass

        themes.append({
            "id": theme_dir.name,
            "name": name,
            "description": description,
            "path": str(theme_dir),
        })

    return themes
