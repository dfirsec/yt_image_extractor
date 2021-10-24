import argparse
import sys
import uuid
from pathlib import Path

import cv2
import youtube_dl

# Base directory path
parent = Path(__file__).resolve().parent


class VideoProcessor:
    def __init__(self):
        self.video = parent.joinpath(str(uuid.uuid1()))
        self.images = self.video.joinpath("Images")

    def download_video(self, url, small=None, fps=None):
        try:
            if small:
                ydl_opts = {"format": "worst", "outtmpl": f"{self.video}/%(title)s.%(ext)s"}
            else:
                ydl_opts = {"format": "best", "outtmpl": f"{self.video}/%(title)s.%(ext)s"}

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except youtube_dl.utils.DownloadError:
            sys.exit()
        else:
            self.video.mkdir(parents=True, exist_ok=True)
            self.images.mkdir(parents=True, exist_ok=True)
            self.extract_images(fps)

    def extract_images(self, fps):
        video_file = "".join([str(x) for x in self.video.iterdir() if x.is_file()])
        video_capture = cv2.VideoCapture(video_file)
        length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        success, image = video_capture.read()
        count = 0

        while success:
            success, image = video_capture.read()
            if not success:
                break
            try:
                if count % fps == 0:
                    filename = self.images.joinpath(f"frame_{str(count)}.jpg")
                    cv2.imwrite(str(filename), image)
                    print(f"[processing frame] {count}/{length}", end="\r")
                count += 1
            except KeyboardInterrupt:
                sys.exit()
        print("\n[completed]")


def check_value(arg):
    num = int(arg)
    if num <= 0:
        raise argparse.ArgumentTypeError("argument must be a positive integer value")
    return num


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="youtube url")
    parser.add_argument(
        "-s", "--small", action="store_true", help="download lowest quality video (smaller size video)"
    )
    parser.add_argument(
        "-f",
        dest="fps",
        metavar="N",
        nargs="?",
        type=check_value,
        default=30,
        help="images to capture per frame (default is 30 = 1 image per 30 frames)",
    )
    args = parser.parse_args()

    vp = VideoProcessor()
    vp.download_video(args.url, args.small, args.fps)


if __name__ == "__main__":
    banner = r"""
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    | YouTube Frame/Image Extractor |
    +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    """
    print(banner)

    main()
