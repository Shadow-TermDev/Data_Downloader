"""
Helpers and utility functions
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import shutil
import json
import sys
from pathlib import Path
from colorama import Fore, Style

from config.settings import ASSETS_DIR
from src.utils.animations import mostrar_cursor, ocultar_cursor


def limpiar_pantalla():
    """Clear the terminal screen (scrollback-safe, TokenHub-style)"""
    try:
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
    except Exception:
        pass
    os.system("cls" if os.name == "nt" else "clear")


def centrar_texto(texto: str) -> str:
    """
    Center text in the terminal
    
    Args:
        texto: Text to center
        
    Returns:
        Centered text with padding
    """
    try:
        ancho = shutil.get_terminal_size().columns
    except Exception:
        ancho = 80
    
    return texto.center(ancho)


def pausar(mensaje: str = None, mostrar: bool = True):
    """
    Pause execution until the user presses Enter
    
    Args:
        mensaje: Custom message (optional)
        mostrar: If True, show cursor before pausing
    """
    if mostrar:
        mostrar_cursor()
    
    msg = mensaje or "\n🔹 Press Enter to continue..."
    input(Fore.CYAN + msg + Style.RESET_ALL)
    ocultar_cursor()


def mostrar_progreso(actual: int, total: int, prefijo: str = "Progress"):
    """
    Show a progress bar
    
    Args:
        actual: Current value
        total: Total value
        prefijo: Text before the bar
    """
    if total <= 0:
        return
    
    porcentaje = (actual / total) * 100
    barra_ancho = 30
    bloques = int((porcentaje / 100) * barra_ancho)
    barra = "█" * bloques + "░" * (barra_ancho - bloques)
    
    print(f"\r{Fore.CYAN}{prefijo}: [{barra}] {porcentaje:.1f}%", end="", flush=True)


def formatear_bytes(bytes_size: int) -> str:
    """
    Format bytes into a readable unit
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted string (e.g. "1.5 MB")
    """
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unidad}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def validar_url(url: str) -> tuple:
    """
    Validate URL format and return details
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple (is_valid, error_message)
    """
    import re
    
    if not url:
        return (False, "URL cannot be empty")
    
    if not url.startswith(('http://', 'https://')):
        return (False, "URL must start with http:// or https://")
    
    patron = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not patron.match(url):
        return (False, "URL format is not valid")
    
    return (True, None)


def validar_url_corta(url: str) -> bool:
    """
    Quickly validate a URL (no detailed message)
    
    Args:
        url: URL to validate
        
    Returns:
        True if it looks valid
    """
    if not url:
        return False
    
    url_lower = url.lower().strip()
    return (
        url_lower.startswith('http://') or 
        url_lower.startswith('https://')
    ) and len(url) > 10


def mostrar_ayuda(opcion: str):
    """
    Show help for a specific option
    
    Args:
        opcion: Help option number
    """
    from pyfiglet import Figlet
    
    # Load help from JSON
    ayuda_file = ASSETS_DIR / "help.json"
    
    if not ayuda_file.exists():
        print(Fore.RED + "\n❌ Help file not found")
        pausar()
        return
    
    try:
        with open(ayuda_file, 'r', encoding='utf-8') as f:
            ayuda_data = json.load(f)
    except Exception as e:
        print(Fore.RED + f"\n❌ Error loading help: {e}")
        pausar()
        return
    
    ayuda = ayuda_data.get(opcion, {
        "title": "Help unavailable",
        "titulo": "Help unavailable",
        "message": "Help for this option is not available.",
        "mensaje": "Help for this option is not available."
    })

    # Back-compat: support both English and legacy Spanish keys
    titulo = ayuda.get("title") or ayuda.get("titulo", "Help")
    mensaje = ayuda.get("message") or ayuda.get("mensaje", "")
    pasos = ayuda.get("steps") or ayuda.get("pasos", [])
    consejos = ayuda.get("tips") or ayuda.get("consejos", [])
    
    limpiar_pantalla()
    
    # Title
    figlet = Figlet(font="slant")
    titulo_ascii = figlet.renderText(titulo)
    for linea in titulo_ascii.splitlines():
        print(Fore.YELLOW + centrar_texto(linea))
    
    print(Fore.CYAN + centrar_texto("USER MANUAL\n"))
    print(Fore.MAGENTA + "═" * 80)
    
    # Message
    print(Fore.WHITE + f"\n{mensaje}\n")
    
    # Steps if present
    if pasos:
        print(Fore.CYAN + "📝 Steps:\n")
        for i, paso in enumerate(pasos, 1):
            print(Fore.GREEN + f"  {i}. {paso}")
    
    # Tips if present
    if consejos:
        print(Fore.YELLOW + "\n💡 Tips:\n")
        for consejo in consejos:
            print(Fore.WHITE + f"  • {consejo}")
    
    print(Fore.MAGENTA + "\n" + "═" * 80)
    pausar()


def crear_directorio_seguro(ruta: Path) -> bool:
    """
    Safely create a directory
    
    Args:
        ruta: Directory path
        
    Returns:
        True if created or already existed
    """
    try:
        ruta.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        print(Fore.RED + f"❌ No permission to create: {ruta}")
        return False
    except Exception as e:
        print(Fore.RED + f"❌ Error creating directory: {e}")
        return False


def verificar_dependencias() -> dict:
    """
    Check that required dependencies are installed
    
    Returns:
        Dict with status of each dependency
    """
    import subprocess
    
    dependencias = {
        "ffmpeg": False,
        "yt-dlp": False,
        "python": True  # Already running if this executes
    }
    
    # Check FFmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      capture_output=True, 
                      timeout=5)
        dependencias["ffmpeg"] = True
    except:
        pass
    
    # Check yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"], 
                      capture_output=True, 
                      timeout=5)
        dependencias["yt-dlp"] = True
    except:
        pass
    
    return dependencias


def mostrar_banner_inicio():
    """Show a welcome banner on startup"""
    import pyfiglet
    from config.settings import PROJECT_NAME, VERSION, WEBSITE
    
    limpiar_pantalla()
    
    titulo = pyfiglet.figlet_format(PROJECT_NAME, font="slant")
    for linea in titulo.splitlines():
        print(Fore.CYAN + centrar_texto(linea))
    
    print(Fore.YELLOW + centrar_texto(f"Version {VERSION}"))
    print(Fore.MAGENTA + centrar_texto(f"🌐 {WEBSITE}"))
    print(Fore.WHITE + centrar_texto("Press Enter to continue..."))
    
    input()


# English aliases (new API) — keep Spanish names for backward compat
clear_screen = limpiar_pantalla
center_text = centrar_texto
pause = pausar
show_help = mostrar_ayuda
format_bytes = formatear_bytes
