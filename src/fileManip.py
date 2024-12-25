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
def overwrite_move(src: str, dest: str) -> None:
    """
    Moves a file to the destination, overwriting the destination file if it already exists.

    Args:
        src (str): The source file path.
        dest (str): The destination file path.

    Returns:
        None
    """
    srcPathAsList: list[str] = src.split("/")
    fileName: str = srcPathAsList[len(srcPathAsList) - 1]
    if os.path.exists(dest + fileName):
        os.remove(dest + fileName)  # Remove the existing file
    shutil.move(src, dest)
