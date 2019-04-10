#! /bin/bash

todayfloder=`date +%Y-%m-%d`
path=`pwd`
workpath="`pwd`/Video"

if [ "`ls $workpath`" != "" ]; then

	for floder in `ls $workpath`
	do
		if [ "$floder" != "$todayfloder" ];then
			rm -r $floder
			echo "Remove floder :$floder"
		fi
	done
else
	echo "$workpath is empty"
fi
