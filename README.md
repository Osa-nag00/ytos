# ytos — YouTube to Spotify

CLI tool that downloads YouTube videos as MP3s to a local Spotify folder.

Given a text file of YouTube URLs (one per line), it downloads each video's audio, converts it to MP3, sets metadata (title, artist, album art), and saves the file to a directory of your choice.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- [ffmpeg](https://ffmpeg.org/) (must be in your PATH)

## Setup

```bash
uv sync
```

## Usage

```bash
uv run ytos.py -f <links-file> -d <output-dir>
```

| Flag | Description |
|------|-------------|
| `-f`, `--file` | Path to a `.txt` file with YouTube URLs, one per line |
| `-d`, `--save-dir` | Directory where MP3s will be saved |

**Example:**

```bash
uv run ytos.py -f links.txt -d ~/Music/Spotify
```

## links.txt format

```
https://www.youtube.com/watch?v=...
https://www.youtube.com/watch?v=...
```
