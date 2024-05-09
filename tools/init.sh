#!/bin/bash
path=$("./getPath")
java=$("./getJavaPath")
export='export PATH="$PATH:'$java':'$path'tools"'
grep -qxF "$export" ~/.bashrc || echo "$export" >> ~/.bashrc

aliases='alias java="java.exe";alias ctf="cd '$path
grep -qxF "$aliases" ~/.bashrc || echo "$aliases" >> ~/.bashrc