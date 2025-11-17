import os
from PIL import Image, ImageEnhance, ImageFilter
from colorama import Fore, Style
from src.utils import pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def seleccionar_calidad():
    print(Fore.CYAN + "\nSelecciona la calidad de mejora:")
    opciones = {
        "1": ((1.2, 1.1, 1.2), "1.2x - Rápido"),
        "2": ((1.5, 1.3, 1.5), "1.5x - Balanceado (recomendado)"),
        "3": ((2.0, 1.6, 2.0), "2.0x - Máxima calidad")
    }
    
    for k, (_, desc) in opciones.items():
        color = Fore.GREEN if k == "1" else Fore.YELLOW if k == "2" else Fore.MAGENTA
        print(color + f"  {k} - {desc}")

    mostrar_cursor()
    choice = input(Fore.CYAN + "\n  -> Elige una opción [1-3]: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    return opciones.get(choice, opciones["2"])[0]  # Por defecto: balanceado


def generar_nombre_salida(ruta_original):
    base, ext = os.path.splitext(ruta_original)
    return f"{base}_mejorada{ext}"


def mejorar_imagen(ruta_entrada, escala, contraste, nitidez):
    try:
        with Image.open(ruta_entrada) as img:
            # Redimensionar con LANCZOS (mejor calidad)
            nuevo_ancho = int(img.width * escala)
            nuevo_alto = int(img.height * escala)
            img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

            # Mejorar detalles y nitidez
            img = img.filter(ImageFilter.DETAIL)
            img = img.filter(ImageFilter.SHARPEN)
            img = ImageEnhance.Sharpness(img).enhance(nitidez)
            img = ImageEnhance.Contrast(img).enhance(contraste)

            # Mantener metadatos EXIF si existen
            exif = img.info.get("exif")
            return img, exif
    except Exception as e:
        print(Fore.RED + f"Error al procesar la imagen: {e}")
        return None, None


def preguntar_eliminar_original(ruta):
    print(Fore.YELLOW + "\n¿Deseas eliminar la imagen original?")
    print(Fore.GREEN + "  1 - Sí, eliminar")
    print(Fore.RED + "  2 - No, conservar")

    mostrar_cursor()
    choice = input(Fore.CYAN + "\n  -> Tu elección [1-2]: " + Style.RESET_ALL).strip()
    ocultar_cursor()

    if choice == "1":
        try:
            os.remove(ruta)
            print(Fore.GREEN + "Imagen original eliminada.")
        except:
            print(Fore.RED + "No se pudo eliminar el archivo original.")


def mejorar_calidad_imagen(ruta_imagen):
    """
    Recibe la ruta completa del archivo (gracias a buscar_archivo)
    """
    ocultar_cursor()

    try:
        if not os.path.exists(ruta_imagen):
            print(Fore.RED + f"\nNo se encontró la imagen:\n{ruta_imagen}")
            pausar()
            return

        print(Fore.CYAN + f"\nProcesando: {os.path.basename(ruta_imagen)}")
        
        escala, contraste, nitidez = seleccionar_calidad()
        salida = generar_nombre_salida(ruta_imagen)

        print(Fore.YELLOW + f"\nMejorando imagen ×{escala} (nitidez + contraste)...")
        print(Fore.CYAN + "Esto puede tomar unos segundos...\n")

        img_mejorada, exif = mejorar_imagen(ruta_imagen, escala, contraste, nitidez)
        
        if img_mejorada is None:
            pausar()
            return

        # Guardar con máxima calidad y preservando EXIF
        save_params = {"quality": 95, "optimize": True, "progressive": True}
        if exif:
            save_params["exif"] = exif

        img_mejorada.save(salida, **save_params)

        print(Fore.GREEN + f"\nImagen mejorada con éxito!")
        print(Fore.WHITE + f"Guardado como: {os.path.basename(salida)}")
        print(Fore.CYAN + f"Resolución: {img_mejorada.width}×{img_mejorada.height} píxeles")

        preguntar_eliminar_original(ruta_imagen)

    except Exception as e:
        print(Fore.RED + f"\nError inesperado: {e}")
    finally:
        pausar()  # ← Siempre espera Enter al final
