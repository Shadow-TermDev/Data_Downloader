import os
import subprocess
from colorama import Fore, Style
from src.utils import pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def convertir_video(ruta_video, formato):
    ocultar_cursor()

    if not os.path.exists(ruta_video):
        print(Fore.RED + f"\nArchivo no encontrado:\n{ruta_video}")
        pausar()
        return

    nombre_base = os.path.splitext(ruta_video)[0]
    ruta_salida = f"{nombre_base}.{formato}"

    print(Fore.YELLOW + f"\nConvirtiendo video a .{formato.upper()}...")
    print(Fore.CYAN + "Esto puede tomar varios minutos...\n")

    comando = [
        "ffmpeg", "-i", ruta_video,
        "-c:v", "libx264" if formato in ["mp4", "mov"] else "copy",
        "-c:a", "aac" if formato in ["mp4", "mov"] else "copy",
        "-y", ruta_salida
    ]

    try:
        process = subprocess.Popen(comando, stderr=subprocess.PIPE, text=True, bufsize=1)
        for linea in process.stderr:
            if "frame=" in linea or "size=" in linea:
                print(f"\r{Fore.CYAN}{linea.strip()}", end="")
        process.wait()

        if process.returncode == 0:
            print(Fore.GREEN + f"\nVideo convertido exitosamente!")
            print(Fore.WHITE + f"Guardado como: {os.path.basename(ruta_salida)}")
        else:
            print(Fore.RED + "\nError durante la conversión.")

    except Exception as e:
        print(Fore.RED + f"\nError: {e}")
    finally:
        pausar()
