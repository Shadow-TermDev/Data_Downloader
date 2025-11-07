import os
import shutil
import pyfiglet
from colorama import Fore, Style, init
from src.plugins.gestor_descargas import descargar_video, descargar_audio, descargar_imagen
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

# Inicializar colorama para colores en la terminal
init(autoreset=True)

# Función para limpiar la pantalla en diferentes sistemas operativos
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

# Función para centrar texto en la terminal con manejo de error en entornos sin terminal
def centrar_texto(texto):
    try:
        ancho_terminal = shutil.get_terminal_size().columns
    except:
        ancho_terminal = 80  # Ancho por defecto si no hay terminal
    return texto.center(ancho_terminal)

# Función para mostrar el menú de descargas
def mostrar_menu_descargador():
    limpiar_pantalla()

    # Título "Downloader"
    titulo = pyfiglet.figlet_format("Downloader", font="slant")
    for linea in titulo.split("\n"):
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("📥 DESCARGA ARCHIVOS MULTIMEDIA 📥\n"))

    # Opciones del menú
    opciones = [
        (Fore.GREEN, "1 - Descargar video 🎬"),
        (Fore.GREEN, "2 - Descargar audio 🎵"),
        (Fore.GREEN, "3 - Descargar imagen 🖼️ "),
        (Fore.RED, "4 - Volver al menú principal"),
    ]

    # Dibujar cuadro del menú
    print(Fore.MAGENTA + "╭" + "─" * 48)
    for color, texto in opciones:
        print(Fore.MAGENTA + "│" + color + " " + texto)
    print(Fore.MAGENTA + "╰" + "─" * 48)

    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

# Función principal del menú de descargas
def menu_descargador():
    ocultar_cursor()  # Ocultar cursor al entrar al menú

    opciones_descarga = {
        "1": ("📂 Ingresa la URL del video: ", descargar_video),
        "2": ("📂 Ingresa la URL del audio: ", descargar_audio),
        "3": ("📂 Ingresa la URL de la imagen: ", descargar_imagen),
        "4": None,  # Opción para volver al menú principal
    }

    while True:
        mostrar_menu_descargador()

        # Mostrar cursor antes de solicitar entrada
        mostrar_cursor()
        opcion = input(Style.RESET_ALL).strip()
        ocultar_cursor()

        if opcion in opciones_descarga:
            if opcion == "4":
                return  # Volver al menú principal

            mensaje, funcion_descarga = opciones_descarga[opcion]

            # Mostrar cursor antes de solicitar la URL
            mostrar_cursor()
            url = input(mensaje).strip()
            ocultar_cursor()

            try:
                funcion_descarga(url)
            except Exception as e:
                print(Fore.RED + f"\n⚠️ Error en la descarga: {e}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n⚠️ Opción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

# Ejecutar solo si el script se ejecuta directamente
if __name__ == "__main__":
    menu_descargador()

