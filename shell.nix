{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python313
    python313Packages.vdf
  ];

  shellHook = ''
    export NIX_SHELL_DIR=$(basename "$PWD")
  '';
}
