import os
import shutil
import pyfiglet
from colorama import Fore, Style, init

# Importar funciones de animaciones.py
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

# Importar módulos del programa
from src.descargador import menu_descargador
from src.convertidor import menu_convertidor
from src.mejorador import menu_mejorador
from src.ayuda import menu_ayuda

# Inicializar colorama
init(autoreset=True)

# Información del proyecto
NOMBRE_PROYECTO = "Data Downloader"
CREADOR = "Shadow-TermDev"
REPOSITORIO = "github.com/Shadow-TermDev/Data_Downloader"
VERSION = "v1.4.2"

# Función para limpiar pantalla
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

# Centrar texto en terminal
def centrar_texto(texto):
    try:
        ancho = shutil.get_terminal_size().columns
    except:
        ancho = 80
    return texto.center(ancho)

# Mostrar menú principal
def mostrar_menu():
    limpiar_pantalla()

    # Título grande
    titulo = pyfiglet.figlet_format("Downloader", font="slant")
    for linea in titulo.splitlines():
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("MUSIC, VIDEO & IMAGE DOWNLOADER\n"))

    ancho_cuadro = 50
    b = Fore.MAGENTA + "│" + Fore.RESET
    linea_vacia = Fore.MAGENTA + "│" + " " * (ancho_cuadro - 2) + Fore.MAGENTA + "│"

    # === CUADRO DE INFORMACIÓN DEL PROYECTO ===
    print(Fore.MAGENTA + "╭" + "─" * (ancho_cuadro - 2) + "╮")
    print(Fore.MAGENTA + "│" + Fore.YELLOW + f" {NOMBRE_PROYECTO} ".center(ancho_cuadro - 2) + Fore.MAGENTA + "│")
    print(linea_vacia)
    print(Fore.MAGENTA + "│" + Fore.CYAN + " Creador: ".center(ancho_cuadro - 2) + Fore.MAGENTA + "│")
    print(Fore.MAGENTA + "│" + Fore.WHITE + f" {CREADOR} ".center(ancho_cuadro - 2) + Fore.MAGENTA + "│")
    print(linea_vacia)
    print(Fore.MAGENTA + "│" + Fore.CYAN + " Repositorio: ".center(ancho_cuadro - 2) + Fore.MAGENTA + "│")
    print(Fore.MAGENTA + "│" + Fore.WHITE + f" {REPOSITORIO} ".center(ancho_cuadro - 2) + Fore.MAGENTA + "│")
    print(linea_vacia)
    print(Fore.MAGENTA + "│" + Fore.CYAN + " Versión: ".center(ancho_cuadro - 2) + Fore.MAGENTA + "│")
    print(Fore.MAGENTA + "│" + Fore.WHITE + f" {VERSION} ".center(ancho_cuadro - 2) + Fore.MAGENTA + "│")
    print(Fore.MAGENTA + "╰" + "─" * (ancho_cuadro - 2) + "╯\n")

    # === CUADRO DE OPCIONES ===
    opciones = [
        (Fore.GREEN,  "1 - Descargar contenido"),
        (Fore.BLUE,   "2 - Convertir archivos"),
        (Fore.CYAN,   "3 - Mejorar calidad de archivos"),
        (Fore.YELLOW, "4 - Ayuda"),
        (Fore.RED,    "5 - Salir"),
    ]

    print(Fore.MAGENTA + "╭" + "─" * (ancho_cuadro - 2) + "╮")
    for color, texto in opciones:
        print(Fore.MAGENTA + "│ " + color + texto.ljust(ancho_cuadro - 4) + Fore.MAGENTA + " │")
    print(Fore.MAGENTA + "╰" + "─" * (ancho_cuadro - 2) + "╯\n")

    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

# Bucle principal
def main():
    ocultar_cursor()

    while True:
        mostrar_menu()
        opcion = input().strip()
        ocultar_cursor()

        menus = {
            "1": menu_descargador,
            "2": menu_convertidor,
            "3": menu_mejorador,
            "4": menu_ayuda,
            "5": lambda: None
        }

        if opcion in menus:
            if opcion == "5":
                #limpiar_pantalla()
                print()
                print(Fore.RED + centrar_texto("¡Gracias por usar Data Downloader!"))
                print(Fore.CYAN + centrar_texto(f"{VERSION} - {CREADOR}"))
                mostrar_cursor()
                break
            menus[opcion]()
        else:
            print(Fore.RED + centrar_texto("Opción no válida. Inténtalo de nuevo.") + Style.RESET_ALL)
            input(Fore.YELLOW + centrar_texto("Presiona Enter para continuar..."))

if __name__ == "__main__":
    main()
