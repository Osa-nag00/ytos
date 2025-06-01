import sys

import click
import src.downloadUtil as du
import src.fileManip as fm
import src.printer as printer
import src.validator as v
from rich.console import Console


@click.command()
@click.option(
    "-f",
    "--file",
    "filePath",
    type=click.STRING,
    required=True,
    help="path to txt file of youtube links separated by new lines, cannot be used it --link",
)
@click.option(
    "-d",
    "--save-dir",
    "save_dir",
    required=True,
    type=click.STRING,
    help="Path to where the mp3 will be downloaded",
)
def ytos(save_dir: str, filePath: str) -> None:
    """
    Youtube to spotify script will take a given a text file of youtube links to be downloaded to mp3
    of the specified video to a Spotify local folder
    """

    console = Console()
    errConsole = Console(stderr=True)

    entryMsg: str = (
        f"Attempting to download songs from list [bold green]{printer.linkString(filePath, filePath)}[/bold green] to [italic green]{printer.linkString(save_dir,save_dir)}[/italic green]"
    )
    console.print(entryMsg + "\n")

    if not v.is_download_dir_valid(save_dir):
        errConsole.print(
            f"Download directory: [bold red]{save_dir}[/bold red] is not a valid directory to download the mp3 to"
        )
        sys.exit(-1)
    elif not v.file_exists(filePath):
        errConsole.print(
            f"List of youtube links : [bold red]{filePath}[/bold red] is not a valid file"
        )
        sys.exit(1)
    else:
        links: list[str] = fm.readLinksFromFile(filePath)
        for link in links:
            console.print(
                f"\nWorking on [bold green]{printer.linkString(link, link)}[/bold green]n"
            )
            du.download_mp3_to_dir(link, save_dir)
        console.print("Done")

        sys.exit(0)


if __name__ == "__main__":
    ytos()
