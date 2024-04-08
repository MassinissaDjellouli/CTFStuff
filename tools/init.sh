#!/bin/bash

export='export PATH="$PATH:/mnt/c/\"Program Files\"/Java/jre-1.8/bin:/mnt/c/Users/massi/Desktop/CTFStuff/tools"'
grep -qxF "$export" ~/.bashrc || echo "$export" >> ~/.bashrc

aliases='alias java="java.exe";alias ctf="cd /mnt/c/Users/massi/Desktop/CTFStuff"'
grep -qxF "$aliases" ~/.bashrc || echo "$aliases" >> ~/.bashrc

