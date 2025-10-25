import os
import sys
import vdf


def build_vdf_path(steam_root: str | None = None) -> str:
    """Build the full path to libraryfolders.vdf from a given Steam root."""
    if steam_root is None:
        steam_root = os.path.expanduser("~/.steam/steam")
    else:
        steam_root = os.path.expanduser(steam_root)
    return os.path.join(steam_root, "steamapps", "libraryfolders.vdf")


def load_vdf(path: str) -> dict:
    """Load and parse a VDF file."""
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return vdf.load(f)
    except Exception as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        sys.exit(1)


def extract_game_ids(vdf_data: dict) -> list[str]:
    """Extract all game IDs from a parsed libraryfolders.vdf."""
    game_ids = set()
    libraries = vdf_data.get("libraryfolders", vdf_data)

    for lib_id, lib_data in libraries.items():
        if isinstance(lib_data, dict) and "apps" in lib_data:
            game_ids.update(lib_data["apps"].keys())

    return sorted(game_ids, key=int)


def get_library_paths(vdf_data: dict) -> list[str]:
    """Extract all library folder paths from the parsed libraryfolders.vdf."""
    libraries = vdf_data.get("libraryfolders", vdf_data)
    paths = []

    for lib_id, lib_data in libraries.items():
        if isinstance(lib_data, dict) and "path" in lib_data:
            paths.append(os.path.expanduser(lib_data["path"]))
    return paths
