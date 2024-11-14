from pytubefix import YouTube
from pytubefix.cli import on_progress

YOUTUBE_URL: str = "https://youtu.be/FeZ5ruaMSeA?si=u6dGGciC6SmdZlT0"


vid: YouTube = YouTube(YOUTUBE_URL, on_progress_callback=on_progress)

stream = vid.streams.get_audio_only()
stream.download(mp3=True, output_path="./mp3s")
