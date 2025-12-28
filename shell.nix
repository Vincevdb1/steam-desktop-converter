{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "Steam Desktop Converter";
  buildInputs = with pkgs; [
    python313
    python313Packages.vdf
    python313Packages.pyinstaller
  ];

  shellHook = ''
  '';
}
