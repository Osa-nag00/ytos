import sys
import validators
import os
import urllib.request
import shutil
import datetime
from typing import Optional

import eyed3
from eyed3.core import AudioFile
from eyed3.core import Tag
from eyed3.id3.frames import ImageFrame

from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix import StreamQuery
from pytubefix import Stream


def is_download_dir_valid(dir: str) -> bool:
    """Checks if the download directory exist and is valid
        !THIS WILL NOT CREATE A DIR FOR YOU
    Args:
        dir (str): Directory where the mp3 will be downloaded to

    Returns:
        bool: returns true if dir is valid and exist; false otherwise
    """
    return os.path.isdir(os.path.abspath(dir))


def is_valid_url(url: str) -> bool:
    """Checks if the Youtube URL passed is valid

    Args:
        ytUrl (str): URL to Youtube video

    Returns:
        bool: returns true if URL is not malformed, false otherwise
    """
    return validators.url(url)


def create_temp_dir():
    """Creates the temp directory"""
    if not os.path.exists("temp/"):
        os.mkdir("temp/")
        os.mkdir("temp/mp3/")
        os.mkdir("temp/thumbnail/")


def clean_up():
    """Removes the temp directory"""
    if os.path.exists("temp/"):
        # remove dir tree
        shutil.rmtree("temp/")


# TODO: come back and see if changing the metadata of the mp3 will be possible
def download_mp3_to_dir(youtube_url: str, download_dir: str):
    """Downloads the mp3 from the YouTube URL to the download dir while modifying any mp3 attributes if needed

    Args:
        youtube_url (str): URL to YouTube Video
        download_dir (str): Directory where the mp3 should be downloaded to
    """
    # if temp dir does not exist, make one
    create_temp_dir()

    video: YouTube = YouTube(youtube_url, on_progress_callback=on_progress)
    artist: str = video.author
    title: str = video.title
    publish_date: datetime = video.publish_date
    thumbnail_url: str = video.thumbnail_url
    has_image: bool = False
    thumbnail_path = "temp/thumbnail/image.jpg"

    # download the thumbnail is available
    # will later attach to mp3 for track image, if one is not already applied
    if is_valid_url(thumbnail_url):
        # this return a tuple but I don't really need the information from it
        path, msg = urllib.request.urlretrieve(thumbnail_url, thumbnail_path)
        has_image = True

    # get all streams from the video
    streams: StreamQuery = video.streams

    # extract only the mp3 from the video
    mp3_from_video: Stream = streams.get_audio_only()
    downloaded_file_path = mp3_from_video.download(output_path="temp/mp3", mp3=True, max_retries=10)

    # modify_mp3_metadata(downloaded_file_path, title, artist, publish_date, has_image, thumbnail_path)

    # after editing mp3, move it to the correct location
    shutil.move(downloaded_file_path, download_dir)

    # remove the temp dir
    clean_up()


# TODO: this function seem to just not work at all; WIll fix later
def modify_mp3_metadata(
    mp3_file_path: str,
    title: str,
    artist: str,
    publish_date: datetime,
    has_image: Optional[bool] = False,
    thumbnail_path: Optional[str] = None,
) -> None:

    mp3: AudioFile = eyed3.load(mp3_file_path)

    if mp3.tag == None:
        mp3.initTag()

    mp3.tag.artist = artist
    mp3.tag.album_artist = artist
    mp3.tag.title = title

    if has_image:
        mp3.tag.images.set(ImageFrame.FRONT_COVER, open(thumbnail_path, "rb").read(), "image/jpeg")

    mp3.tag.save(mp3_file_path, version=eyed3.id3.ID3_V2_3)


def main():
    # the youtube url is passed first from the bash script
    youtube_url = sys.argv[1]
    download_dir = sys.argv[2]
    # TODO: take out later for debugging reasons
    # youtube_url = "https://youtu.be/DXk8S3OlBrE?si=j2NnLy0guSUm8te7"
    # download_dir = "mp3s/"  # this will really be the folder passed in from script

    # do a quick validation check on the args passed in
    if not is_valid_url(youtube_url):
        print(f"Youtube URL = {youtube_url} is malformed and not a valid URL")
        sys.exit()
    elif not is_download_dir_valid(download_dir):
        print(f"Download directory = {download_dir} is not a valid directory to download the mp3 to")
        sys.exit()
    else:
        download_mp3_to_dir(youtube_url, download_dir)


if __name__ == "__main__":
    main()
