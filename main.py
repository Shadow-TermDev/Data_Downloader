import os
import sys
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
from src.transiciones import menu_transiciones

# Inicializar colorama para colores en la terminal
init(autoreset=True)

# Función para limpiar la pantalla en diferentes sistemas operativos
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

# Función para centrar texto en la terminal, con manejo de error en entornos sin terminal
def centrar_texto(texto):
    try:
        ancho_terminal = shutil.get_terminal_size().columns
    except:
        ancho_terminal = 80  # Ancho por defecto si no hay terminal
    return texto.center(ancho_terminal)

# Función para mostrar el menú con estilos
def mostrar_menu():
    limpiar_pantalla()
    # Título "Downloader" en amarillo
    titulo = pyfiglet.figlet_format("Downloader", font="slant")
    for linea in titulo.split("\n"):
        print(Fore.YELLOW + centrar_texto(linea))
    # Subtítulo en azul
    print(Fore.CYAN + centrar_texto("MUSIC, VIDEO & IMAGE DOWNLOADER\n"))

    # Opciones del menú
    opciones = [
        (Fore.GREEN, "1 - Descargar contenido"),
        (Fore.BLUE, "2 - Convertir archivos"),
        (Fore.CYAN, "3 - Mejorar calidad de archivos"),
        (Fore.YELLOW, "4 - Ayuda"),
        (Fore.MAGENTA, "5 - Configurar transiciones"),
        (Fore.RED, "6 - Salir"),
    ]

    # Dibujar cuadro del menú
    ancho_cuadro = 50
    print(Fore.MAGENTA + "╭" + "─" * (ancho_cuadro - 2))
    for color, texto in opciones:
        print(Fore.MAGENTA + "│" + color + " " + texto)
    print(Fore.MAGENTA + "╰" + "─" * (ancho_cuadro - 2))

    # Mostrar cursor antes de pedir la opción
    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

# Función principal del programa
def main():
    ocultar_cursor()  # Ocultar cursor al iniciar el programa

    while True:
        mostrar_menu()
        opcion = input().strip()
        ocultar_cursor()  # Ocultar cursor después de la entrada

        # Manejamos opciones válidas con un diccionario
        opciones_menu = {
            "1": menu_descargador,
            "2": menu_convertidor,
            "3": menu_mejorador,
            "4": menu_ayuda,
            "5": menu_transiciones,
            "6": lambda: print(Fore.RED + "\nSaliendo del programa... ¡Hasta luego!")
        }

        # Ejecutar la opción seleccionada o mostrar error
        if opcion in opciones_menu:
            if opcion == "6":
                mostrar_cursor()
                break  # Salir del bucle si elige opción 6
            opciones_menu[opcion]()  # Ejecutar la función correspondiente
        else:
            print(Fore.RED + "\nOpción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

# Ejecutar solo si el script se ejecuta directamente
if __name__ == "__main__":
    main()

