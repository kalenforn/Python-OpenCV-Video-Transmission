#! /bin/bash

thispath=`pwd`
cd ..
filename="`pwd`/source/client.py"

python3 $filename &
cd $thispath
