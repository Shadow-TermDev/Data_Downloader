import os
from colorama import Fore, Style
from src.plugins.convertidor.utils import ejecutar_comando
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

FORMATOS_VALIDOS = {"mp3", "wav", "aac", "flac", "ogg", "m4a"}

def convertir_audio(ruta_audio, formato):
    """Convierte un archivo de audio al formato deseado."""
    ocultar_cursor()  # Ocultar cursor al iniciar

    if not os.path.exists(ruta_audio):
        print(Fore.RED + f"\n❌ Error: El archivo '{ruta_audio}' no existe." + Style.RESET_ALL)
        mostrar_cursor()  # Mostrar cursor antes de salir
        return

    if formato not in FORMATOS_VALIDOS:
        print(Fore.RED + f"\n❌ Error: Formato '{formato}' no soportado. Usa uno de: {', '.join(FORMATOS_VALIDOS)}" + Style.RESET_ALL)
        mostrar_cursor()  # Mostrar cursor antes de salir
        return

    ruta_salida = f"{os.path.splitext(ruta_audio)[0]}.{formato}"
    comando = ["ffmpeg", "-i", ruta_audio, ruta_salida, "-y"]

    print(Fore.YELLOW + f"\n🔊 Convirtiendo audio a {formato}..." + Style.RESET_ALL)
    ejecutar_comando(comando, ruta_salida)

    mostrar_cursor()  # Mostrar cursor al finalizar

