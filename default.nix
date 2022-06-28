{ pkgs ? import <nixpkgs> {} }:

with pkgs;

stdenv.mkDerivation rec {
  name = "rtos-1";
  python = python37.withPackages(ps: with ps; [ matplotlib ]);
  buildInputs = [
    python
  ];
}
