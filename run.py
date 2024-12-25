import sys
from pathlib import Path
from rich.console import Console
import click

import src.validator as v
import src.downloadUtil as du
import src.printer as printer


@click.command()
@click.option(
    "-l",
    "--link",
    "link",
    type=click.STRING,
    help="Link to youtube video that will be downloaded, cannot be used with --file(file flags takes precedents)",
)
@click.option(
    "-f",
    "--file",
    "filePath",
    type=click.STRING,
    help="path to txt file of youtube links separated by new lines, cannot be used it --link",
)
@click.option(
    "-d", "--save-dir", "save_dir", required=True, type=click.STRING, help="Path to where the mp3 will be downloaded"
)
def ytos(link: str, save_dir: str, filePath: str) -> None:
    """
    Youtube to spotify script will take a given Youtube video URL and download the mpo3
    of the specified video to a Spotify local folder
    """
    console = Console()
    errConsole = Console(stderr=True)

    if filePath and link != None:
        errConsole.print("Can only have either --link or --file set at once")
        sys.exit(1)

    readList: bool = False
    if filePath != None:
        readList = True

    entryMsg: str = ""

    if readList:
        entryMsg = f"Attempting to download songs from list [bold green]{printer.linkString(filePath, filePath)}[/bold green] to [italic green]{printer.linkString(save_dir,save_dir)}[/italic green]"
    else:
        entryMsg = f"Attempting to download [bold green]{printer.linkString(link, link)}[/bold green] to [italic green]{printer.linkString(save_dir,save_dir)}[/italic green]"

    console.print(entryMsg + "\n")

    if not v.is_valid_url(link) and not readList:
        errConsole.print("Youtube URL: [bold red]{link}[/bold red] is malformed and not a valid URL")
        sys.exit(-1)
    elif not v.is_download_dir_valid(save_dir):
        errConsole.print(
            f"Download directory: [bold red]{save_dir}[/bold red] is not a valid directory to download the mp3 to"
        )
        sys.exit(-1)
    elif not v.file_exists(filePath) and link != None:
        errConsole.print(f"List of youtube links : [bold red]{filePath}[/bold red] is not a valid file")
        sys.exit(1)
    elif readList:
        with open(filePath, "r") as file:
            # Loop through each line in the file
            for line in file:
                # Remove any leading/trailing whitespace (like newline characters)
                link = line.strip()

                # Perform any operation on the link (e.g., print it, or replace with your operation)
                du.download_mp3_to_dir(link, save_dir)
        sys.exit(0)
    else:
        du.download_mp3_to_dir(link, save_dir)
        sys.exit(0)


if __name__ == "__main__":
    ytos()
