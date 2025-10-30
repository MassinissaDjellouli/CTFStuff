#!/bin/bash

chmod +x ./getPath
dos2unix ./getPath
path=$("./getPath")

run(){
    local name=$1

    executable = $path'tools/'$name
    dos2unix $executable
    chmod +x $executable
    $executable
}

# java=$("./getJavaPath")
export='export PATH="$PATH:'$path'tools"'
grep -qxF "$export" ~/.bashrc || echo "$export" >> ~/.bashrc

alias1='alias java="java.exe"'
alias2='alias ctf="cd '$path'"'
grep -qxF "$alias1" ~/.bashrc || echo "$alias1" >> ~/.bashrc
grep -qxF "$alias2" ~/.bashrc || echo "$alias2" >> ~/.bashrc

run "setup_plainsight.sh"
run "instal_vol.sh"
