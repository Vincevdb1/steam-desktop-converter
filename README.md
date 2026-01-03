# steam-desktop-converter

Automatically generates `.desktop` launchers for your installed Steam games on Linux, using local game logos. It also cleans up obsolete entries for games that are no longer installed.

## Features

* Generates `.desktop` files for all installed Steam games.
* Uses local `logo.png` from `appcache/librarycache/<AppID>/` as the application icon.
* Ignores non-game entries like Proton, Steam, and Steamworks.
* Cleans up obsolete desktop entries for uninstalled games automatically.
* Works with multiple Steam library folders.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Vincevdb1/steam-desktop-converter.git
cd steam-desktop-converter
```

2. Make sure you have Python 3 or higher installed and the required dependencies:

```bash
pip install -r requirements.txt
```
### Nix

Add the repository to your `inputs`:

```nix
inputs.steam-desktop-converter.url = "github:Vincevdb1/steam-desktop-converter";
```

Then add the package to your configuration:

```nix
{ inputs }:

{
  environment.systemPackages = {
    inputs.steam-desktop-converter.packages.${system}.default
  };
}
```

### Manual Installation


## Usage

```bash
# Default Steam path (~/.steam/steam)
python main.py

# Custom Steam path
python main.py "/path/to/steam"
```

This will:

1. Parse your Steam `libraryfolders.vdf`.
2. Create `.desktop` launchers for each installed game in `~/.local/share/applications/`.
3. Remove `.desktop` files for games that are no longer installed.

### Or make binary with pyinstaller
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

### Options

* `-h` or `--help`: Show usage instructions.

## Notes

* Games with multiple logo files will use the **deepest logo** found in the AppID folder.
* Ignored games: Proton, Steam, Steamworks. You can update the `IGNORED_GAME_NAMES` list in `process.py` to customize.
* Generated `.desktop` files are placed in `~/.local/share/applications/` and are executable.

