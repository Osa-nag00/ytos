import sys
import validators
import os


def is_download_dir_valid(dir: str) -> bool:
    """Checks if the download directory exist and is valid
        !THIS WILL NOT CREATE A DIR FOR YOU
    Args:
        dir (str): Directory where the mp3 will be downloaded to

    Returns:
        bool: returns true if dir is valid and exist; false otherwise
    """
    return os.path.isdir(dir)


def is_Youtube_url_valid(youtube_url: str) -> bool:
    """Checks if the Youtube URL passed is valid

    Args:
        ytUrl (str): URL to Youtube video

    Returns:
        bool: returns true if URL is not malformed, false otherwise
    """
    return validators.url(youtube_url)


def main():
    # the youtube url is passed first from the bash script
    youtube_url = sys.argv[1]
    download_dir = sys.argv[2]

    # do a quick validation check on the args passed in
    if not is_Youtube_url_valid(youtube_url=youtube_url):
        print(f"Youtube URL = {youtube_url} is malformed and not a valid URL")
        sys.exit(-1)
    elif not is_download_dir_valid(dir=download_dir):
        print(f"Download directory = {download_dir} is not a valid directory to download the mp3 to")
        sys.exit(-1)


if __name__ == "__main__":
    main()
