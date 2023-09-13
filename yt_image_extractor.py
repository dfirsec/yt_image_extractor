"""Downloads YouTube video and extracts video frames as a collection of image files."""

import argparse

from utils import check_value
from utils import is_ffmpeg_installed
from video_processor import VideoProcessor


def main() -> None:
    """Argument parser/main function."""
    fps_rate = 30
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="youtube url")
    parser.add_argument(
        "-s",
        "--small",
        action="store_true",
        help="download lowest quality video (smaller size video)",
    )
    parser.add_argument(
        "-f",
        dest="fps",
        metavar="N",
        nargs="?",
        type=check_value,
        default=fps_rate,
        help="images to capture per frame (default is 30 = 1 image per 30 frames)",
    )
    parser.add_argument(
        "--start-time",
        help="start time for video timeframe (format: HH:MM:SS)",
    )
    parser.add_argument(
        "--end-time",
        help="end time for video timeframe (format: HH:MM:SS)",
    )
    args = parser.parse_args()

    vidp = VideoProcessor()

    if args.start_time and args.end_time:
        vidp.video_timeframe_downloader(args.url, args.start_time, args.end_time, args.fps)
    else:
        vidp.download_video(args.url, args.small, args.fps)


if __name__ == "__main__":
    BANNER = """
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    | YouTube Frame/Image Extractor |
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    """
    print(BANNER)
    if not is_ffmpeg_installed():
        print(
            "Error: ffmpeg is not installed or not available in the system PATH. "
            "Please install it before proceeding.",
        )
    main()
