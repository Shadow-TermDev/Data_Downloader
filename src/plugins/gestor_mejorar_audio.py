import os
import subprocess
from colorama import Fore, Style
from src.utils import pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def seleccionar_calidad():
    print(Fore.CYAN + "\nSelecciona la calidad deseada:")
    opciones = {
        "1": ("128k", "128 kbps - Calidad estándar"),
        "2": ("256k", "256 kbps - Alta calidad"),
        "3": ("320k", "320 kbps - Calidad máxima (mejor)")
    }
    for k, (_, desc) in opciones.items():
        color = Fore.GREEN if k == "1" else Fore.YELLOW if k == "2" else Fore.MAGENTA
        print(color + f"  {k} - {desc}")

    mostrar_cursor()
    choice = input(Fore.CYAN + "\n  -> Elige una opción [1-3]: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    return opciones.get(choice, opciones["2"])[0]  # Por defecto 256k


def generar_nombre_salida(ruta_original):
    base, ext = os.path.splitext(ruta_original)
    return f"{base}_mejorado{ext}"


def ejecutar_ffmpeg(entrada, salida, bitrate):
    """
    Mejora el audio con FFmpeg manteniendo:
    - Portada (cover art)
    - Metadatos
    - Calidad máxima posible
    """
    comando = [
        "ffmpeg",
        "-i", entrada,
        "-c:a", "libmp3lame",
        "-b:a", bitrate,
        "-map_metadata", "0",      # Copia todos los metadatos
        "-map", "0",               # Copia todas las pistas (incluye portada)
        "-y",                      # Sobrescribe sin preguntar
        salida
    ]

    print(Fore.YELLOW + f"\nMejorando audio a {bitrate} (manteniendo portada)...")
    print(Fore.CYAN + "Esto puede tomar algunos segundos...\n")

    result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(Fore.GREEN + f"\nAudio mejorado con éxito!")
        print(Fore.WHITE + f"Guardado como: {os.path.basename(salida)}")
        return True
    else:
        print(Fore.RED + "\nError al procesar el audio con ffmpeg.")
        if "No such file or directory" in result.stderr:
            print(Fore.RED + "ffmpeg no está instalado.")
        else:
            print(Fore.RED + result.stderr.split("\n")[-3:])
        return False


def preguntar_eliminar_original(ruta):
    print(Fore.YELLOW + "\n¿Deseas eliminar el audio original?")
    print(Fore.GREEN + "  1 - Sí, eliminar")
    print(Fore.RED + "  2 - No, conservar")

    mostrar_cursor()
    choice = input(Fore.CYAN + "\n  -> Tu elección [1-2]: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    if choice == "1":
        try:
            os.remove(ruta)
            print(Fore.GREEN + "Archivo original eliminado.")
        except Exception as e:
            print(Fore.RED + f"No se pudo eliminar: {e}")


def mejorar_calidad_audio(ruta_audio):
    """
    Recibe directamente la ruta completa (gracias a buscar_archivo)
    """
    ocultar_cursor()

    try:
        if not os.path.exists(ruta_audio):
            print(Fore.RED + f"\nNo se encontró el archivo:\n{ruta_audio}")
            pausar()
            return

        bitrate = seleccionar_calidad()
        salida = generar_nombre_salida(ruta_audio)

        if ejecutar_ffmpeg(ruta_audio, salida, bitrate):
            preguntar_eliminar_original(ruta_audio)

    except Exception as e:
        print(Fore.RED + f"\nError inesperado: {e}")
    finally:
        pausar()  # ← Siempre espera Enter al final
