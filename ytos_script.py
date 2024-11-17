import sys
import validators
import os
import urllib.request
import shutil
import datetime
from typing import Optional

from pydub import AudioSegment

import eyed3
from eyed3.id3.frames import ImageFrame

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TCON, TPUB, TENC, TIT3, APIC, WOAR, TMOO

from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix import StreamQuery
from pytubefix import Stream


def is_download_dir_valid(dir: str) -> bool:
    """Checks if the download directory exist and is valid
        THIS WILL NOT CREATE A DIR FOR YOU!
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


# TODO: clean this up, add the rest of the docs to the code
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
        urllib.request.urlretrieve(thumbnail_url, thumbnail_path)
        has_image = True

    # get all streams from the video
    streams: StreamQuery = video.streams

    # extract only the mp3 from the video
    audio_from_video: Stream = streams.get_audio_only()
    downloaded_file_path = audio_from_video.download(output_path="temp/mp3", mp3=True, max_retries=10)

    """
    For some reason when downloading the video and then extracting audio only from youtube, the audio file actually 
    follows the m4a codec. This causes problems when trying the modify mp3 specific attributes that use the ID3 header.
    To fix that, convert the mystery file into an actual mp3 using some ffmpeg magic and then you're able to modify the
    mp3 attributes.
    """
    convert_audio_to_mp3(downloaded_file_path)

    edit_mp3_metadata(
        downloaded_file_path, title=title, album_artist=artist, author_url=youtube_url, contributing_artists=artist
    )

    if has_image:
        add_album_art(downloaded_file_path, album_art_file=thumbnail_path)

    # after editing mp3, move it to the correct location
    shutil.move(downloaded_file_path, download_dir)

    # remove the temp dir
    clean_up()


def convert_audio_to_mp3(filepath: str) -> None:
    """_summary_

    Args:
        filepath (str): _description_
    """
    audio = AudioSegment.from_file(filepath, format="mp4")
    audio.export(filepath, format="mp3")
    pass


def edit_mp3_metadata(
    mp3_file,
    title=None,
    subtitle=None,
    contributing_artists=None,
    album_artist=None,
    album=None,
    genre=None,
    publisher=None,
    encoded_by=None,
    author_url=None,
    mood=None,
):
    """_summary_

    Args:
        mp3_file (_type_): _description_
        title (_type_, optional): _description_. Defaults to None.
        subtitle (_type_, optional): _description_. Defaults to None.
        contributing_artists (_type_, optional): _description_. Defaults to None.
        album_artist (_type_, optional): _description_. Defaults to None.
        album (_type_, optional): _description_. Defaults to None.
        genre (_type_, optional): _description_. Defaults to None.
        publisher (_type_, optional): _description_. Defaults to None.
        encoded_by (_type_, optional): _description_. Defaults to None.
        author_url (_type_, optional): _description_. Defaults to None.
        mood (_type_, optional): _description_. Defaults to None.
    """
    audio = MP3(mp3_file, ID3=ID3)

    if title:
        audio["TIT2"] = TIT2(encoding=3, text=title)  # Title
    if subtitle:
        audio["TIT3"] = TIT3(encoding=3, text=subtitle)  # Subtitle
    if contributing_artists:
        audio["TPE1"] = TPE1(encoding=3, text=contributing_artists)  # Contributing artists
    if album_artist:
        audio["TPE2"] = TPE2(encoding=3, text=album_artist)  # Album artist
    if album:
        audio["TALB"] = TALB(encoding=3, text=album)  # Album
    if genre:
        audio["TCON"] = TCON(encoding=3, text=genre)  # Genre
    if publisher:
        audio["TPUB"] = TPUB(encoding=3, text=publisher)  # Publisher
    if encoded_by:
        audio["TENC"] = TENC(encoding=3, text=encoded_by)  # Encoded by
    if author_url:
        audio["WOAR"] = WOAR(encoding=3, url=author_url)  # Author URL
    if mood:
        audio["TMOO"] = TMOO(encoding=3, text=mood)  # Mood(what?)
    audio.save()


def add_album_art(mp3_file, album_art_file):
    """_summary_

    Args:
        mp3_file (_type_): _description_
        album_art_file (_type_): _description_
    """

    audio_file = eyed3.load(mp3_file)

    if audio_file.tag == None:
        audio_file.initTag()

    audio_file.tag.images.set(ImageFrame.FRONT_COVER, open(album_art_file, "rb").read(), "image/jpeg")

    audio_file.tag.save(version=eyed3.id3.ID3_V2_3)  # need to provide ID3 version or image does not show

    # audio = MP3(mp3_file, ID3=ID3)
    # if audio.tags is None:
    #     audio.add_tags()

    # # Open album art image
    # with open(album_art_file, "rb") as img:
    #     audio.tags.add(
    #         APIC(
    #             encoding=3,  # 3 is for utf-8
    #             mime="image/jpeg",  # or image/png
    #             type=3,  # 3 is for the album front cover
    #             desc="Cover",
    #             data=img.read(),
    #         )
    #     )

    # audio.save()


def main():
    # the youtube url is passed first from the bash script
    youtube_url = sys.argv[1]
    download_dir = sys.argv[2]
    # # TODO: take out later for debugging reasons
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
