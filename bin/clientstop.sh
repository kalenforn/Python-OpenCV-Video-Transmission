#! /bin/bash

clid=`ps -ef | grep "python3.*client.py$"| grep -o "[0-9]\+  " | head -n 1`

kill -9 $clid
echo "killed client job at $clid."

