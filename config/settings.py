"""
Data Downloader central configuration
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

from pathlib import Path

# ============================================================
# PROJECT INFO
# ============================================================

PROJECT_NAME = "Data Downloader"
VERSION = "v1.8.0"
AUTHOR = "Shadow-TermDev"
AUTHOR_TITLE = "The Termux Lord"
WEBSITE = "Shadow-TermDev.github.io"
REPOSITORY = "github.com/Shadow-TermDev/Data_Downloader"
LICENSE = "MIT"

# ============================================================
# SYSTEM PATHS
# ============================================================

# Android storage base path
STORAGE_BASE = Path("/storage/emulated/0")

# Output directories
VIDEOS_DIR = STORAGE_BASE / "Movies" / "Videos_Downloader"
AUDIO_DIR = STORAGE_BASE / "Music" / "Music_Downloader"
IMAGES_DIR = STORAGE_BASE / "Pictures" / "Picture_Downloader"

# Project directories
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_FILE = ASSETS_DIR / "config.json"
HELP_FILE = ASSETS_DIR / "help.json"

# ============================================================
# DOWNLOAD SETTINGS
# ============================================================

# Supported formats
VIDEO_FORMATS = ["mp4", "mkv", "avi", "mov", "webm"]
AUDIO_FORMATS = ["mp3", "wav", "ogg", "aac", "flac", "m4a"]
IMAGE_FORMATS = ["png", "jpg", "jpeg", "webp", "bmp", "gif", "tiff", "ico"]

# Video qualities
VIDEO_QUALITIES = {
    "4k": "2160p",
    "1080p": "1080p",
    "720p": "720p",
    "480p": "480p",
    "360p": "360p"
}

# Audio bitrates
AUDIO_BITRATES = {
    "low": "128k",
    "medium": "256k",
    "high": "320k"
}

# ============================================================
# CONVERSION SETTINGS
# ============================================================

# Real extensions per format
AUDIO_EXTENSIONS = {
    "mp3": "mp3",
    "wav": "wav",
    "flac": "flac",
    "ogg": "ogg",
    "m4a": "m4a",
    "aac": "m4a"  # AAC is stored as M4A
}

# Formats with cover/thumbnail support
FORMATS_WITH_COVER = {"mp3", "flac", "m4a", "aac", "ogg"}

# ============================================================
# ENHANCEMENT SETTINGS
# ============================================================

# Image scale factors
IMAGE_SCALE_FACTORS = {
    "low": 1.2,
    "medium": 1.5,
    "high": 2.0
}

# Video resolutions
VIDEO_RESOLUTIONS = {
    "720p": "1280x720",
    "1080p": "1920x1080",
    "4k": "3840x2160"
}

# ============================================================
# UI SETTINGS
# ============================================================

# ANSI colors
COLORS = {
    "primary": "\033[95m",      # Magenta
    "secondary": "\033[96m",    # Cyan
    "success": "\033[92m",      # Green
    "warning": "\033[93m",      # Yellow
    "error": "\033[91m",        # Red
    "info": "\033[94m",         # Blue
    "reset": "\033[0m"
}

# Title fonts (pyfiglet)
TITLE_FONTS = {
    "main": "slant",
    "subtitle": "small"
}

# Box/border width
BOX_WIDTH = 52

# ============================================================
# ANIMATION SETTINGS
# ============================================================

TRANSITION_TYPES = ["Fade", "Slide", "Zoom", "Wipe", "Flash"]
DEFAULT_TRANSITION = "Fade"
ANIMATION_SPEED = 0.05

# ============================================================
# SYSTEM MESSAGES
# ============================================================

MESSAGES = {
    "welcome": f"{PROJECT_NAME} {VERSION}",
    "goodbye": "Thanks for using Data Downloader!",
    "invalid_option": "Invalid option",
    "empty_input": "Empty input. Please enter a value",
    "file_not_found": "File not found",
    "download_success": "Download completed",
    "conversion_success": "Conversion completed",
    "enhancement_success": "Enhancement completed",
    "error_occurred": "An error occurred",
    "press_enter": "Press Enter to continue...",
    "processing": "Processing...",
    "downloading": "Downloading...",
    "converting": "Converting...",
    "saving": "Saving..."
}

# ============================================================
# CONFIGURACIÓN DE LOGGING (para futuras versiones)
# ============================================================

LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "data_downloader.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def create_directories():
    """Create required directories if missing"""
    directories = [VIDEOS_DIR, AUDIO_DIR, IMAGES_DIR, ASSETS_DIR]
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            print(f"⚠️  Could not create directory: {directory}")

def get_output_dir(file_type: str) -> Path:
    """
    Return output directory by file type
    
    Args:
        file_type: 'video', 'audio' or 'image'
    
    Returns:
        Path object of the matching directory
    """
    mapping = {
        "video": VIDEOS_DIR,
        "audio": AUDIO_DIR,
        "image": IMAGES_DIR
    }
    return mapping.get(file_type, VIDEOS_DIR)

def is_valid_format(format_str: str, file_type: str) -> bool:
    """
    Check if a format is valid for the file type
    
    Args:
        format_str: Format to validate (e.g. 'mp4', 'mp3')
        file_type: File type ('video', 'audio', 'image')
    
    Returns:
        True if the format is valid
    """
    format_map = {
        "video": VIDEO_FORMATS,
        "audio": AUDIO_FORMATS,
        "image": IMAGE_FORMATS
    }
    return format_str.lower() in format_map.get(file_type, [])

# Inicializar directorios al importar el módulo
create_directories()
