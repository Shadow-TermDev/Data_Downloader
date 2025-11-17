import os
from PIL import Image
from colorama import Fore, Style
from src.utils import pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

# Formatos soportados
FORMATOS_VALIDOS = {"png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp", "ico"}

# Parámetros de calidad por formato
CALIDAD_POR_FORMATO = {
    "jpg": {"quality": 95, "optimize": True, "progressive": True},
    "jpeg": {"quality": 95, "optimize": True, "progressive": True},
    "webp": {"quality": 95, "lossless": False, "method": 6},
    "png": {"compress_level": 6, "optimize": True},
    "tiff": {"compression": "tiff_adobe_deflate"},
    "bmp": {},
    "gif": {"optimize": True},
    "ico": {"sizes": [(256, 256)]},
}

def convertir_imagen(ruta_imagen, formato):
    ocultar_cursor()

    try:
        if not os.path.exists(ruta_imagen):
            print(Fore.RED + f"\nArchivo no encontrado:\n{ruta_imagen}")
            pausar()
            return

        formato = formato.lower()
        if formato == "jpeg":
            formato = "jpg"  # PIL usa "jpg" internamente

        if formato not in FORMATOS_VALIDOS:
            print(Fore.RED + f"\nFormato no soportado: {formato.upper()}")
            print(Fore.YELLOW + f"Disponibles: {', '.join(sorted(FORMATOS_VALIDOS))}")
            pausar()
            return

        nombre_base = os.path.splitext(ruta_imagen)[0]
        ruta_salida = f"{nombre_base}_convertida.{formato}"

        print(Fore.YELLOW + f"\nConvirtiendo imagen → .{formato.upper()}")
        print(Fore.CYAN + "Preservando calidad máxima y transparencia (si aplica)...\n")

        with Image.open(ruta_imagen) as img:
            # Convertir a RGB si es necesario (para JPG, etc.)
            if formato in ["jpg", "jpeg", "webp"] and img.mode in ("RGBA", "LA", "P"):
                print(Fore.CYAN + "Fondo blanco aplicado (formato no soporta transparencia)")
                fondo = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                fondo.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
                img = fondo
            elif img.mode not in ("RGB", "RGBA", "L", "P"):
                img = img.convert("RGB")

            # Parámetros específicos
            save_kwargs = CALIDAD_POR_FORMATO.get(formato, {})

            # Forzar formato correcto para ICO
            if formato == "ico":
                img = img.resize((256, 256), Image.LANCZOS)

            # Guardar
            img.save(ruta_salida, **save_kwargs)

        # Info del archivo
        tamaño_original = os.path.getsize(ruta_imagen) / (1024*1024)
        tamaño_nuevo = os.path.getsize(ruta_salida) / (1024*1024)

        print(Fore.GREEN + f"\nImagen convertida exitosamente!")
        print(Fore.WHITE + f"   Formato → {formato.upper()}")
        print(Fore.WHITE + f"   Tamaño original → {tamaño_original:.2f} MB")
        print(Fore.WHITE + f"   Tamaño final    → {tamaño_nuevo:.2f} MB")
        print(Fore.WHITE + f"   Reducción → {((tamaño_original - tamaño_nuevo) / tamaño_original * 100):.1f}%")
        print(Fore.WHITE + f"   Guardado como → {os.path.basename(ruta_salida)}")

        # Pregunta eliminar original (igual que todos)
        print(Fore.CYAN + f"\n¿Deseas eliminar la imagen original?")
        print(Fore.GREEN + "  1 - Sí, eliminar")
        print(Fore.RED + "  2 - No, conservar")
        while True:
            mostrar_cursor()
            choice = input(Fore.CYAN + f"\n  -> Tu elección [1-2]: " + Style.RESET_ALL).strip()
            ocultar_cursor()
            if choice == "1":
                try:
                    os.remove(ruta_imagen)
                    print(Fore.GREEN + f"\nOriginal eliminado.")
                except:
                    print(Fore.RED + "\nError al eliminar.")
                break
            elif choice == "2":
                print(Fore.GREEN + f"\nOriginal conservado.")
                break
            else:
                print(Fore.RED + "Opción inválida.")

    except Exception as e:
        print(Fore.RED + f"\nError al convertir: {e}")
    finally:
        pausar()
