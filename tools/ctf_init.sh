#!/bin/bash
mkdir "$1"
cd "$1" || exit
python3 -m venv .venv
path="$(./getPath)"
cp "$path/examples/z3sol.py" "./z3.py"
cp "$path/examples/pwnsolve.py" "./pwnsolve.py"