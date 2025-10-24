#!/bin/bash
if [ -z "$1" ]
then
    echo "Pass a cookie"
    exit
fi

if [ -z "$2" ]
then
    echo "Pass a secret"
    exit
fi
flask-unsign --sign --cookie "$1" --secret "$2"