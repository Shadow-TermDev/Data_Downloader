"""
Utilidades y funciones auxiliares
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import shutil
import json
from pathlib import Path
from colorama import Fore, Style

from config.settings import ASSETS_DIR, MESSAGES
from src.utils.animations import mostrar_cursor, ocultar_cursor


def limpiar_pantalla():
    """Limpia la pantalla de la terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def centrar_texto(texto: str) -> str:
    """
    Centra un texto en la terminal
    
    Args:
        texto: Texto a centrar
        
    Returns:
        Texto centrado con espacios
    """
    try:
        ancho = shutil.get_terminal_size().columns
    except:
        ancho = 80
    
    return texto.center(ancho)


def pausar(mensaje: str = None, mostrar: bool = True):
    """
    Pausa la ejecución hasta que el usuario presione Enter
    
    Args:
        mensaje: Mensaje personalizado (opcional)
        mostrar: Si True muestra el cursor antes de pausar
    """
    if mostrar:
        mostrar_cursor()
    
    msg = mensaje or "\n🔹 Presiona Enter para continuar..."
    input(Fore.CYAN + msg + Style.RESET_ALL)
    ocultar_cursor()


def mostrar_progreso(actual: int, total: int, prefijo: str = "Progreso"):
    """
    Muestra una barra de progreso
    
    Args:
        actual: Valor actual
        total: Valor total
        prefijo: Texto antes de la barra
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
    Formatea bytes a una unidad legible
    
    Args:
        bytes_size: Tamaño en bytes
        
    Returns:
        String formateado (ej: "1.5 MB")
    """
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unidad}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def validar_url(url: str) -> tuple:
    """
    Valida que una URL tenga formato correcto y retorna detalles
    
    Args:
        url: URL a validar
        
    Returns:
        Tupla (es_valida, mensaje_error)
    """
    import re
    
    if not url:
        return (False, "La URL no puede estar vacía")
    
    if not url.startswith(('http://', 'https://')):
        return (False, "La URL debe comenzar con http:// o https://")
    
    patron = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not patron.match(url):
        return (False, "El formato de la URL no es válido")
    
    return (True, None)


def validar_url_corta(url: str) -> bool:
    """
    Valida rápidamente si es una URL (sin mensaje detallado)
    
    Args:
        url: URL a validar
        
    Returns:
        True si parece válida
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
    Muestra la ayuda para una opción específica
    
    Args:
        opcion: Número de opción de ayuda
    """
    from pyfiglet import Figlet
    
    # Cargar ayuda desde JSON
    ayuda_file = ASSETS_DIR / "help.json"
    
    if not ayuda_file.exists():
        print(Fore.RED + "\n❌ Archivo de ayuda no encontrado")
        pausar()
        return
    
    try:
        with open(ayuda_file, 'r', encoding='utf-8') as f:
            ayuda_data = json.load(f)
    except Exception as e:
        print(Fore.RED + f"\n❌ Error al cargar ayuda: {e}")
        pausar()
        return
    
    ayuda = ayuda_data.get(opcion, {
        "titulo": "Ayuda no disponible",
        "mensaje": "La ayuda para esta opción no está disponible."
    })
    
    limpiar_pantalla()
    
    # Título
    figlet = Figlet(font="slant")
    titulo_ascii = figlet.renderText(ayuda["titulo"])
    for linea in titulo_ascii.splitlines():
        print(Fore.YELLOW + centrar_texto(linea))
    
    print(Fore.CYAN + centrar_texto("📖 MANUAL DE USUARIO 📖\n"))
    print(Fore.MAGENTA + "═" * 80)
    
    # Mensaje
    print(Fore.WHITE + f"\n{ayuda['mensaje']}\n")
    
    # Pasos si existen
    if "pasos" in ayuda:
        print(Fore.CYAN + "📝 Pasos a seguir:\n")
        for i, paso in enumerate(ayuda["pasos"], 1):
            print(Fore.GREEN + f"  {i}. {paso}")
    
    # Consejos si existen
    if "consejos" in ayuda:
        print(Fore.YELLOW + f"\n💡 Consejos:\n")
        for consejo in ayuda["consejos"]:
            print(Fore.WHITE + f"  • {consejo}")
    
    print(Fore.MAGENTA + "\n" + "═" * 80)
    pausar()


def crear_directorio_seguro(ruta: Path) -> bool:
    """
    Crea un directorio de forma segura
    
    Args:
        ruta: Path del directorio
        
    Returns:
        True si se creó o ya existía
    """
    try:
        ruta.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        print(Fore.RED + f"❌ Sin permisos para crear: {ruta}")
        return False
    except Exception as e:
        print(Fore.RED + f"❌ Error al crear directorio: {e}")
        return False


def verificar_dependencias() -> dict:
    """
    Verifica que las dependencias necesarias estén instaladas
    
    Returns:
        Diccionario con estado de cada dependencia
    """
    import subprocess
    
    dependencias = {
        "ffmpeg": False,
        "yt-dlp": False,
        "python": True  # Ya está si ejecuta esto
    }
    
    # Verificar FFmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      capture_output=True, 
                      timeout=5)
        dependencias["ffmpeg"] = True
    except:
        pass
    
    # Verificar yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"], 
                      capture_output=True, 
                      timeout=5)
        dependencias["yt-dlp"] = True
    except:
        pass
    
    return dependencias


def mostrar_banner_inicio():
    """Muestra un banner de bienvenida al iniciar"""
    import pyfiglet
    from config.settings import PROJECT_NAME, VERSION, WEBSITE
    
    limpiar_pantalla()
    
    titulo = pyfiglet.figlet_format(PROJECT_NAME, font="slant")
    for linea in titulo.splitlines():
        print(Fore.CYAN + centrar_texto(linea))
    
    print(Fore.YELLOW + centrar_texto(f"Versión {VERSION}"))
    print(Fore.MAGENTA + centrar_texto(f"🌐 {WEBSITE}"))
    print(Fore.WHITE + centrar_texto("Presiona Enter para continuar..."))
    
    input()
