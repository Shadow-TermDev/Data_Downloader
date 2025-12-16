"""
Gestor de archivos y búsqueda en el sistema
Autor: Shadow-TermDev
"""

import os
from pathlib import Path
from typing import Optional
from colorama import Fore, Style

from config.settings import STORAGE_BASE, MESSAGES


def buscar_archivo(nombre_archivo: str, carpeta_base: Path = STORAGE_BASE) -> Optional[Path]:
    """
    Busca un archivo en el almacenamiento del dispositivo
    
    Args:
        nombre_archivo: Nombre del archivo a buscar
        carpeta_base: Directorio base donde iniciar la búsqueda
        
    Returns:
        Path del archivo si se encuentra, None en caso contrario
    """
    print(Fore.CYAN + f"🔍 Buscando '{nombre_archivo}' en {carpeta_base}...")
    
    try:
        # Búsqueda recursiva eficiente
        for archivo in carpeta_base.rglob(nombre_archivo):
            if archivo.is_file():
                print(Fore.GREEN + f"✅ Archivo encontrado: {archivo}")
                return archivo
        
        # Si no se encuentra, buscar con coincidencia parcial
        print(Fore.YELLOW + "No se encontró coincidencia exacta. Buscando similares...")
        
        archivos_similares = []
        nombre_lower = nombre_archivo.lower()
        
        for archivo in carpeta_base.rglob("*"):
            if archivo.is_file() and nombre_lower in archivo.name.lower():
                archivos_similares.append(archivo)
                if len(archivos_similares) >= 5:  # Limitar a 5 resultados
                    break
        
        if archivos_similares:
            print(Fore.CYAN + "\n📁 Archivos similares encontrados:")
            for i, archivo in enumerate(archivos_similares, 1):
                print(Fore.WHITE + f"  {i}. {archivo.name}")
                print(Fore.BLUE + f"     {archivo.parent}")
            
            from src.utils.animations import mostrar_cursor, ocultar_cursor
            mostrar_cursor()
            seleccion = input(Fore.YELLOW + "\n¿Usar alguno de estos? (1-5, Enter=ninguno): ").strip()
            ocultar_cursor()
            
            if seleccion.isdigit() and 1 <= int(seleccion) <= len(archivos_similares):
                archivo_seleccionado = archivos_similares[int(seleccion) - 1]
                print(Fore.GREEN + f"✅ Usando: {archivo_seleccionado.name}")
                return archivo_seleccionado
        
        print(Fore.RED + f"❌ {MESSAGES['file_not_found']}: '{nombre_archivo}'")
        return None
    
    except PermissionError:
        print(Fore.RED + "❌ Permiso denegado para acceder a algunos directorios")
        return None
    except Exception as e:
        print(Fore.RED + f"❌ Error durante la búsqueda: {e}")
        return None


def obtener_extension(ruta: Path) -> str:
    """
    Obtiene la extensión de un archivo sin el punto
    
    Args:
        ruta: Path del archivo
        
    Returns:
        Extensión en minúsculas (sin punto)
    """
    return ruta.suffix.lstrip('.').lower()


def generar_nombre_salida(ruta_original: Path, sufijo: str = "_procesado", nueva_extension: str = None) -> Path:
    """
    Genera un nombre para archivo de salida
    
    Args:
        ruta_original: Path del archivo original
        sufijo: Sufijo a agregar al nombre (default: "_procesado")
        nueva_extension: Nueva extensión si se quiere cambiar
        
    Returns:
        Path del nuevo archivo
    """
    nombre_base = ruta_original.stem
    extension = nueva_extension if nueva_extension else ruta_original.suffix
    
    if not extension.startswith('.'):
        extension = f'.{extension}'
    
    return ruta_original.parent / f"{nombre_base}{sufijo}{extension}"


def verificar_espacio_disponible(directorio: Path, tamano_requerido_mb: float = 100) -> bool:
    """
    Verifica si hay suficiente espacio en disco
    
    Args:
        directorio: Directorio a verificar
        tamano_requerido_mb: Espacio requerido en MB
        
    Returns:
        True si hay suficiente espacio
    """
    try:
        stat = os.statvfs(directorio)
        espacio_libre_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
        
        if espacio_libre_mb < tamano_requerido_mb:
            print(Fore.YELLOW + f"⚠️ Poco espacio disponible: {espacio_libre_mb:.1f} MB")
            return False
        
        return True
    except Exception:
        # Si no se puede verificar, asumir que hay espacio
        return True


def obtener_info_archivo(ruta: Path) -> dict:
    """
    Obtiene información detallada de un archivo
    
    Args:
        ruta: Path del archivo
        
    Returns:
        Diccionario con información del archivo
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
    Lista los archivos más recientes en un directorio
    
    Args:
        directorio: Directorio a listar
        extension: Filtrar por extensión (opcional)
        limite: Número máximo de archivos a retornar
        
    Returns:
        Lista de Path ordenados por fecha de modificación
    """
    try:
        archivos = []
        patron = f"*.{extension}" if extension else "*"
        
        for archivo in directorio.glob(patron):
            if archivo.is_file():
                archivos.append(archivo)
        
        # Ordenar por fecha de modificación (más recientes primero)
        archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        return archivos[:limite]
    
    except Exception as e:
        print(Fore.RED + f"Error al listar archivos: {e}")
        return []


def eliminar_archivo_seguro(ruta: Path) -> bool:
    """
    Elimina un archivo de forma segura con confirmación
    
    Args:
        ruta: Path del archivo a eliminar
        
    Returns:
        True si se eliminó correctamente
    """
    try:
        if not ruta.exists():
            print(Fore.RED + "El archivo no existe")
            return False
        
        info = obtener_info_archivo(ruta)
        print(Fore.YELLOW + f"\n⚠️ ¿Eliminar '{info['nombre']}'? ({info['tamano_mb']} MB)")
        print(Fore.GREEN + "  1 - Sí, eliminar")
        print(Fore.RED + "  2 - No, conservar")
        
        from src.utils.animations import mostrar_cursor, ocultar_cursor
        mostrar_cursor()
        choice = input(Fore.CYAN + "\n  -> Tu elección [1-2]: " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        if choice == "1":
            ruta.unlink()
            print(Fore.GREEN + "✅ Archivo eliminado correctamente")
            return True
        else:
            print(Fore.CYAN + "✅ Archivo conservado")
            return False
    
    except PermissionError:
        print(Fore.RED + "❌ Permiso denegado para eliminar el archivo")
        return False
    except Exception as e:
        print(Fore.RED + f"❌ Error al eliminar: {e}")
        return False
