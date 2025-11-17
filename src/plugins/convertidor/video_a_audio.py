import os
import subprocess
from colorama import Fore, Style
from src.utils import pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

FORMATOS_VALIDOS = {"mp3", "wav", "aac", "flac", "ogg", "m4a"}
EXTENSION_REAL = {"mp3": "mp3", "wav": "wav", "flac": "flac", "ogg": "ogg", "m4a": "m4a", "aac": "m4a"}
FORMATOS_CON_PORTADA = {"mp3", "flac", "m4a", "aac", "ogg"}

def convertir_video_a_audio(ruta_video, formato):
    ocultar_cursor()

    try:
        if not os.path.exists(ruta_video):
            print(Fore.RED + f"\nArchivo no encontrado:\n{ruta_video}")
            pausar()
            return

        if formato not in FORMATOS_VALIDOS:
            print(Fore.RED + f"\nFormato no soportado.")
            pausar()
            return

        nombre_base = os.path.splitext(ruta_video)[0]
        extension = EXTENSION_REAL[formato]
        ruta_salida = f"{nombre_base}_audio.{extension}"

        titulo = "AAC → .M4A" if formato == "aac" else formato.upper()
        print(Fore.YELLOW + f"\nExtrayendo audio del video → {titulo}")
        print(Fore.CYAN + "Copiando portada y metadatos del video...\n")

        # COMANDO MÁGICO QUE SÍ FUNCIONA (orden crítico)
        comando = ["ffmpeg", "-i", ruta_video]

        # PRIMERO: portada (OBLIGATORIO antes del audio)
        if formato in FORMATOS_CON_PORTADA:
            if formato == "ogg":
                # OGG necesita PNG
                comando += ["-map", "0:v?", "-c:v", "png", "-disposition:v", "attached_pic"]
            else:
                # MP3, FLAC, M4A: copia directa
                comando += ["-map", "0:v?", "-c:v", "copy", "-disposition:v", "attached_pic"]

        # SEGUNDO: audio + sin video
        comando += ["-map", "0:a", "-vn"]

        # Códec de máxima calidad
        if formato == "mp3":
            comando += ["-c:a", "libmp3lame", "-b:a", "320k", "-q:a", "0"]
        elif formato == "wav":
            comando += ["-c:a", "pcm_s16le"]
        elif formato == "flac":
            comando += ["-c:a", "flac", "-compression_level", "8"]
        elif formato in ["aac", "m4a"]:
            comando += ["-c:a", "aac", "-b:a", "320k"]
        elif formato == "ogg":
            comando += ["-c:a", "libvorbis", "-q:a", "9"]

        # Metadatos al final
        comando += ["-map_metadata", "0", "-y", ruta_salida]

        # Ejecutar con progreso
        process = subprocess.Popen(comando, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

        for linea in process.stderr:
            if any(x in linea for x in ["time=", "size=", "bitrate=", "speed="]):
                print(f"\r{Fore.CYAN}{linea.strip():<90}", end="", flush=True)

        process.wait()

        # ÉXITO
        if os.path.exists(ruta_salida) and os.path.getsize(ruta_salida) > 100000:
            tamaño = os.path.getsize(ruta_salida) / (1024*1024)
            print(Fore.GREEN + f"\nAudio extraído con éxito!")
            if formato in FORMATOS_CON_PORTADA:
                print(Fore.GREEN + "   Portada del video COPIADA correctamente")
            else:
                print(Fore.YELLOW + "   WAV no soporta portada")
            print(Fore.WHITE + f"   Formato → {titulo}")
            print(Fore.WHITE + f"   Tamaño → {tamaño:.2f} MB")
            print(Fore.WHITE + f"   Guardado como: {os.path.basename(ruta_salida)}")

            # Pregunta eliminar original
            print(Fore.CYAN + f"\n¿Deseas eliminar el video original?")
            print(Fore.GREEN + "  1 - Sí, eliminar")
            print(Fore.RED + "  2 - No, conservar")
            while True:
                mostrar_cursor()
                choice = input(Fore.CYAN + f"\n  -> Tu elección [1-2]: " + Style.RESET_ALL).strip()
                ocultar_cursor()
                if choice == "1":
                    try:
                        os.remove(ruta_video)
                        print(Fore.GREEN + f"\nVideo eliminado.")
                    except:
                        print(Fore.RED + "\nError al eliminar.")
                    break
                elif choice == "2":
                    print(Fore.GREEN + f"\nVideo conservado.")
                    break

        else:
            print(Fore.RED + "\nFalló la extracción.")

    except Exception as e:
        print(Fore.RED + f"\nError: {e}")
    finally:
        pausar()
