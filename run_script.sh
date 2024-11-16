#!/bin/bash

# VARIABLES
song_dl_dir=''
youtube_link=''

# FUNCTIONS
# Function to display script usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo " -h       Display this help message"
    echo -e "\nRequired:"
    echo " -l       Used to specify the youtube link to download"
    echo " -d       Used to specify to dir of where to download the mp3"
}

# if there is ":" after letter, it means that opt is required
# OPTARG is the current flag being read
while getopts "hl:d:" flag; do
    case $flag in
    h)
        usage
        ;;
    l)
        youtube_link=$OPTARG
        ;;
    d)
        song_dl_dir=$OPTARG
        ;;

    \?)
        usage
        ;;
    esac
done

if [[ -z $youtube_link ]] || [[ -z $song_dl_dir ]]; then
    echo -e "You must specify both -l and -d\n"
    usage
    exit 1
fi

echo -e "\nRunning Python script"
python "ytos_script.py" "$youtube_link" "$song_dl_dir"

exit 0
