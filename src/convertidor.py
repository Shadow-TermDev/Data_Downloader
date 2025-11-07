import os
import shutil
import pyfiglet
from colorama import Fore, Style, init
from src.plugins.gestor_convertidor import convertir_video, convertir_video_a_audio, convertir_imagen, convertir_audio
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos funciones

# Inicializar colorama
init(autoreset=True)

# Ruta base para la búsqueda de archivos (ajustable)
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

# Mostrar menú del convertidor
def mostrar_submenu_convertidor():
    limpiar_pantalla()
    # Banner "Converter"
    titulo = pyfiglet.figlet_format("Converter", font="slant")
    for linea in titulo.split("\n"):
        print(Fore.YELLOW + centrar_texto(linea))
    print(Fore.CYAN + centrar_texto("VIDEO, AUDIO & IMAGE CONVERTER\n"))

    opciones = [
        (Fore.GREEN, "1 - Convertir Video 🎬"),
        (Fore.GREEN, "2 - Video a Audio 🎵"),
        (Fore.GREEN, "3 - Convertir Imagen 🖼️ "),
        (Fore.GREEN, "4 - Convertir Audio 🔊"),
        (Fore.RED, "5 - Volver al menú principal"),
    ]

    # Dibujar el cuadro del menú
    print(Fore.MAGENTA + "╭" + "─" * 48)
    for color, texto in opciones:
        print(Fore.MAGENTA + "│" + color + " " + texto)
    print(Fore.MAGENTA + "╰" + "─" * 48)

    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")

# Función para buscar archivos en la ruta base
def buscar_archivo(nombre_archivo):
    archivos_encontrados = []
    for root, _, files in os.walk(RUTA_BASE):
        if nombre_archivo in files:
            archivos_encontrados.append(os.path.join(root, nombre_archivo))

    if not archivos_encontrados:
        print(Fore.RED + f"❌ Archivo '{nombre_archivo}' no encontrado." + Style.RESET_ALL)
        return None

    if len(archivos_encontrados) == 1:
        return archivos_encontrados[0]

    print(Fore.YELLOW + "\n📂 Se encontraron múltiples archivos con el mismo nombre:")
    for i, archivo in enumerate(archivos_encontrados, 1):
        print(Fore.CYAN + f"  {i}. {archivo}")

    while True:
        mostrar_cursor()
        seleccion = input(Fore.CYAN + "\n🔢 Ingresa el número del archivo que deseas usar: ").strip()
        ocultar_cursor()
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(archivos_encontrados):
            return archivos_encontrados[int(seleccion) - 1]
        print(Fore.RED + "❌ Selección inválida. Inténtalo de nuevo." + Style.RESET_ALL)

# Función principal del menú de conversión
def menu_convertidor():
    ocultar_cursor()  # Ocultar cursor al entrar al menú

    opciones_convertidor = {
        "1": ("📂 Ingresa el nombre del video: ", convertir_video, ["mp4", "mkv", "avi"]),
        "2": ("📂 Ingresa el nombre del video para extraer el audio: ", convertir_video_a_audio, ["mp3", "wav", "ogg"]),
        "3": ("🖼️   Ingresa el nombre de la imagen: ", convertir_imagen, ["png", "jpg", "webp"]),
        "4": ("🔊 Ingresa el nombre del audio: ", convertir_audio, ["mp3", "wav", "ogg"]),
        "5": None,  # Opción para salir
    }

    while True:
        mostrar_submenu_convertidor()

        # Mostrar cursor antes de la entrada del usuario
        mostrar_cursor()
        opcion = input(Style.RESET_ALL).strip()
        ocultar_cursor()

        if opcion in opciones_convertidor:
            if opcion == "5":
                return  # Volver al menú principal

            mensaje, funcion_convertir, formatos_permitidos = opciones_convertidor[opcion]

            mostrar_cursor()
            nombre_archivo = input(Fore.YELLOW + f"\n{mensaje}").strip()
            ocultar_cursor()

            ruta_archivo = buscar_archivo(nombre_archivo)
            if ruta_archivo:
                while True:
                    mostrar_cursor()
                    formato = input(f"🎥 Ingresa el formato de salida ({', '.join(formatos_permitidos)}): ").strip().lower()
                    ocultar_cursor()

                    if formato in formatos_permitidos:
                        try:
                            funcion_convertir(ruta_archivo, formato)
                        except Exception as e:
                            print(Fore.RED + f"\n⚠️ Error en la conversión: {e}" + Style.RESET_ALL)
                        break
                    print(Fore.RED + f"❌ Formato inválido. Debe ser uno de: {', '.join(formatos_permitidos)}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n⚠️ Opción no válida. Inténtalo de nuevo." + Style.RESET_ALL)

# Ejecutar solo si el script se ejecuta directamente
if __name__ == "__main__":
    menu_convertidor()

