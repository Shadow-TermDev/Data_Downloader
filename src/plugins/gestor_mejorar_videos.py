import os
import subprocess
from colorama import Fore, Style
from src.utils import buscar_archivo, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

def obtener_resolucion():
    """Solicita al usuario la resolución deseada y la retorna."""
    print(Fore.CYAN + "\n🔧 Selecciona la calidad:")
    opciones = {
        "1": ("1280x720", "720p (HD, buena calidad)"),
        "2": ("1920x1080", "1080p (Full HD, alta calidad)"),
        "3": ("3840x2160", "4K (Ultra HD, máximo detalle)")
    }
    for key, (_, descripcion) in opciones.items():
        print(Fore.GREEN + f" {key} - {descripcion}")

    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    eleccion = input(Fore.CYAN + "  -> Ingresa el número de la calidad: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    if eleccion not in opciones:
        print(Fore.RED + "\n⚠️ Opción no válida. Usando 1080p por defecto." + Style.RESET_ALL)
        eleccion = "2"

    return opciones[eleccion][0]

def generar_nombre_salida(nombre_original):
    """Genera un nombre de archivo nuevo para el video mejorado."""
    base, extension = os.path.splitext(nombre_original)
    return f"{base}_mejorado{extension}"

def ejecutar_ffmpeg(ruta_video, nueva_ruta, resolucion):
    """Ejecuta el comando ffmpeg para mejorar la calidad del video."""
    comando = [
        "ffmpeg", "-i", ruta_video,
        "-vf", f"scale={resolucion}",
        "-preset", "slow",
        "-crf", "18",
        nueva_ruta
    ]
    print(Fore.YELLOW + f"\n⏳ Mejorando calidad a {resolucion}...")

    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if resultado.returncode == 0:
        print(Fore.GREEN + f"\n✅ Video mejorado guardado en: {nueva_ruta}" + Style.RESET_ALL)
        return True
    else:
        print(Fore.RED + "\n❌ Error al mejorar el video." + Style.RESET_ALL)
        print(resultado.stderr)
        return False

def preguntar_eliminar_original(ruta_video):
    """Pregunta al usuario si desea eliminar el video original."""
    print(Fore.YELLOW + "\n🗑️   ¿Quieres eliminar el archivo original?")
    print(Fore.GREEN + " 1 - Sí")
    print(Fore.RED + " 2 - No")

    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    eleccion = input(Fore.CYAN + "  -> Ingresa tu elección: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    if eleccion == "1":
        os.remove(ruta_video)
        print(Fore.GREEN + f"\n✅ Archivo original eliminado: {ruta_video}" + Style.RESET_ALL)

def mejorar_calidad_video(nombre_video):
    """Proceso principal para mejorar la calidad de un video."""
    ocultar_cursor()  # Ocultar cursor al iniciar la función

    try:
        ruta_video = buscar_archivo(nombre_video)
        if not ruta_video:
            print(Fore.RED + f"\n❌ No se encontró el archivo '{nombre_video}'. Asegúrate de escribirlo bien." + Style.RESET_ALL)
            pausar()
            return

        resolucion = obtener_resolucion()
        nueva_ruta = generar_nombre_salida(ruta_video)

        if ejecutar_ffmpeg(ruta_video, nueva_ruta, resolucion):
            preguntar_eliminar_original(ruta_video)

        pausar()

    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {e}" + Style.RESET_ALL)
        pausar()

