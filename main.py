#!/usr/bin/env python3
import sys
import os
from vdf_utils import build_vdf_path, load_vdf
from process import process_games
from cleanup import cleanup_desktop_files


def print_help():
    """Print usage information."""

    print(
        """Usage:
  python main.py [STEAM_PATH]

Description:
  Parses Steam's 'libraryfolders.vdf' and creates .desktop launchers for each installed game.
  Uses local logos from appcache/librarycache/<AppID>/logo.png if available.
  Automatically removes obsolete desktop entries for uninstalled games.

Arguments:
  STEAM_PATH   Optional path to your Steam installation directory.
               Default: ~/.steam/steam

Options:
  -h, --help   You are here right now!
"""
    )


def get_vdf_path() -> str:
    """Determine which libraryfolders.vdf path to use."""

    steam_root = sys.argv[1] if len(sys.argv) > 1 else None
    return build_vdf_path(steam_root)


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0)

    steam_root = (
        os.path.abspath(sys.argv[1])
        if len(sys.argv) > 1
        else os.path.expanduser("~/.steam/steam")
    )
    steam_vdf_path = build_vdf_path(steam_root)
    vdf_data = load_vdf(steam_vdf_path)

    # Generate desktop entries
    process_games(vdf_data, steam_root)

    # Cleanup obsolete desktop entries
    cleanup_desktop_files(vdf_data)


if __name__ == "__main__":
    main()
