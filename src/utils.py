import os
import pathlib
import colorama
from colorama import Fore, Style

# Inicializar colorama para colores en la terminal
colorama.init(autoreset=True)

# Directorios base para almacenamiento
BASE_DIR = pathlib.Path("/storage/emulated/0")
BASE_VIDEOS = BASE_DIR / "VMovies/Videos_Downloader"
BASE_AUDIOS = BASE_DIR / "Music/Music_Downloader"
BASE_IMAGENES = BASE_DIR / "Pictures/Picture_Downloader"

# Mapeo de tipos de archivo a rutas
RUTAS = {
    "video": BASE_VIDEOS,
    "audio": BASE_AUDIOS,
    "imagen": BASE_IMAGENES
}

def obtener_ruta(tipo: str) -> pathlib.Path:
    """
    Retorna la ruta base de almacenamiento según el tipo de archivo.
    Si el tipo no existe, usa la carpeta de videos por defecto.
    """
    return RUTAS.get(tipo, BASE_VIDEOS)

def crear_carpetas():
    """
    Crea las carpetas necesarias para guardar los archivos si no existen.
    """
    for ruta in RUTAS.values():
        ruta.mkdir(parents=True, exist_ok=True)

def imprimir_titulo(texto: str):
    """
    Imprime un título decorado en la consola.
    """
    borde = "═" * 50
    print(f"{borde}\n  🎵📥 {texto} 📥🎵\n{borde}")

def buscar_archivo(nombre_archivo: str, carpeta_base: pathlib.Path = BASE_DIR) -> pathlib.Path | None:
    """
    Busca un archivo en el almacenamiento del dispositivo, comenzando desde `carpeta_base`.
    Retorna la ruta completa si el archivo existe, o None si no se encuentra.
    """
    print(f"🔍 Buscando '{nombre_archivo}' en {carpeta_base}...")

    for archivo in carpeta_base.rglob(nombre_archivo):  # Búsqueda más eficiente
        if archivo.is_file():
            return archivo

    print(Fore.RED + f"❌ Archivo '{nombre_archivo}' no encontrado." + Style.RESET_ALL)
    return None

def pausar():
    """
    Pausa la ejecución del programa hasta que el usuario presione ENTER.
    """
    input(Fore.CYAN + "\n🔹 Presiona ENTER para continuar..." + Style.RESET_ALL)

# Crear carpetas en la ejecución inicial
crear_carpetas()

