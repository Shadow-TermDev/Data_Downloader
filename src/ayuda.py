import os
import pyfiglet
from colorama import Fore, Style, init
from src.plugins.gestor_ayuda import obtener_ayuda
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos funciones

init(autoreset=True)

def limpiar_pantalla():
    os.system("clear")

def centrar_texto(texto):
    ancho_terminal = os.get_terminal_size().columns
    return texto.center(ancho_terminal)

def menu_ayuda():
    ocultar_cursor()  # Ocultar cursor al entrar al menú

    while True:
        limpiar_pantalla()
        titulo = pyfiglet.figlet_format("Ayuda", font="slant")
        for linea in titulo.split("\n"):
            print(Fore.YELLOW + centrar_texto(linea))
        print(Fore.CYAN + centrar_texto("📖 Manual de Usuario 📖\n"))

        opciones = [
            Fore.GREEN + " 1 - Cómo descargar contenido",
            Fore.GREEN + " 2 - Cómo convertir archivos",
            Fore.GREEN + " 3 - Cómo mejorar calidad",
            Fore.RED   + " 4 - Volver al menú principal"
        ]

        print(Fore.MAGENTA + "╭" + "─" * 50)
        for opcion in opciones:
            print(Fore.MAGENTA + "│ " + opcion)
        print(Fore.MAGENTA + "╰" + "─" * 50)

        # Mostrar cursor antes de pedir la opción
        mostrar_cursor()
        print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")
        opcion = input().strip()
        ocultar_cursor()  # Ocultar cursor después de la entrada

        if opcion in ["1", "2", "3"]:
            ayuda = obtener_ayuda(opcion)
            mostrar_info(ayuda["titulo"], ayuda["mensaje"])
        elif opcion == "4":
            break
        else:
            print(Fore.RED + "\n⚠️ Opción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

def mostrar_info(titulo, mensaje):
    limpiar_pantalla()
    print(Fore.YELLOW + centrar_texto(f"📖 {titulo} 📖\n"))
    print(Fore.GREEN + centrar_texto(mensaje) + "\n")

    # Mostrar cursor antes de esperar la entrada
    mostrar_cursor()
    input(Fore.CYAN + "🔙 Presiona ENTER para volver al menú de ayuda...")
    ocultar_cursor()  # Ocultar cursor después de la entrada

