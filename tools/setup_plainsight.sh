#!/bin/bash

sudo apt install python2
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
sudo python2 get-pip.py
pip2 install bitstring
pip2 install plainsight
sed -i -e 's/python /python2 /g' $(which plainsight)