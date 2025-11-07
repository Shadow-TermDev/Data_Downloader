import os
import subprocess
from colorama import Fore, Style
from src.utils import BASE_VIDEOS as ruta_videos
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones
import yt_dlp

def obtener_calidades(url, tipo="video"):
    """Obtiene las calidades disponibles de un video o audio."""
    calidades = []
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            for formato in info["formats"]:
                if tipo == "video" and formato.get("vcodec") != "none":
                    tamaño_mb = (formato.get("filesize", 0) or 0) / (1024 * 1024)
                    tamaño_texto = f"{tamaño_mb:.2f} MB" if tamaño_mb > 0 else "Desconocido"
                    calidades.append((formato["format_id"], formato["format_note"], tamaño_texto))
    except Exception as e:
        print(Fore.RED + f"\n❌ Error al obtener calidades: {e}" + Style.RESET_ALL)
    return calidades

def mostrar_menu_calidades(calidades):
    """Muestra las calidades disponibles para que el usuario seleccione."""
    print(Fore.CYAN + "\n🎥 Calidades disponibles:")
    for i, (formato, calidad, tamaño) in enumerate(calidades):
        print(Fore.GREEN + f" {i + 1} - {calidad} ({formato}) [{tamaño}]")
    
    mostrar_cursor()  # Mostrar cursor antes de solicitar entrada
    seleccion = input(Fore.CYAN + "  -> Ingresa el número de la calidad: " + Style.RESET_ALL).strip()
    ocultar_cursor()  # Ocultar cursor después de la entrada

    return seleccion

def seleccionar_calidad(calidades):
    """Solicita al usuario una calidad y valida la entrada."""
    seleccion = mostrar_menu_calidades(calidades)
    try:
        seleccion = int(seleccion) - 1
        if 0 <= seleccion < len(calidades):
            return calidades[seleccion][0]
        else:
            raise ValueError
    except ValueError:
        print(Fore.RED + "⚠️ Selección no válida. Volviendo al menú..." + Style.RESET_ALL)
        return None

def descargar_video(url):
    """Proceso principal para descargar videos."""
    ocultar_cursor()  # Ocultar cursor al iniciar

    try:
        print(Fore.YELLOW + "\n🔍 Obteniendo calidades disponibles..." + Style.RESET_ALL)
        calidades = obtener_calidades(url, "video")
        if not calidades:
            print(Fore.RED + "❌ No hay calidades disponibles." + Style.RESET_ALL)
            return

        formato_elegido = seleccionar_calidad(calidades)
        if not formato_elegido:
            return

        print(Fore.YELLOW + "\n⏳ Descargando video..." + Style.RESET_ALL)
        salida = os.path.join(ruta_videos, "%(title)s.%(ext)s")
        comando = ["yt-dlp", "-f", formato_elegido, "-o", salida, url]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if resultado.returncode == 0:
            print(Fore.GREEN + "\n✅ Video descargado correctamente." + Style.RESET_ALL)
            print(Fore.BLUE + f"\nArchivo guardado en: {ruta_videos}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Error en la descarga del video." + Style.RESET_ALL)
            print(resultado.stderr)

    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {e}" + Style.RESET_ALL)

    finally:
        mostrar_cursor()  # Mostrar cursor antes de solicitar entrada
        input(Fore.CYAN + "\nPresiona ENTER para volver al menú..." + Style.RESET_ALL)
        ocultar_cursor()  # Ocultar cursor después de la entrada

