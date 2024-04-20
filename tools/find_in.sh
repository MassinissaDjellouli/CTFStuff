#!/bin/bash
if [ -z "$1" ]
then
    echo "Pass a directory path"
    exit
fi

if [ -z "$2" ]
then
    echo "Pass a string to find"
    exit
fi
grep -Rnw "$1" -e "$2"