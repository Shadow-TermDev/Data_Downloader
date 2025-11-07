import os
import subprocess
from colorama import Fore, Style
from src.utils import BASE_AUDIOS as ruta_audios, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

def obtener_calidades_audio(url):
    """Obtiene las calidades de audio disponibles con sus bitrates."""
    try:
        resultado = subprocess.run(["yt-dlp", "-F", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if resultado.returncode != 0:
            print(Fore.RED + "\n❌ No se pudieron obtener las calidades de audio." + Style.RESET_ALL)
            return None

        calidades = {}
        for linea in resultado.stdout.split("\n"):
            partes = linea.split()
            if "audio only" in linea and len(partes) > 1:
                formato = partes[0]
                bitrate = partes[-1] if "k" in partes[-1] else "Desconocido"
                calidades[formato] = bitrate

        return calidades if calidades else None
    except Exception as e:
        print(Fore.RED + f"\n❌ Error al obtener calidades: {e}" + Style.RESET_ALL)
        return None

def mostrar_menu_calidades_audio(calidades):
    """Muestra las calidades de audio disponibles y permite elegir una."""
    if not calidades:
        print(Fore.RED + "\n❌ No hay calidades de audio disponibles." + Style.RESET_ALL)
        return None

    opciones = list(calidades.items())
    print(Fore.CYAN + "\n🎵 Calidades de audio disponibles:")
    for i, (formato, calidad) in enumerate(opciones, 1):
        print(Fore.GREEN + f" {i} - {calidad} ({formato})")

    while True:
        mostrar_cursor()  # Mostrar cursor antes de input
        opcion = input(Fore.CYAN + "\n-> Ingresa el número de la calidad deseada: " + Style.RESET_ALL).strip()
        ocultar_cursor()  # Ocultar cursor después de input

        if opcion.isdigit():
            opcion = int(opcion)
            if 1 <= opcion <= len(opciones):
                return opciones[opcion - 1][0]  # Retorna el formato elegido

        print(Fore.RED + "❌ Opción inválida. Intenta de nuevo." + Style.RESET_ALL)

def descargar_audio(url):
    """Descarga un audio en la calidad seleccionada."""
    ocultar_cursor()  # Ocultar cursor al iniciar

    try:
        print(Fore.YELLOW + "\n⏳ Obteniendo calidades disponibles..." + Style.RESET_ALL)
        calidades = obtener_calidades_audio(url)
        if not calidades:
            mostrar_cursor()  # Mostrar cursor antes de pausar
            pausar()
            ocultar_cursor()  # Ocultar cursor después de la entrada
            return

        calidad_seleccionada = mostrar_menu_calidades_audio(calidades)
        if not calidad_seleccionada:
            mostrar_cursor()  # Mostrar cursor antes de pausar
            pausar()
            ocultar_cursor()  # Ocultar cursor después de la entrada
            return

        print(Fore.YELLOW + "\n⏳ Descargando audio..." + Style.RESET_ALL)
        salida = os.path.join(ruta_audios, "%(title)s.%(ext)s")
        comando = [
            "yt-dlp", "-f", calidad_seleccionada, "--extract-audio",
            "--audio-format", "mp3", "--embed-thumbnail", "--add-metadata",
            "-o", salida, url
        ]

        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        destino = None
        for linea in resultado.stdout.splitlines():
            if "Destination:" in linea:
                destino = linea.split("Destination:")[-1].strip()
                break

        if resultado.returncode == 0:
            print(Fore.GREEN + "\n✅ Audio descargado correctamente." + Style.RESET_ALL)
            print(Fore.BLUE + f"\nArchivo guardado en: {destino}" + Style.RESET_ALL if destino else "\nNo se pudo determinar la ruta del archivo.")
        else:
            print(Fore.RED + "\n❌ Error en la descarga del audio." + Style.RESET_ALL)
            print(resultado.stderr)

    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {e}" + Style.RESET_ALL)

    mostrar_cursor()  # Mostrar cursor antes de pausar
    pausar()
    ocultar_cursor()  # Ocultar cursor después de la entrada

