import os
import shutil
from pyfiglet import Figlet
from colorama import Fore, Style, init

from src.utils import buscar_archivo, pausar
from src.plugins.gestor_mejorar_imagen import mejorar_calidad_imagen
from src.plugins.gestor_mejorar_audio import mejorar_calidad_audio
from src.plugins.gestor_mejorar_videos import mejorar_calidad_video
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

init(autoreset=True)

RUTA_BASE = "/storage/emulated/0/"

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def centrar_texto(texto):
    try:
        ancho = shutil.get_terminal_size().columns
    except:
        ancho = 80
    return texto.center(ancho)

def mostrar_submenu_mejorador():
    limpiar_pantalla()

    figlet = Figlet(font="slant")
    titulo = figlet.renderText("Quality Boost")
    for linea in titulo.splitlines():
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("IMPROVE IMAGE, VIDEO & AUDIO QUALITY\n"))

    ancho = 52
    print(Fore.MAGENTA + "╭" + "─" * (ancho - 2) + "╮")
    
    opciones = [
        "1 - Mejorar calidad de video ",
        "2 - Mejorar calidad de audio ",
        "3 - Mejorar calidad de imagen ",
        "4 - Volver al menú principal "
    ]

    for i, texto in enumerate(opciones):
        color = Fore.GREEN if i < 3 else Fore.RED
        print(Fore.MAGENTA + "│ " + color + texto.ljust(ancho - 4) + Fore.MAGENTA + " │")
    
    print(Fore.MAGENTA + "╰" + "─" * (ancho - 2) + "╯\n")

    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

def menu_mejorador():
    ocultar_cursor()

    while True:
        mostrar_submenu_mejorador()
        opcion = input().strip()
        ocultar_cursor()

        if opcion == "4":
            return

        if opcion not in ["1", "2", "3"]:
            print(Fore.RED + centrar_texto("Opción no válida. Inténtalo de nuevo.") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))
            continue

        mensajes = {
            "1": "Ingresa el nombre del video: ",
            "2": "Ingresa el nombre del audio: ",
            "3": "Ingresa el nombre de la imagen: "
        }
        funciones = {
            "1": mejorar_calidad_video,
            "2": mejorar_calidad_audio,
            "3": mejorar_calidad_imagen
        }

        mostrar_cursor()
        print()
        nombre = input(Fore.YELLOW + f"{mensajes[opcion]}").strip()
        ocultar_cursor()

        if not nombre:
            print(Fore.RED + centrar_texto("Nombre vacío.") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))
            continue

        ruta = buscar_archivo(nombre)
        if not ruta:
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))
            continue

        try:
            funciones[opcion](ruta)
        except Exception as e:
            print(Fore.RED + centrar_texto(f"Error inesperado: {e}") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))

if __name__ == "__main__":
    menu_mejorador()
