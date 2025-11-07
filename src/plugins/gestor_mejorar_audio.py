import os
import subprocess
from colorama import Fore, Style
from src.utils import buscar_archivo, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

def seleccionar_calidad():
    """Solicita al usuario la calidad de mejora y retorna el bitrate correspondiente."""
    opciones = {
        "1": "128k",  # Calidad estándar
        "2": "256k",  # Alta calidad
        "3": "320k"   # Calidad máxima
    }
    
    print(Fore.CYAN + "\n🔧 Selecciona la calidad:")
    print(Fore.GREEN + " 1 - Calidad estándar (128 kbps)")
    print(Fore.YELLOW + " 2 - Alta calidad (256 kbps)")
    print(Fore.MAGENTA + " 3 - Calidad máxima (320 kbps)")

    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    seleccion = input(Fore.CYAN + "  -> Ingresa el número de la calidad: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    return opciones.get(seleccion, "256k")  # Por defecto, calidad alta

def generar_nombre_salida(nombre_original):
    """Genera un nuevo nombre para el audio mejorado sin afectar la extensión."""
    base, extension = os.path.splitext(nombre_original)
    return f"{base}_mejorado{extension}"

def mejorar_audio(ruta_audio, nuevo_bitrate):
    """Ejecuta el comando FFmpeg para mejorar la calidad del audio."""
    nueva_ruta = generar_nombre_salida(ruta_audio)
    print(Fore.YELLOW + f"\n⏳ Mejorando calidad a {nuevo_bitrate}...")

    comando_ffmpeg = [
        "ffmpeg", "-i", ruta_audio,
        "-b:a", nuevo_bitrate,
        nueva_ruta
    ]

    resultado = subprocess.run(comando_ffmpeg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if resultado.returncode == 0:
        return nueva_ruta
    else:
        print(Fore.RED + "\n❌ Error al mejorar el audio:" + Style.RESET_ALL)
        print(resultado.stderr)
        return None

def preguntar_eliminar_original(ruta_audio):
    """Pregunta al usuario si desea eliminar el audio original."""
    
    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    eleccion = input(Fore.YELLOW + "\n🗑️   ¿Eliminar archivo original? (s/n): " + Style.RESET_ALL).strip().lower()
    ocultar_cursor()

    if eleccion == "s":
        os.remove(ruta_audio)
        print(Fore.GREEN + f"✅ Archivo original eliminado: {ruta_audio}" + Style.RESET_ALL)

def mejorar_calidad_audio(nombre_audio):
    """Proceso principal para mejorar la calidad de un archivo de audio."""
    ocultar_cursor()  # Ocultar cursor al iniciar la función

    try:
        ruta_audio = buscar_archivo(nombre_audio)
        if not ruta_audio:
            print(Fore.RED + f"\n❌ No se encontró el archivo '{nombre_audio}'." + Style.RESET_ALL)
            pausar()
            return

        nuevo_bitrate = seleccionar_calidad()
        nueva_ruta = mejorar_audio(ruta_audio, nuevo_bitrate)

        if nueva_ruta:
            print(Fore.GREEN + f"\n✅ Audio mejorado guardado en: {nueva_ruta}" + Style.RESET_ALL)
            preguntar_eliminar_original(ruta_audio)

        pausar()

    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {e}" + Style.RESET_ALL)
        pausar()

