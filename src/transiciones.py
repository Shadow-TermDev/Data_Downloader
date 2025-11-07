import os
import pyfiglet
from colorama import Fore, Style, init
from src.plugins.animaciones import obtener_transicion, cambiar_transicion, ocultar_cursor, mostrar_cursor  # Importamos las funciones

# Inicializar colorama para colores en la terminal
init(autoreset=True)

def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system("clear" if os.name == "posix" else "cls")

def centrar_texto(texto: str) -> str:
    """Centra el texto en la terminal, si es posible."""
    try:
        ancho_terminal = os.get_terminal_size().columns
        return texto.center(ancho_terminal)
    except OSError:
        return texto  # Si no se puede obtener el tamaño, devuelve el texto sin centrar

def mostrar_menu_transiciones():
    """Muestra el menú de configuración de transiciones."""
    limpiar_pantalla()

    # Banner "Transiciones"
    titulo = pyfiglet.figlet_format("Transiciones", font="slant")
    for linea in titulo.split("\n"):
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("🎥 Configuración de Transiciones 🎥\n"))

    # Definición de transiciones y obtención del estado actual
    transiciones = ["Fade", "Slide", "Zoom", "Wipe", "Flash"]
    transicion_actual = obtener_transicion()
    
    opciones = [
        Fore.GREEN   + f"1 - Fade   {'(Actual)' if transicion_actual == 'Fade' else ''}",
        Fore.BLUE    + f"2 - Slide  {'(Actual)' if transicion_actual == 'Slide' else ''}",
        Fore.CYAN    + f"3 - Zoom   {'(Actual)' if transicion_actual == 'Zoom' else ''}",
        Fore.YELLOW  + f"4 - Wipe   {'(Actual)' if transicion_actual == 'Wipe' else ''}",
        Fore.MAGENTA + f"5 - Flash  {'(Actual)' if transicion_actual == 'Flash' else ''}",
        Fore.RED     + "6 - Volver al menú principal"
    ]

    # Mostrar opciones con bordes
    print(Fore.MAGENTA + "╭" + "─" * 48)
    for opcion in opciones:
        print(Fore.MAGENTA + "│ " + opcion)
    print(Fore.MAGENTA + "╰" + "─" * 48)
    
    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    print(Fore.CYAN + "-> Ingresa el número de la opción: ", end="")

def menu_transiciones():
    """Controla la lógica del menú de transiciones."""
    ocultar_cursor()  # Ocultar cursor al entrar al menú

    while True:
        mostrar_menu_transiciones()

        # Mostrar cursor antes de solicitar entrada
        mostrar_cursor()
        eleccion = input().strip()
        ocultar_cursor()

        if eleccion in ["1", "2", "3", "4", "5"]:
            nueva_transicion = ["Fade", "Slide", "Zoom", "Wipe", "Flash"][int(eleccion) - 1]
            cambiar_transicion(nueva_transicion)
            print(Fore.GREEN + f"\n✅ Transición cambiada a: {nueva_transicion}")
            input(Fore.CYAN + "🔙 Presiona ENTER para volver al menú de transiciones...")
        elif eleccion == "6":
            break
        else:
            print(Fore.RED + "\n⚠️ Opción no válida. Inténtalo de nuevo.")

# Si se ejecuta directamente, inicia el menú
if __name__ == "__main__":
    menu_transiciones()

