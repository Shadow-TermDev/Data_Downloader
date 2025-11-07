import os
import shutil
import pyfiglet
from colorama import Fore, Style, init
from src.plugins.gestor_mejorar_imagen import mejorar_calidad_imagen
from src.plugins.gestor_mejorar_audio import mejorar_calidad_audio
from src.plugins.gestor_mejorar_videos import mejorar_calidad_video
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

# Inicializar colorama para colores en la terminal
init(autoreset=True)

# Ruta base donde se almacenan los archivos
RUTA_BASE = "/storage/emulated/0/"

# Función para limpiar la pantalla en Windows y Linux/Termux
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

# Función para centrar texto en la terminal
def centrar_texto(texto):
    try:
        ancho_terminal = shutil.get_terminal_size().columns
    except:
        ancho_terminal = 80  # Ancho por defecto si no hay terminal
    return texto.center(ancho_terminal)

# Mostrar el menú del mejorador
def mostrar_submenu_mejorador():
    limpiar_pantalla()

    # Banner "Quality Boost"
    titulo = pyfiglet.figlet_format("Quality Boost", font="slant")
    for linea in titulo.split("\n"):
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("IMPROVE IMAGE, VIDEO & AUDIO QUALITY\n"))

    opciones = [
        (Fore.GREEN, "1 - Mejorar calidad de video 🎬"),
        (Fore.GREEN, "2 - Mejorar calidad de audio 🎵"),
        (Fore.GREEN, "3 - Mejorar calidad de imagen 🖼️ "),
        (Fore.RED, "4 - Volver al menú principal"),
    ]

    # Dibujar el cuadro del menú
    print(Fore.MAGENTA + "╭" + "─" * 50)
    for color, texto in opciones:
        print(Fore.MAGENTA + "│" + color + " " + texto)
    print(Fore.MAGENTA + "╰" + "─" * 50)

    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

# Función para verificar si un archivo existe
def buscar_archivo(nombre_archivo):
    ruta_archivo = os.path.join(RUTA_BASE, nombre_archivo)
    if not os.path.exists(ruta_archivo):
        print(Fore.RED + f"\n❌ El archivo '{nombre_archivo}' no existe en {RUTA_BASE}." + Style.RESET_ALL)
        return None
    return ruta_archivo

# Menú principal de mejoras
def menu_mejorador():
    ocultar_cursor()  # Ocultar cursor al entrar al menú

    opciones_mejorador = {
        "1": ("📂 Ingresa el nombre del video: ", mejorar_calidad_video),
        "2": ("📂 Ingresa el nombre del audio: ", mejorar_calidad_audio),
        "3": ("📂 Ingresa el nombre de la imagen: ", mejorar_calidad_imagen),
        "4": None,  # Salir
    }

    while True:
        mostrar_submenu_mejorador()

        # Mostrar cursor antes de solicitar entrada
        mostrar_cursor()
        opcion = input(Style.RESET_ALL).strip()
        ocultar_cursor()

        if opcion in opciones_mejorador:
            if opcion == "4":
                return  # Volver al menú principal

            mensaje, funcion_mejorar = opciones_mejorador[opcion]

            # Mostrar cursor antes de solicitar el archivo
            mostrar_cursor()
            nombre_archivo = input(Fore.YELLOW + f"\n{mensaje}").strip()
            ocultar_cursor()

            ruta_archivo = buscar_archivo(nombre_archivo)
            if ruta_archivo:
                try:
                    funcion_mejorar(ruta_archivo)
                except Exception as e:
                    print(Fore.RED + f"\n⚠️ Error al mejorar la calidad: {e}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n⚠️ Opción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

# Función para pausar la pantalla antes de volver al menú
def pausar():
    mostrar_cursor()
    input(Fore.CYAN + "\n🔹 Presiona ENTER para volver al menú..." + Style.RESET_ALL)
    ocultar_cursor()

# Ejecutar solo si el script se ejecuta directamente
if __name__ == "__main__":
    menu_mejorador()

