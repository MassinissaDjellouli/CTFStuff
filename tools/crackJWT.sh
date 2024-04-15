#!/bin/bash
if [ -z "$1" ]
then
    echo "Pass a token"
    exit
fi
jwt-cracker -t $1 -d /usr/share/wordlists/rockyou.txt
