
from pathlib import Path
from uuid import uuid4
import shutil

SCREENSHOTS_DIR = (
    Path.home()
    / ".local/share/sddm-theme-manager/screenshots"
)

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def get_screenshot_dir(theme_id):
    # Keep theme identifiers within our application directory.
    safe_id = Path(theme_id).name

    if safe_id != theme_id or safe_id in ("", ".", ".."):
        raise ValueError("Invalid theme identifier")

    return SCREENSHOTS_DIR / safe_id


def get_custom_screenshots(theme_id):
    directory = get_screenshot_dir(theme_id)

    if not directory.is_dir():
        return []

    return [
        str(path)
        for path in sorted(directory.iterdir())
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def add_screenshots(theme_id, file_paths):
    directory = get_screenshot_dir(theme_id)
    directory.mkdir(parents=True, exist_ok=True)

    added = []

    for file_path in file_paths:
        source = Path(file_path)

        if not source.is_file():
            continue

        if source.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        destination = (
            directory
            / f"{uuid4().hex}{source.suffix.lower()}"
        )

        shutil.copy2(source, destination)
        added.append(str(destination))

    return added

def remove_screenshot(theme_id, screenshot_path):
    directory = get_screenshot_dir(theme_id).resolve()
    screenshot = Path(screenshot_path).resolve()

    # Only allow deleting files inside this theme's
    # custom screenshot directory.
    if screenshot.parent != directory:
        raise ValueError(
            "Cannot remove an original theme screenshot."
        )

    if screenshot.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported screenshot format.")

    if not screenshot.is_file():
        raise FileNotFoundError(
            "Screenshot does not exist."
        )

    screenshot.unlink()

