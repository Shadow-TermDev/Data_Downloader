import os
import subprocess
from colorama import Fore, Style
from src.utils import pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

FORMATOS_VALIDOS = {"mp3", "wav", "aac", "flac", "ogg", "m4a"}
FORMATOS_CON_PORTADA = {"mp3", "flac", "m4a", "aac", "ogg"}

# Extensión real según formato
EXTENSION_REAL = {
    "mp3": "mp3",
    "wav": "wav",
    "flac": "flac",
    "ogg": "ogg",
    "m4a": "m4a",
    "aac": "m4a",
}

def convertir_audio(ruta_audio, formato):
    ocultar_cursor()

    try:
        if not os.path.exists(ruta_audio):
            print(Fore.RED + f"\nArchivo no encontrado:\n{ruta_audio}")
            pausar()
            return

        if formato not in FORMATOS_VALIDOS:
            print(Fore.RED + f"\nFormato no soportado.")
            pausar()
            return

        nombre_base = os.path.splitext(ruta_audio)[0]
        extension = EXTENSION_REAL[formato]
        ruta_salida = f"{nombre_base}_convertido.{extension}"

        titulo = "AAC → .M4A" if formato == "aac" else formato.upper()
        print(Fore.YELLOW + f"\nConvirtiendo a {titulo}")
        print(Fore.CYAN + "Preservando portada y metadatos...\n")

        comando = ["ffmpeg", "-i", ruta_audio]

        # PORTADA: TRUCO ESPECIAL PARA OGG (conversión a PNG si es necesario)
        if formato in FORMATOS_CON_PORTADA:
            if formato == "ogg":
                # Para OGG: forzamos PNG (el más compatible)
                comando += ["-map", "0:v?", "-c:v", "png", "-disposition:v", "attached_pic"]
            else:
                # Para MP3, FLAC, M4A: copia directa
                comando += ["-map", "0:v?", "-c:v", "copy", "-disposition:v", "attached_pic"]

        comando += ["-map", "0:a"]

        # Códec de audio
        if formato == "mp3":
            comando += ["-c:a", "libmp3lame", "-b:a", "320k"]
        elif formato == "wav":
            comando += ["-c:a", "pcm_s16le"]
        elif formato == "flac":
            comando += ["-c:a", "flac", "-compression_level", "8"]
        elif formato in ["aac", "m4a"]:
            comando += ["-c:a", "aac", "-b:a", "320k"]
        elif formato == "ogg":
            comando += ["-c:a", "libvorbis", "-q:a", "9"]

        comando += ["-map_metadata", "0", "-y", ruta_salida]

        process = subprocess.Popen(comando, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

        for linea in process.stderr:
            if any(x in linea for x in ["time=", "size=", "bitrate=", "speed="]):
                print(f"\r{Fore.CYAN}{linea.strip():<90}", end="", flush=True)

        process.wait()

        if os.path.exists(ruta_salida) and os.path.getsize(ruta_salida) > 50000:
            tamaño = os.path.getsize(ruta_salida) / (1024*1024)
            print(Fore.GREEN + f"\nAudio convertido exitosamente!")
            if formato in FORMATOS_CON_PORTADA:
                print(Fore.GREEN + "   Portada preservada correctamente")
            else:
                print(Fore.YELLOW + "   WAV no soporta portada")
            print(Fore.WHITE + f"   Formato → {titulo}")
            print(Fore.WHITE + f"   Tamaño → {tamaño:.2f} MB")
            print(Fore.WHITE + f"   Guardado como: {os.path.basename(ruta_salida)}")

            # Pregunta eliminar original
            print(Fore.CYAN + f"\n¿Deseas eliminar el audio original?")
            print(Fore.GREEN + "  1 - Sí, eliminar")
            print(Fore.RED + "  2 - No, conservar")
            while True:
                mostrar_cursor()
                choice = input(Fore.CYAN + f"\n  -> Tu elección [1-2]: " + Style.RESET_ALL).strip()
                ocultar_cursor()
                if choice == "1":
                    try:
                        os.remove(ruta_audio)
                        print(Fore.GREEN + f"\nOriginal eliminado.")
                    except:
                        print(Fore.RED + "\nError al eliminar.")
                    break
                elif choice == "2":
                    print(Fore.GREEN + f"\nOriginal conservado.")
                    break
                else:
                    print(Fore.RED + "Opción inválida.")

        else:
            print(Fore.RED + "\nFalló la conversión.")

    except Exception as e:
        print(Fore.RED + f"\nError: {e}")
    finally:
        pausar()
