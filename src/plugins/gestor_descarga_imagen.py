import os
import requests
from PIL import Image
from io import BytesIO
from colorama import Fore, Style
from src.utils import BASE_IMAGENES as ruta_imagenes, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

def obtener_calidad_imagen(url):
    """Obtiene la resolución y el formato de la imagen antes de descargarla."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lanza error si la respuesta no es 200
        imagen = Image.open(BytesIO(response.content))
        return imagen, imagen.size, imagen.format  # Retornamos la imagen para evitar hacer otra petición
    except requests.RequestException as e:
        print(Fore.RED + f"\n❌ Error al obtener calidad de la imagen: {e}" + Style.RESET_ALL)
        return None, None, None

def limpiar_nombre_archivo(url, formato):
    """Genera un nombre de archivo válido a partir de la URL y el formato."""
    nombre = os.path.basename(url.split("?")[0])  # Elimina parámetros de URL
    if not nombre or "." not in nombre:  # Si no tiene extensión
        nombre += f".{formato.lower()}" if formato else ".jpg"
    return nombre

def descargar_imagen(url):
    """Descarga una imagen desde una URL y la guarda en el sistema."""
    ocultar_cursor()  # Ocultar cursor al iniciar

    try:
        print(Fore.YELLOW + "\n⏳ Obteniendo calidad de la imagen..." + Style.RESET_ALL)
        imagen, resolucion, formato = obtener_calidad_imagen(url)
        if not imagen:
            print(Fore.RED + "\n❌ No se pudo obtener la calidad de la imagen." + Style.RESET_ALL)
            mostrar_cursor()  # Mostrar cursor antes de pausar
            pausar()
            ocultar_cursor()  # Ocultar cursor después de la entrada
            return

        print(Fore.CYAN + f"\n🖼️    Calidad disponible: {resolucion[0]}x{resolucion[1]} - Formato: {formato}" + Style.RESET_ALL)
        nombre_archivo = limpiar_nombre_archivo(url, formato)
        ruta_completa = os.path.join(ruta_imagenes, nombre_archivo)
        imagen.save(ruta_completa, formato if formato else "JPEG")  # Guarda la imagen con su formato original

        print(Fore.GREEN + "\n✅ Imagen descargada correctamente." + Style.RESET_ALL)
        print(Fore.BLUE + f"\nArchivo guardado en: {ruta_completa}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {e}" + Style.RESET_ALL)

    mostrar_cursor()  # Mostrar cursor antes de pausar
    pausar()
    ocultar_cursor()  # Ocultar cursor después de la entrada

