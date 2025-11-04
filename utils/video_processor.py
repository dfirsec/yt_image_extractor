"""Video Processor."""

import subprocess
import sys
import uuid
from pathlib import Path

from rich.console import Console
from yt_dlp import YoutubeDL
from yt_dlp import utils

from utils.helpers import restrict_to_ascii

console = Console()
parent = Path(__file__).resolve().parent.parent


class VideoProcessor:
    """Main processor."""

    def __init__(self: "VideoProcessor") -> None:
        """Setup video and image directories."""
        self.video_dir = parent.joinpath(str(uuid.uuid4()))  # default to a random directory name
        self.images_dir = None
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, Like Gecko) Chrome/48.0.2564.82 Safari/537.36 Edge/14.14316"
        )

    def create_directories(self: "VideoProcessor", video_title: str) -> None:
        """Create video and image directories based on video filename."""
        self.video_dir = parent.joinpath(video_title or str(uuid.uuid4()))
        self.images_dir = self.video_dir.joinpath("Images")
        self.video_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def get_video_title(self: "VideoProcessor", url: str) -> str:
        """Get video title from YouTube URL."""
        ydl_opts = {
            "quiet": True,
            "no-warnings": True,
            "logger": None,
            "no-progress": True,
        }
        try:
            with console.status("[sea_green2]Getting video title..."), YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info is None or "title" not in info:
                    return "video"
                console.print(f"  Video Title: '{info['title']}'", style="gold1")
                return restrict_to_ascii(info["title"])
        except utils.DownloadError:
            print("Error: Invalid URL")
            sys.exit()
        except KeyboardInterrupt:
            print("Exited: KeyboardInterrupt")
            sys.exit()

    def download_video(self: "VideoProcessor", url: str, small: bool | None, fps: int) -> None:
        """Download video and extract images."""
        video_title = self.get_video_title(url)
        self.create_directories(video_title)

        ydl_opts = {
            "format": "worst" if small else "22/18/best[height<=720]",
            "outtmpl": f"{self.video_dir}/%(title)s.%(ext)s",
            "restrict-filenames": True,
            "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
            "merge_output_format": "mp4",
            "sort": "res:2160,fps",
            "quiet": True,
            "no-warnings": True,
            "logger": None,
            "no-progress": True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                self.video_filename = ydl.prepare_filename(info_dict)

        except utils.DownloadError:
            print("Error: Invalid URL")
            sys.exit(1)
        except KeyboardInterrupt:
            print("Exited: KeyboardInterrupt")
            sys.exit(1)
        else:
            self.extract_images(fps)

    def video_timeframe_downloader(
        self: "VideoProcessor",
        url: str,
        start: str,
        end: str,
        fps: int,
        *args: str | list[str],
    ) -> None:
        """Download a video from YouTube and extract a specific timeframe."""
        video_title = self.get_video_title(url)
        self.create_directories(video_title)

        external_downloader_args = f'-ss {start} -to {end} -user_agent "{self.user_agent}"'

        yt_dlp_args = [
            "yt-dlp",
            "-q",
            "-4",
            "--no-warnings",
            "--no-progress",
            "--no-playlist",
            "-f",
            "22/18/best[height<=720]",
            "--downloader",
            "ffmpeg",
            "--downloader-args",
            f"ffmpeg_i:{external_downloader_args}",
            "--restrict-filenames",
            "--output",
            str(self.video_dir.joinpath(f"{video_title}.%(ext)s")),
            url,
            *args,
        ]

        with console.status("[sea_green2]Downloading video..."):
            result = subprocess.call(
                yt_dlp_args,
                stdout=subprocess.DEVNULL,  # Redirect standard output
                stderr=subprocess.DEVNULL,  # Redirect standard error
            )
        if result != 0:
            print("Error: Could not download the video with given timeframe.")
            sys.exit(1)

        self.video_filename = str(self.video_dir.joinpath(f"{video_title}.mp4"))
        self.extract_images(fps)

    def extract_images(self: "VideoProcessor", fps: int) -> None:
        """Extract frames from video using ffmpeg."""
        if not self.images_dir:
            print("Error: Image directory not properly initialized.")
            return

        video_filepath = "".join([str(vidobj) for vidobj in self.video_dir.iterdir() if vidobj.is_file()])
        if not video_filepath:
            print("Error: No video files found in the video directory.")
            return

        output_file_pattern = str(self.images_dir.joinpath("frame_%d.png"))
        command = [
            "ffmpeg",
            "-y",
            "-i",
            video_filepath,
            "-vf",
            f"fps={fps}",
            "-loglevel",
            "error",
            output_file_pattern,
        ]

        with console.status("[sea_green2]Extracting frames..."):
            process = subprocess.run(command, capture_output=True, text=True)  # noqa: PLW1510

            if "Error" in process.stderr:
                print("Error:", process.stderr)

            if process.stdout:
                print(process.stdout)

            if process.stderr:
                print("Error:", process.stderr)

        console.print("[sea_green2]  Done!")
