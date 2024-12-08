import sys
from rich.console import Console
import click
from ytos import printer
from ytos import validator as v


@click.command()
@click.option(
    "-l", "--link", "link", required=True, type=click.STRING, help="Link to youtube video that will be downloaded"
)
@click.option(
    "-d", "--save-dir", "save_dir", required=True, type=click.STRING, help="Path to where the mp3 will be downloaded"
)
def ytos(link: str, save_dir: str) -> None:
    """
    Youtube to spotify script will take a given Youtube video URL and download the mpo3
    of the specified video to a Spotify local folder
    """
    console = Console()
    errConsole = Console(stderr=True)

    entryMsg: str = (
        f"Attempting to download [bold green]{printer.linkString(link, link)}[/bold green] to [italic green]{printer.linkString(save_dir,save_dir)}[/italic green]"
    )

    console.print(entryMsg + "\n")

    if not v.is_valid_url(link):
        errConsole.print(f"Youtube URL: [bold red]{link}[/bold red] is malformed and not a valid URL")
        sys.exit(-1)
    elif not v.is_download_dir_valid(save_dir):
        errConsole.print(
            f"Download directory: [bold red]{save_dir}[/bold red] is not a valid directory to download the mp3 to"
        )
        sys.exit(-1)
    # TODO: handle the rest of this later, need to figure out how functionality should be split
    # else:
    # download_mp3_to_dir(youtube_url, download_dir)

    pass


if __name__ == "__main__":
    ytos()
