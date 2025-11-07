import os
import shlex
import subprocess
from colorama import Fore, Style
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def convertir_video(ruta_video, formato):
    """Convierte un video a otro formato usando ffmpeg."""
    ocultar_cursor()  # Ocultar cursor al iniciar

    if not os.path.exists(ruta_video):
        print(Fore.RED + f"\n❌ Archivo no encontrado: {ruta_video}" + Style.RESET_ALL)
        mostrar_cursor()  # Mostrar cursor antes de salir
        return

    ruta_salida = f"{os.path.splitext(ruta_video)[0]}.{formato}"
    comando = ["ffmpeg", "-i", ruta_video, ruta_salida, "-y"]

    print(Fore.YELLOW + f"\n🎬 Convirtiendo video a {formato}..." + Style.RESET_ALL)

    try:
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if resultado.returncode == 0:
            print(Fore.GREEN + f"\n✅ Video convertido y guardado en: {ruta_salida}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n❌ Error en la conversión del video." + Style.RESET_ALL)
            print(resultado.stderr)

    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {e}" + Style.RESET_ALL)

    mostrar_cursor()  # Mostrar cursor al finalizar

