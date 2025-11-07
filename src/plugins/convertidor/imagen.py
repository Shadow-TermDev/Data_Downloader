import os
from PIL import Image
from colorama import Fore, Style
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

FORMATOS_VALIDOS = {"png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"}

def convertir_imagen(ruta_imagen, formato):
    """Convierte una imagen al formato deseado."""
    ocultar_cursor()  # Ocultar cursor al iniciar

    if not os.path.exists(ruta_imagen):
        print(Fore.RED + f"\n❌ Error: El archivo '{ruta_imagen}' no existe." + Style.RESET_ALL)
        mostrar_cursor()  # Mostrar cursor antes de salir
        return

    if formato.lower() not in FORMATOS_VALIDOS:
        print(Fore.RED + f"\n❌ Error: Formato '{formato}' no soportado. Usa uno de: {', '.join(FORMATOS_VALIDOS)}" + Style.RESET_ALL)
        mostrar_cursor()  # Mostrar cursor antes de salir
        return

    ruta_salida = f"{os.path.splitext(ruta_imagen)[0]}.{formato.lower()}"

    try:
        with Image.open(ruta_imagen) as img:
            img.save(ruta_salida, format=formato.upper())
        print(Fore.GREEN + f"\n✅ Imagen convertida y guardada en: {ruta_salida}" + Style.RESET_ALL)
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error al convertir la imagen: {e}" + Style.RESET_ALL)

    mostrar_cursor()  # Mostrar cursor al finalizar

