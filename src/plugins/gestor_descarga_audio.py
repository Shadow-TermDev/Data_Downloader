import os
import subprocess
from colorama import Fore, Style
from src.utils import BASE_AUDIOS as ruta_audios, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def obtener_calidades_audio(url):
    try:
        result = subprocess.run(["yt-dlp", "-F", url], capture_output=True, text=True)
        if result.returncode != 0:
            return None

        calidades = []
        for linea in result.stdout.splitlines():
            if "audio only" in linea and "m4a" not in linea:
                partes = linea.split()
                if len(partes) >= 5:
                    formato = partes[0]
                    bitrate = partes[3] if "k" in partes[3] else "??k"
                    calidades.append((formato, bitrate))
        return calidades or None
    except:
        return None

def seleccionar_calidad(calidades):
    print(Fore.CYAN + "\nCalidades de audio disponibles:")
    for i, (formato, bitrate) in enumerate(calidades, 1):
        print(Fore.GREEN + f"  {i} - {bitrate} - formato {formato}")

    while True:
        mostrar_cursor()
        sel = input(Fore.CYAN + "\n  -> Elige una calidad [1-{}]: ".format(len(calidades)) + Style.RESET_ALL).strip()
        ocultar_cursor()
        if sel.isdigit() and 1 <= int(sel) <= len(calidades):
            return calidades[int(sel)-1][0]
        print(Fore.RED + "Opción inválida.")

def descargar_audio(url):
    ocultar_cursor()

    print(Fore.YELLOW + "\nObteniendo información del audio...")
    calidades = obtener_calidades_audio(url)

    if not calidades:
        print(Fore.RED + "\nNo se encontraron calidades de audio o URL inválida.")
        pausar()
        return

    formato = seleccionar_calidad(calidades)

    print(Fore.YELLOW + f"\nDescargando audio en la mejor calidad disponible...")
    print(Fore.CYAN + "Esto puede tardar unos segundos/minutos...\n")

    comando = [
        "yt-dlp", "-f", formato,
        "--extract-audio", "--audio-format", "mp3",
        "--embed-thumbnail", "--add-metadata",
        "-o", os.path.join(ruta_audios, "%(title)s.%(ext)s"),
        url
    ]

    result = subprocess.run(comando, capture_output=True, text=True)

    if result.returncode == 0:
        print(Fore.GREEN + "\nAudio descargado y convertido correctamente!")
    else:
        print(Fore.RED + "\nError durante la descarga.")
        print(Fore.RED + result.stderr.splitlines()[-3:])

    pausar()
