{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      treefmt-nix,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        treefmtEval = treefmt-nix.lib.evalModule pkgs ./treefmt.nix;
      in
      {
        packages = {
          default = pkgs.callPackage ./. {
            inherit (pkgs.python3Packages) buildPythonPackage setuptools pytestCheckHook;
          };
        };

        devShells = {
          default = pkgs.mkShell {
            venvDir = ".venv";
            packages =
              with pkgs;
              [
                python3
              ]
              ++ (with pkgs.python3Packages; [
                pip
                venvShellHook
                setuptools
              ]);
          };
        };

        formatter = treefmtEval.config.build.wrapper;

        checks = {
          formatting = treefmtEval.config.build.check self;
        };
      }
    );
}
