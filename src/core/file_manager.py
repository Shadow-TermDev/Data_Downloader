"""
File manager and on-device search
Author: Shadow-TermDev
"""

import os
from pathlib import Path
from typing import Optional
from colorama import Fore, Style

from config.settings import STORAGE_BASE, VIDEOS_DIR, AUDIO_DIR, IMAGES_DIR, MESSAGES
from src.utils.boxes import print_warning_box


def buscar_archivo(nombre_archivo: str, carpeta_base: Path = None) -> Optional[Path]:
    """
    Search for a file on device storage
    
    Args:
        nombre_archivo: File name to search
        carpeta_base: Base directory to start from
        
    Returns:
        File Path if found, None otherwise
    """
    if carpeta_base is None:
        carpeta_base = STORAGE_BASE
    
    print(Fore.CYAN + f"🔍 Searching for '{nombre_archivo}'...")
    
    def _coincidencia_exacta(carpeta: Path):
        try:
            for archivo in carpeta.rglob(nombre_archivo):
                if archivo.is_file():
                    return archivo
        except (PermissionError, OSError):
            return None
        return None
    
    # Search app download dirs first (faster)
    for directorio in (VIDEOS_DIR, AUDIO_DIR, IMAGES_DIR):
        if directorio.exists():
            encontrado = _coincidencia_exacta(directorio)
            if encontrado:
                print(Fore.GREEN + f"✅ File found: {encontrado}")
                return encontrado
    
    # Otherwise, general storage search
    encontrado = _coincidencia_exacta(carpeta_base)
    if encontrado:
        print(Fore.GREEN + f"✅ File found: {encontrado}")
        return encontrado
    
    # Partial-match search
    print(Fore.YELLOW + "No exact match found. Looking for similar files...")
    
    archivos_similares = []
    nombre_lower = nombre_archivo.lower()
    
    try:
        for archivo in carpeta_base.rglob("*"):
            if archivo.is_file() and nombre_lower in archivo.name.lower():
                archivos_similares.append(archivo)
                if len(archivos_similares) >= 5:  # Limitar a 5 resultados
                    break
    except (PermissionError, OSError):
        pass
    
    if archivos_similares:
        print(Fore.CYAN + "\n📁 Similar files found:")
        for i, archivo in enumerate(archivos_similares, 1):
            print(Fore.WHITE + f"  {i}. {archivo.name}")
            print(Fore.BLUE + f"     {archivo.parent}")
        
        from src.utils.animations import mostrar_cursor, ocultar_cursor
        mostrar_cursor()
        seleccion = input(Fore.YELLOW + "\nUse any of these? (1-5, Enter=none): ").strip()
        ocultar_cursor()
        
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(archivos_similares):
            archivo_seleccionado = archivos_similares[int(seleccion) - 1]
            print(Fore.GREEN + f"✅ Using: {archivo_seleccionado.name}")
            return archivo_seleccionado
    
    print(Fore.RED + f"❌ {MESSAGES['file_not_found']}: '{nombre_archivo}'")
    
    # Pause before going back
    from src.utils.helpers import pausar
    pausar()
    return None


def obtener_extension(ruta: Path) -> str:
    """
    Get a file extension without the dot
    
    Args:
        ruta: File path
        
    Returns:
        Lowercase extension (no dot)
    """
    return ruta.suffix.lstrip('.').lower()


def generar_nombre_salida(ruta_original: Path, sufijo: str = "_processed", nueva_extension: str = None) -> Path:
    """
    Build an output file name
    
    Args:
        ruta_original: Original file path
        sufijo: Suffix to append (default: "_procesado")
        nueva_extension: New extension if you want to change it
        
    Returns:
        New file path
    """
    nombre_base = ruta_original.stem
    extension = nueva_extension if nueva_extension else ruta_original.suffix
    
    if not extension.startswith('.'):
        extension = f'.{extension}'
    
    return ruta_original.parent / f"{nombre_base}{sufijo}{extension}"


def verificar_espacio_disponible(directorio: Path, tamano_requerido_mb: float = 100) -> bool:
    """
    Check for enough free disk space
    
    Args:
        directorio: Directory to check
        tamano_requerido_mb: Required space in MB
        
    Returns:
        True if there is enough space
    """
    try:
        stat = os.statvfs(directorio)
        espacio_libre_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
        
        if espacio_libre_mb < tamano_requerido_mb:
            print(Fore.YELLOW + f"⚠️ Low free space: {espacio_libre_mb:.1f} MB")
            return False
        
        return True
    except Exception:
        # If it can't be checked, assume there is space
        return True


def obtener_info_archivo(ruta: Path) -> dict:
    """
    Get detailed file info
    
    Args:
        ruta: File path
        
    Returns:
        Dict with file info
    """
    if not ruta.exists():
        return {}
    
    stat = ruta.stat()
    tamano_mb = stat.st_size / (1024 * 1024)
    
    return {
        "nombre": ruta.name,
        "ruta_completa": str(ruta),
        "extension": obtener_extension(ruta),
        "tamano_mb": round(tamano_mb, 2),
        "tamano_bytes": stat.st_size,
        "directorio": str(ruta.parent)
    }


def listar_archivos_recientes(directorio: Path, extension: str = None, limite: int = 10) -> list:
    """
    List the most recent files in a directory
    
    Args:
        directorio: Directory to list
        extension: Filter by extension (optional)
        limite: Max files to return
        
    Returns:
        List of Paths sorted by mtime
    """
    try:
        archivos = []
        patron = f"*.{extension}" if extension else "*"
        
        for archivo in directorio.glob(patron):
            if archivo.is_file():
                archivos.append(archivo)
        
        # Sort by mtime (newest first)
        archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        return archivos[:limite]
    
    except Exception as e:
        print(Fore.RED + f"Error listing files: {e}")
        return []


def eliminar_archivo_seguro(ruta: Path) -> bool:
    """
    Safely delete a file with confirmation
    
    Args:
        ruta: File path to delete
        
    Returns:
        True if deleted successfully
    """
    try:
        if not ruta.exists():
            print(Fore.RED + "File does not exist")
            return False
        
        info = obtener_info_archivo(ruta)
        print_warning_box("⚠️  DELETE FILE?", [
            f"📝 {info['nombre']}",
            f"💾 {info['tamano_mb']} MB",
            f"📁 {info['directorio']}",
            "1 - Yes, delete",
            "2 - No, keep",
        ], [Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.GREEN, Fore.RED])
        
        from src.utils.animations import mostrar_cursor, ocultar_cursor
        mostrar_cursor()
        choice = input(Fore.CYAN + "\n  -> Your choice [1-2]: " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        if choice == "1":
            ruta.unlink()
            print(Fore.GREEN + "✅ File deleted successfully")
            return True
        else:
            print(Fore.CYAN + "✅ File kept")
            return False
    
    except PermissionError:
        print(Fore.RED + "❌ Permission denied to delete the file")
        return False
    except Exception as e:
        print(Fore.RED + f"❌ Delete error: {e}")
        return False


# English aliases (new API)
find_file = buscar_archivo
get_extension = obtener_extension
build_output_name = generar_nombre_salida
get_file_info = obtener_info_archivo
list_recent_files = listar_archivos_recientes
delete_file_safe = eliminar_archivo_seguro
