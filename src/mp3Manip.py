from pydub import AudioSegment
import eyed3
from eyed3.id3.frames import ImageFrame

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TCON, TPUB, TENC, TIT3, APIC, WOAR, TMOO


def convert_audio_to_mp3(filepath: str) -> None:
    """Converts mp4 file to mp3, this operation will happen in place

    Args:
        filepath (str): Path the mp3 that will be converted
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
    """Modifies the attributes of a mp3 file at the passed in filepath

    # TODO: document these arguments later

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
