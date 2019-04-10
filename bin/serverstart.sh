#! /bin/bash

thispath=`pwd`
cd ..
path=`pwd`

filename="$path/source/server.py"
VideoPath="$path/Video/"
LogPath="$path/log/" 

cd $thispath

if [ "`crontab -l`" != "no crontab for $USER" ]; then
        crontab -l > conf
        echo "New ./conf"
fi

echo "* * */7 * * $USER bash $thispath/removefile.sh" >> conf && crontab conf && rm -f conf

cd "$path/source"
echo "Starting this project."
python3 $filename >> $LogPath/Run_server_log &

cd $thispath
