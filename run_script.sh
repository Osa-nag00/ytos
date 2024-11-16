#!/bin/bash

# TODO: maybe come back and make this script more verbose?

if [ $# -ne 2 ]; then
    echo "Incorrect number of arguments"
    exit 1
fi

# variables used to pass the link on
song_dl_dir=$1
youtube_link=$2

python "ytos_script.py" $song_dl_dir $youtube_link

# after the python script has finish running
exit 0
