import os

import validators


def file_exists(file_path: str) -> bool:
    """
    Check if a file exists at the given file path.

    Parameters:
    file_path (str): The path to the file to check.

    Returns:
    bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)


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
    answer = validators.url(url)

    if type(answer) is bool:
        return answer
    return False
