{
  description = "Steam Desktop Converter";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      pythonEnv = pkgs.python313.withPackages (ps: with ps; [ vdf pyinstaller ]);
    in
    {
      packages.${system}.default = pkgs.stdenv.mkDerivation {
        pname = "steam-desktop-converter";
        version = "0.1.0";
        src = ./.;

        nativeBuildInputs = [ pythonEnv ];

        buildPhase = ''
          export HOME=$TMPDIR
          pyinstaller --onefile main.py
        '';

        installPhase = ''
          mkdir -p $out/bin
          cp dist/main $out/bin/steam-desktop-converter
        '';
      };

      devShells.${system}.default = pkgs.mkShell {
        name = "Steam Desktop Converter";
        buildInputs = [ pythonEnv ];
      };
    };
}
