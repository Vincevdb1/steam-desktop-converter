import os
import vdf
from vdf_utils import get_library_paths

APPLICATIONS_DIR = os.path.expanduser("~/.local/share/applications/")
IGNORED_GAME_NAMES = ["Proton", "Steam", "Steamworks"]


def parse_appmanifest(manifest_path: str) -> dict | None:
    """Parse an appmanifest_*.acf file to extract basic game info."""
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            return vdf.load(f)
    except Exception:
        return None


def get_game_icon(steam_root: str, app_id: str) -> str:
    """
    Recursively search for logo.png inside appcache/librarycache/<AppID>/.
    Returns the absolute path if found, otherwise an empty string.
    """
    base_path = os.path.join(steam_root, "appcache", "librarycache", app_id)
    if not os.path.isdir(base_path):
        return ""

    # Find the deepest logo.png file
    best_path = ""
    max_depth = 0
    for root, dirs, files in os.walk(base_path):
        if "logo.png" in files:
            depth = root.count(os.sep)
            if depth > max_depth:
                max_depth = depth
                best_path = os.path.join(root, "logo.png")
    return os.path.abspath(best_path) if best_path else ""


def make_desktop_entry(app_id: str, game_name: str, icon_path: str = "") -> str:
    """Create the contents of a .desktop file for a Steam game."""
    exec_cmd = f"xdg-open steam://rungameid/{app_id}"
    icon_line = f"Icon={icon_path}" if icon_path else "Icon=steam"

    return f"""[Desktop Entry]
                Name={game_name}
                Comment=Launch {game_name} via Steam
                Exec={exec_cmd}
                Terminal=false
                Type=Application
                Categories=Game;
                {icon_line}
            """


def save_desktop_file(app_id: str, desktop_content: str) -> None:
    """Save a .desktop file for the given AppID."""
    os.makedirs(APPLICATIONS_DIR, exist_ok=True)
    filename = os.path.join(APPLICATIONS_DIR, f"steam_app_{app_id}.desktop")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(desktop_content)
    os.chmod(filename, 0o755)
    print(f"✅ Created: {filename}")


def process_games(vdf_data: dict, steam_root: str):
    """Process all installed Steam games and create .desktop entries, skipping ignored games."""
    steam_root = os.path.abspath(steam_root)
    library_paths = get_library_paths(vdf_data)
    total_created = 0

    for library in library_paths:
        steamapps = os.path.join(library, "steamapps")
        if not os.path.isdir(steamapps):
            continue

        for file in os.listdir(steamapps):
            if not file.startswith("appmanifest_") or not file.endswith(".acf"):
                continue

            manifest_path = os.path.join(steamapps, file)
            app = parse_appmanifest(manifest_path)
            if not app:
                continue

            app_state = app.get("AppState", {})
            app_id = app_state.get("appid")
            game_name = app_state.get("name")

            if not app_id or not game_name:
                continue

            # Skip games whose name contains any ignored keywords
            if any(ignored_name in game_name for ignored_name in IGNORED_GAME_NAMES):
                continue

            icon_path = get_game_icon(steam_root, str(app_id))
            desktop_content = make_desktop_entry(app_id, game_name, icon_path)
            save_desktop_file(app_id, desktop_content)
            total_created += 1

    print(f"\n🎮 Done! Created {total_created} desktop entries.")
