import os
import shutil


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


# TODO: fix bug where if file already exist then don't try to move
def move(src: str, dest: str) -> None:
    """Moves file at src to dest

    Args:
        src (str): Source file
        dest (str): destination location
    """
    shutil.move(src, dest)
