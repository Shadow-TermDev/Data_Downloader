import os
import shutil
from pyfiglet import Figlet
from colorama import Fore, Style, init

# Importamos directamente los gestores reales (sin puente)
from src.plugins.convertidor.video import convertir_video
from src.plugins.convertidor.video_a_audio import convertir_video_a_audio
from src.plugins.convertidor.imagen import convertir_imagen
from src.plugins.convertidor.audio import convertir_audio

from src.utils import buscar_archivo, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

init(autoreset=True)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def centrar_texto(texto):
    try:
        ancho = shutil.get_terminal_size().columns
    except:
        ancho = 80
    return texto.center(ancho)

def mostrar_submenu_convertidor():
    limpiar_pantalla()

    # Título moderno
    figlet = Figlet(font="slant")
    titulo = figlet.renderText("Converter")
    for linea in titulo.splitlines():
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("VIDEO, AUDIO & IMAGE CONVERTER\n"))

    # Cuadro perfecto (igual que mejorador y descargador)
    ancho = 52
    print(Fore.MAGENTA + "╭" + "─" * (ancho - 2) + "╮")
    
    opciones = [
        "1 - Convertir video ",
        "2 - Video → Audio ",
        "3 - Convertir imagen ",
        "4 - Convertir audio ",
        "5 - Volver al menú principal "
    ]

    for i, texto in enumerate(opciones):
        color = Fore.GREEN if i < 4 else Fore.RED
        print(Fore.MAGENTA + "│ " + color + texto.ljust(ancho - 4) + Fore.MAGENTA + " │")
    
    print(Fore.MAGENTA + "╰" + "─" * (ancho - 2) + "╯\n")

    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

def menu_convertidor():
    ocultar_cursor()

    while True:
        mostrar_submenu_convertidor()
        opcion = input().strip()
        ocultar_cursor()

        if opcion == "5":
            return

        if opcion not in ["1", "2", "3", "4"]:
            print(Fore.RED + centrar_texto("Opción no válida. Inténtalo de nuevo.") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))
            continue

        # Configuración por opción
        configs = {
            "1": ("Ingresa el nombre del video: ", convertir_video, ["mp4", "mkv", "avi", "mov", "webm"]),
            "2": ("Ingresa el nombre del video: ", convertir_video_a_audio, ["mp3", "wav", "ogg", "aac", "flac"]),
            "3": ("Ingresa el nombre de la imagen: ", convertir_imagen, ["png", "jpg", "jpeg", "webp", "bmp"]),
            "4": ("Ingresa el nombre del audio: ", convertir_audio, ["mp3", "wav", "ogg", "aac", "flac"])
        }

        mensaje, funcion, formatos = configs[opcion]

        mostrar_cursor()
        print()
        nombre = input(Fore.YELLOW + f"{mensaje}").strip()
        ocultar_cursor()

        if not nombre:
            print(Fore.RED + centrar_texto("Nombre vacío.") + Style.RESET_ALL)
            continue

        ruta = buscar_archivo(nombre)
        if not ruta:
            continue

        # Pedir formato
        while True:
            mostrar_cursor()
            fmt = input(Fore.CYAN + f"Formato de salida ({', '.join(formatos)}): " + Style.RESET_ALL).strip().lower()
            ocultar_cursor()

            if fmt in formatos:
                try:
                    funcion(ruta, fmt)
                except Exception as e:
                    print(Fore.RED + centrar_texto(f"Error en conversión: {e}") + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + centrar_texto(f"Formato no soportado. Opciones: {', '.join(formatos)}") + Style.RESET_ALL)

        # Pausa final automática

if __name__ == "__main__":
    menu_convertidor()
