#!/bin/bash
if [ $# -ne 2 ]; then
    echo "Usage: getFileFromSSH.sh \"ssh -p [PORT] user@hostname\" \"/path/to/file\""
    exit 1
fi
port=$(echo $1 | grep -P -o -- '-p [0-9]{1,5}' | grep -P -o -- '[0-9]{1,5}')
if [ -z $port ]; then
    port=22
fi

address=$(echo $1 | grep -o " .*@.*$" | sed --regexp-extended 's/ -p [0-9]{1,5} //g')
if [ -z $address ]; then
    echo "Hostname is not specified. Give the ssh address in the form of user@hostname"
    exit 1
fi
filename=$(echo $2 | sed --regexp-extended 's/.*\///g')
echo "Downloading $2 to ./$filename from $address using port $port"
scp -P $port $address:$2 ./$filename