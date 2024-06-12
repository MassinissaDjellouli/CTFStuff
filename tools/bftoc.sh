#!/bin/bash
if [ -z "$1" ]
then
    echo "Pass a brainfuck file"
    exit
fi
path=$("getPath")
python3 $path"tools/bftoc.py" $1