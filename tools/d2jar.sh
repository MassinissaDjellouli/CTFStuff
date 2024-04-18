#!/bin/bash 
if [ -z "$1" ]
then
    echo "Pass an apk file path"
    exit
fi
res=$(echo "$1" | sed 's/\.apk/\.jar/g')
/mnt/c/Windows/System32/cmd.exe /C "C:\Users\massi\Desktop\CTFStuff\tools\dex-tools-v2.4\d2j-dex2jar.bat -f $1 -o $res"