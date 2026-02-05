#!/bin/bash 
if [ -z "$1" ]
then
    echo "Pass a cpassword"
    exit
fi
path=$("getPath")
python3 $path"tools/gpp-decrypt/gpp-decrypt.py" -c $1