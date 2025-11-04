# YouTube Image Extractor

![Generic badge](https://img.shields.io/badge/python-3.10-blue.svg) [![Twitter](https://img.shields.io/badge/Twitter-@pulsecode-blue.svg)](https://twitter.com/pulsecode)

Downloads YouTube video and extracts video frames as a collection of image files.

Files created by the script:

- Unique directory ID to store downloaded video and image files.

## Requirements

- [ffmpeg](https://ffmpeg.org/download.html)
  - Windows: `winget install Gyan.FFmpeg` or `scoop install ffmpeg`
  - Ubuntu: `sudo apt update && sudo apt install ffmpeg`
  - Mac: `brew install ffmpeg`
- [yt-dlp](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation)
  - `python -m pip install yt-dlp -U`

## Installation

1. Clone the repository:

        git clone <https://github.com/dfirsec/yt_image_extractor.git>

2. Change to the project directory:

        cd yt_image_extractor

3. Install dependencies and create environment:

        uv venv
        uv sync

4. Run the script:

        uv run yt_image_extractor.py <video_url> [options]


## Usage

    ██╗   ██╗  ██╗   ███████╗
    ╚██╗ ██╔╝  ██║   ██╔════╝
     ╚████╔╝   ██║   █████╗
      ╚██╔╝    ██║   ██╔══╝
       ██║     ██║   ███████╗
       ╚═╝     ╚═╝   ╚══════╝

     YouTube Image Extractor

     usage: yt_image_extractor.py [-h] [-s] [-f [N]] [--start-time START_TIME] [--end-time END_TIME] url

## Arguments

- `url`: The YouTube URL to process.
- `-h, --help`: Display the help message.
- `-s, --small`: Download the video in the lowest available quality.
- `-f [N]`: Specify the number of frames to skip before capturing an image (default is 30, i.e., capture 1 image every 30 frames).
- `--start-time`: Define the video start time for image extraction (format: MM:SS).
- `--end-time`: Define the video end time for image extraction (format: MM:SS).

### Example Usage

Download the entire video with default options:

    uv run yt_image_extractor.py <video_url>

Download in low quality:

    uv run yt_image_extractor.py -s <video_url>

Capture one image every 60 frames:

    uv run yt_image_extractor.py -f 60 <video_url>

Extract images from a specific timeframe:

    uv run yt_image_extractor.py --start-time 01:10 --end-time 01:35 <video_url>

> Note: Replace <video_url> with the actual YouTube video URL you want to process.

## License

This program is licensed under the MIT License. For more information, please see the `LICENSE` file.
