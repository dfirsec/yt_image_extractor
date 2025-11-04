"""Utility functions for ytdl_img_extractor."""

import platform
import string
import subprocess

from rich.panel import Panel
from rich.text import Text


class InvalidFPSValueError(ValueError):
    """Custom exception for invalid fps value."""

    message = "Argument must be a positive integer value"


def is_ffmpeg_installed() -> bool:
    """Check if ffmpeg is installed."""
    try:
        # Get ffmpeg version info
        # stdout and stderr prevent the output from being printed
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False
    return True


def get_ffmpeg_install_instructions() -> Panel:
    """Installation instructions for ffmpeg."""
    system = platform.system().lower()

    instructions = {
        "windows": """
To install ffmpeg on Windows:

1. Using WinGet (recommended):
   - Run: winget install ffmpeg -s winget

2. Manual installation:
   - Download from https://ffmpeg.org/download.html
   - Extract the ZIP file
   - Add the bin folder to your system PATH
   - Restart your terminal/IDE after installation

After installing, run the program again to verify the installation.""",
        "darwin": """
To install ffmpeg on macOS:

1. Using Homebrew (recommended):
   - Open Terminal
   - Run: brew install ffmpeg

2. Using MacPorts:
   - Run: sudo port install ffmpeg

After installing, run the program again to verify the installation.""",
        "linux": """
To install ffmpeg on Linux:

Ubuntu/Debian:
- Run: sudo apt update && sudo apt install ffmpeg

Fedora:
- Run: sudo dnf install ffmpeg

Arch Linux:
- Run: sudo pacman -S ffmpeg

After installing, run the program again to verify the installation.""",
    }

    default_instructions = f"""
To install ffmpeg on {platform.system()}:

1. Visit https://ffmpeg.org/download.html
2. Follow the installation instructions for your system
3. Ensure ffmpeg is added to your system PATH
4. Restart your terminal/IDE after installation

After installing, run the program again to verify the installation."""

    instruction_text = Text(
        instructions.get(system, default_instructions),
        style="yellow",
    )

    return Panel(
        instruction_text,
        title="FFmpeg Installation Instructions",
        border_style="blue",
        padding=(1, 2),
    )


def check_value(arg: str) -> int:
    """Check fps value.

    Raises:
        InvalidFPSValueError: if value is not a positive integer
    """
    num = int(arg)
    if num <= 0:
        raise InvalidFPSValueError
    return num


def restrict_to_ascii(title: str) -> str:
    """Restrict the title to ASCII characters and replace spaces with underscores."""
    return "".join(char if char.isascii() and char != " " and char not in string.punctuation else "_" for char in title)
