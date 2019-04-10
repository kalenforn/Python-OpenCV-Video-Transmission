#! /bin/bash

seid=`ps -ef | grep "python3.*server.py$"| grep -o "[0-9]\+  " | head -n 1`

kill -9 $seid
echo "Kiiled server job at $seid."

crontab -r 
echo "Close crontab task."

