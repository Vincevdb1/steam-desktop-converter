import os
import re
from vdf_utils import extract_game_ids

APPLICATIONS_DIR = os.path.expanduser("~/.local/share/applications/")
DESKTOP_PATTERN = re.compile(r"steam_app_(\d+)\.desktop")


def get_desktop_app_ids() -> dict[str, str]:
    """Return a mapping of AppID -> desktop file path for all steam_app_*.desktop files."""

    app_files = {}

    if not os.path.isdir(APPLICATIONS_DIR):
        return app_files

    for file in os.listdir(APPLICATIONS_DIR):
        match = DESKTOP_PATTERN.fullmatch(file)
        if match:
            app_id = match.group(1)
            app_files[app_id] = os.path.join(APPLICATIONS_DIR, file)
    return app_files


def cleanup_desktop_files(vdf_data: dict):
    """Remove .desktop files for games no longer present in Steam libraries."""

    installed_app_ids = set(extract_game_ids(vdf_data))
    desktop_files = get_desktop_app_ids()

    removed_count = 0
    for app_id, file_path in desktop_files.items():
        if app_id not in installed_app_ids:
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

    if removed_count > 0:
        print(f"\nCleanup done. Removed {removed_count} obsolete desktop entries.")
