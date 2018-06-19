with import <nixpkgs> {};
stdenv.mkDerivation {
  name = "sfork";
  src = ./.;
  buildInputs = [ autoconf automake libtool pkgconfig autoreconfHook ];
}
