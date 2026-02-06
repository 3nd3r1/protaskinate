{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
    poetry
    postgresql.pg_config
    gcc
  ];

  shellHook = ''
    poetry install --quiet
    source "$(poetry env info --path)/bin/activate"
  '';
}
