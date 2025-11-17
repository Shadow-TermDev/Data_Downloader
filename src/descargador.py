import os
import shutil
from pyfiglet import Figlet
from colorama import Fore, Style, init

# Importamos directamente los gestores reales
from src.plugins.gestor_descarga_video import descargar_video
from src.plugins.gestor_descarga_audio import descargar_audio
from src.plugins.gestor_descarga_imagen import descargar_imagen

from src.plugins.animaciones import ocultar_cursor, mostrar_cursor
from src.utils import pausar

init(autoreset=True)

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def centrar_texto(texto):
    try:
        ancho = shutil.get_terminal_size().columns
    except:
        ancho = 80
    return texto.center(ancho)

def mostrar_menu_descargador():
    limpiar_pantalla()

    # Título moderno (pyfiglet actual)
    figlet = Figlet(font="slant")
    titulo = figlet.renderText("Downloader")
    for linea in titulo.splitlines():
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("DESCARGA ARCHIVOS MULTIMEDIA\n"))

    # Cuadro perfecto de 52 caracteres (igual que el de mejorador)
    ancho = 52
    print(Fore.MAGENTA + "╭" + "─" * (ancho - 2) + "╮")
    
    opciones = [
        "1 - Descargar video ",
        "2 - Descargar audio ",
        "3 - Descargar imagen ",
        "4 - Volver al menú principal "
    ]

    for i, texto in enumerate(opciones):
        color = Fore.GREEN if i < 3 else Fore.RED
        print(Fore.MAGENTA + "│ " + color + texto.ljust(ancho - 4) + Fore.MAGENTA + " │")
    
    print(Fore.MAGENTA + "╰" + "─" * (ancho - 2) + "╯\n")

    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

def menu_descargador():
    ocultar_cursor()

    while True:
        mostrar_menu_descargador()
        opcion = input().strip()
        ocultar_cursor()

        if opcion == "4":
            return

        if opcion not in ["1", "2", "3"]:
            print(Fore.RED + centrar_texto("Opción no válida. Inténtalo de nuevo.") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))
            continue

        mensajes = {
            "1": "Ingresa la URL del video: ",
            "2": "Ingresa la URL del audio: ",
            "3": "Ingresa la URL de la imagen: "
        }

        funciones = {
            "1": descargar_video,
            "2": descargar_audio,
            "3": descargar_imagen
        }

        mostrar_cursor()
        print()
        url = input(Fore.YELLOW + f"{mensajes[opcion]}").strip()
        ocultar_cursor()

        if not url:
            print(Fore.RED + centrar_texto("URL vacía.") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))
            continue

        try:
            funciones[opcion](url)
        except Exception as e:
            print(Fore.RED + centrar_texto(f"Error en la descarga: {e}") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))

if __name__ == "__main__":
    menu_descargador()
