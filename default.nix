with import <nixpkgs> { };
with python3.pkgs;
buildPythonPackage rec {
  name = "clibt";
  version = "0.0.1";
  src = ./.;
  propagatedBuildInputs = [ pygame ];
}
