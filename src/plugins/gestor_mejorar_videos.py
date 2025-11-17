import os
import subprocess
from colorama import Fore, Style
from src.utils import pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def obtener_resolucion():
    print(Fore.CYAN + "\nSelecciona la calidad deseada:")
    opciones = {
        "1": ("1280x720", "720p (HD)"),
        "2": ("1920x1080", "1080p (Full HD)"),
        "3": ("3840x2160", "4K (Ultra HD)")
    }
    for k, (_, desc) in opciones.items():
        print(Fore.GREEN + f"  {k} - {desc}")

    mostrar_cursor()
    choice = input(Fore.CYAN + "\n  -> Elige una opción [1-3]: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    return opciones.get(choice, opciones["2"])[0]

def generar_nombre_salida(ruta_original):
    base, ext = os.path.splitext(ruta_original)
    return f"{base}_mejorado{ext}"

def ejecutar_ffmpeg(entrada, salida, resolucion):
    comando = [
        "ffmpeg", "-i", entrada,
        "-vf", f"scale={resolucion}:flags=lanczos",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "copy",
        "-y",  # Sobrescribir sin preguntar
        salida
    ]

    print(Fore.YELLOW + f"\nMejorando video a {resolucion}...")
    print(Fore.CYAN + "Esto puede tomar varios minutos...\n")

    result = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(Fore.GREEN + f"\nVideo mejorado exitosamente!")
        print(Fore.WHITE + f"Guardado como: {os.path.basename(salida)}")
        return True
    else:
        print(Fore.RED + "\nError al procesar el video con ffmpeg.")
        if "No such file" in result.stderr:
            print(Fore.RED + "ffmpeg no está instalado o no está en PATH.")
        else:
            print(Fore.RED + result.stderr[:300] + "...")
        return False

def preguntar_eliminar_original(ruta):
    print(Fore.YELLOW + "\n¿Deseas eliminar el video original?")
    print(Fore.GREEN + "  1 - Sí, eliminar")
    print(Fore.RED + "  2 - No, conservar")

    mostrar_cursor()
    choice = input(Fore.CYAN + "\n  -> Tu elección [1-2]: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    if choice == "1":
        try:
            os.remove(ruta)
            print(Fore.GREEN + "Archivo original eliminado.")
        except:
            print(Fore.RED + "No se pudo eliminar el archivo original.")

def mejorar_calidad_video(ruta_video):
    ocultar_cursor()

    try:
        resolucion = obtener_resolucion()
        salida = generar_nombre_salida(ruta_video)

        if ejecutar_ffmpeg(ruta_video, salida, resolucion):
            preguntar_eliminar_original(ruta_video)

    except Exception as e:
        print(Fore.RED + f"\nError inesperado: {e}")
    finally:
        pausar()  # ← Siempre espera Enter al final
