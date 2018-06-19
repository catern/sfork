let pkgs = import <nixpkgs> {}; in
with pkgs.python36Packages;
buildPythonPackage {
  name = "sfork";
  src = ./.;
  propagatedBuildInputs = [ (import ../c) cffi pkgconfig ];
}

