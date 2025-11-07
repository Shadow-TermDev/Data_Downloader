import os
from colorama import Fore, Style
from PIL import Image, ImageEnhance, ImageFilter
from src.utils import buscar_archivo, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor  # Importamos las funciones

def seleccionar_calidad():
    """Solicita al usuario la calidad de mejora y retorna los factores correspondientes."""
    opciones = {
        "1": (1.2, 1.1, 1.2),  # Baja calidad
        "2": (1.5, 1.3, 1.5),  # Calidad media
        "3": (2.0, 1.6, 2.0)   # Alta calidad
    }
    
    print(Fore.CYAN + "\n🔧 Selecciona la calidad:")
    print(Fore.GREEN + " 1 - Baja calidad (rápido)")
    print(Fore.YELLOW + " 2 - Calidad media (balanceado)")
    print(Fore.MAGENTA + " 3 - Alta calidad (procesamiento intenso)")

    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    seleccion = input(Fore.CYAN + "  -> Ingresa el número de la calidad: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    return opciones.get(seleccion, opciones["2"])  # Por defecto, calidad media

def generar_nombre_salida(nombre_original):
    """Genera un nuevo nombre para la imagen mejorada sin afectar la extensión."""
    base, extension = os.path.splitext(nombre_original)
    return f"{base}_mejorada{extension}"

def mejorar_imagen(ruta_imagen, factor_nitidez, factor_contraste, escala):
    """Aplica mejoras a la imagen según los factores seleccionados."""
    with Image.open(ruta_imagen) as imagen:
        nueva_resolucion = (int(imagen.width * escala), int(imagen.height * escala))
        imagen = imagen.resize(nueva_resolucion, Image.LANCZOS)
        imagen = imagen.filter(ImageFilter.DETAIL).filter(ImageFilter.SHARPEN)
        imagen = ImageEnhance.Sharpness(imagen).enhance(factor_nitidez)
        imagen = ImageEnhance.Contrast(imagen).enhance(factor_contraste)
        return imagen

def preguntar_eliminar_original(ruta_imagen):
    """Pregunta al usuario si desea eliminar la imagen original."""
    
    # Mostrar cursor antes de solicitar entrada
    mostrar_cursor()
    eleccion = input(Fore.YELLOW + "\n🗑️   ¿Eliminar archivo original? (s/n): " + Style.RESET_ALL).strip().lower()
    ocultar_cursor()

    if eleccion == "s":
        os.remove(ruta_imagen)
        print(Fore.GREEN + f"✅ Archivo original eliminado: {ruta_imagen}" + Style.RESET_ALL)

def mejorar_calidad_imagen(nombre_imagen):
    """Proceso principal para mejorar la calidad de una imagen."""
    ocultar_cursor()  # Ocultar cursor al iniciar la función

    try:
        ruta_imagen = buscar_archivo(nombre_imagen)
        if not ruta_imagen:
            print(Fore.RED + f"\n❌ No se encontró el archivo '{nombre_imagen}'." + Style.RESET_ALL)
            pausar()
            return

        factores = seleccionar_calidad()
        imagen_mejorada = mejorar_imagen(ruta_imagen, *factores)
        nueva_ruta = generar_nombre_salida(ruta_imagen)
        imagen_mejorada.save(nueva_ruta)

        print(Fore.GREEN + f"\n✅ Imagen mejorada guardada en: {nueva_ruta}" + Style.RESET_ALL)

        preguntar_eliminar_original(ruta_imagen)
        pausar()

    except Exception as e:
        print(Fore.RED + f"\n❌ Error al mejorar imagen: {e}" + Style.RESET_ALL)
        pausar()

