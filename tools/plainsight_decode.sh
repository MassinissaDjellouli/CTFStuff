#!/bin/bash
if [ -z "$1" ]
then
    echo "Pass a ciphertext"
    exit
fi

if [ -z "$2" ]
then
    echo "Pass a cleartext"
    exit
fi
cat $1 | plainsight -m decipher -f $2