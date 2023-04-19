# shell.nix

{ pkgs ? import <nixpkgs> { } }:

let
  unstable = import <nixos-unstable> { };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    unstable.flutter
  ];
}
