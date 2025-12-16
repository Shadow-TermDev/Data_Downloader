"""
Configuración centralizada del proyecto Data Downloader
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
from pathlib import Path

# ============================================================
# INFORMACIÓN DEL PROYECTO
# ============================================================

PROJECT_NAME = "Data Downloader"
VERSION = "v1.4.4"
AUTHOR = "Shadow-TermDev"
AUTHOR_TITLE = "El Lord de Termux"
WEBSITE = "Shadow-TermDev.github.io"
REPOSITORY = "github.com/Shadow-TermDev/Data_Downloader"
LICENSE = "MIT"

# ============================================================
# RUTAS DEL SISTEMA
# ============================================================

# Ruta base del almacenamiento Android
STORAGE_BASE = Path("/storage/emulated/0")

# Directorios de salida
VIDEOS_DIR = STORAGE_BASE / "VMovies" / "Videos_Downloader"
AUDIO_DIR = STORAGE_BASE / "Music" / "Music_Downloader"
IMAGES_DIR = STORAGE_BASE / "Pictures" / "Picture_Downloader"

# Directorio del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_FILE = ASSETS_DIR / "config.json"
HELP_FILE = ASSETS_DIR / "help.json"

# ============================================================
# CONFIGURACIÓN DE DESCARGA
# ============================================================

# Formatos soportados
VIDEO_FORMATS = ["mp4", "mkv", "avi", "mov", "webm"]
AUDIO_FORMATS = ["mp3", "wav", "ogg", "aac", "flac", "m4a"]
IMAGE_FORMATS = ["png", "jpg", "jpeg", "webp", "bmp", "gif", "tiff", "ico"]

# Calidades de video
VIDEO_QUALITIES = {
    "4k": "2160p",
    "1080p": "1080p",
    "720p": "720p",
    "480p": "480p",
    "360p": "360p"
}

# Bitrates de audio
AUDIO_BITRATES = {
    "low": "128k",
    "medium": "256k",
    "high": "320k"
}

# ============================================================
# CONFIGURACIÓN DE CONVERSIÓN
# ============================================================

# Extensiones reales por formato
AUDIO_EXTENSIONS = {
    "mp3": "mp3",
    "wav": "wav",
    "flac": "flac",
    "ogg": "ogg",
    "m4a": "m4a",
    "aac": "m4a"  # AAC se guarda como M4A
}

# Formatos con soporte de portada/thumbnail
FORMATS_WITH_COVER = {"mp3", "flac", "m4a", "aac", "ogg"}

# ============================================================
# CONFIGURACIÓN DE MEJORA
# ============================================================

# Factores de escala para imágenes
IMAGE_SCALE_FACTORS = {
    "low": 1.2,
    "medium": 1.5,
    "high": 2.0
}

# Resoluciones de video
VIDEO_RESOLUTIONS = {
    "720p": "1280x720",
    "1080p": "1920x1080",
    "4k": "3840x2160"
}

# ============================================================
# CONFIGURACIÓN DE INTERFAZ
# ============================================================

# Colores ANSI
COLORS = {
    "primary": "\033[95m",      # Magenta
    "secondary": "\033[96m",    # Cyan
    "success": "\033[92m",      # Green
    "warning": "\033[93m",      # Yellow
    "error": "\033[91m",        # Red
    "info": "\033[94m",         # Blue
    "reset": "\033[0m"
}

# Fuentes para títulos (pyfiglet)
TITLE_FONTS = {
    "main": "slant",
    "subtitle": "small"
}

# Ancho de cuadros/bordes
BOX_WIDTH = 52

# ============================================================
# CONFIGURACIÓN DE ANIMACIONES
# ============================================================

TRANSITION_TYPES = ["Fade", "Slide", "Zoom", "Wipe", "Flash"]
DEFAULT_TRANSITION = "Fade"
ANIMATION_SPEED = 0.05

# ============================================================
# MENSAJES DEL SISTEMA
# ============================================================

MESSAGES = {
    "welcome": f"{PROJECT_NAME} {VERSION}",
    "goodbye": "¡Gracias por usar Data Downloader!",
    "invalid_option": "Opción no válida. Inténtalo de nuevo.",
    "empty_input": "Entrada vacía. Por favor ingresa un valor.",
    "file_not_found": "Archivo no encontrado.",
    "download_success": "Descarga completada con éxito!",
    "conversion_success": "Conversión completada con éxito!",
    "enhancement_success": "Mejora completada con éxito!",
    "error_occurred": "Ocurrió un error inesperado.",
    "press_enter": "Presiona Enter para continuar..."
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
    """Crea los directorios necesarios si no existen"""
    directories = [VIDEOS_DIR, AUDIO_DIR, IMAGES_DIR, ASSETS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_output_dir(file_type: str) -> Path:
    """
    Retorna el directorio de salida según el tipo de archivo
    
    Args:
        file_type: 'video', 'audio' o 'image'
    
    Returns:
        Path object del directorio correspondiente
    """
    mapping = {
        "video": VIDEOS_DIR,
        "audio": AUDIO_DIR,
        "image": IMAGES_DIR
    }
    return mapping.get(file_type, VIDEOS_DIR)

def is_valid_format(format_str: str, file_type: str) -> bool:
    """
    Verifica si un formato es válido para el tipo de archivo
    
    Args:
        format_str: Formato a validar (ej: 'mp4', 'mp3')
        file_type: Tipo de archivo ('video', 'audio', 'image')
    
    Returns:
        True si el formato es válido
    """
    format_map = {
        "video": VIDEO_FORMATS,
        "audio": AUDIO_FORMATS,
        "image": IMAGE_FORMATS
    }
    return format_str.lower() in format_map.get(file_type, [])

# Inicializar directorios al importar el módulo
create_directories()
