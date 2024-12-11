from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix import StreamQuery
from pytubefix import Stream
import urllib

# Local imports
from . import validator as v
from . import fileManip as fm
from . import mp3Manip as mp3m

TEMP_THUMBNAIL_PATH = "temp/thumbnail/image.jpg"


def download_mp3_to_dir(youtube_url: str, download_dir: str):
    """Downloads the mp3 from the YouTube URL to the download dir while modifying any mp3 attributes if needed

    Args:
        youtube_url (str): URL to YouTube Video
        download_dir (str): Directory where the mp3 should be downloaded to
    """
    # if temp dir does not exist, make one
    fm.create_temp_dir()

    video: YouTube = YouTube(youtube_url, on_progress_callback=on_progress)
    artist: str = video.author
    title: str = video.title
    # ? See why this is not used
    # publish_date: datetime = video.publish_date
    thumbnail_url: str = video.thumbnail_url
    has_image: bool = False

    # download the thumbnail is available
    # will later attach to mp3 for track image, if one is not already applied
    if v.is_valid_url(thumbnail_url):
        # this return a tuple but I don't really need the information from it
        urllib.request.urlretrieve(thumbnail_url, TEMP_THUMBNAIL_PATH)
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
    mp3m.convert_audio_to_mp3(downloaded_file_path)

    mp3m.edit_mp3_metadata(
        downloaded_file_path, title=title, album_artist=artist, author_url=youtube_url, contributing_artists=artist
    )

    if has_image:
        mp3m.add_album_art(downloaded_file_path, album_art_file=TEMP_THUMBNAIL_PATH)

    # after editing mp3, move it to the correct location
    fm.move(downloaded_file_path, download_dir)

    # remove the temp dir
    fm.clean_up()
