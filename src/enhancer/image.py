"""
Image quality enhancement module
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
from colorama import Fore, Style

from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.utils.boxes import print_success_box, print_selection_box
from src.core.file_manager import generar_nombre_salida, eliminar_archivo_seguro


def seleccionar_calidad() -> tuple:
    """
    Let the user pick el nivel de mejora
    
    Returns:
        Tuple with (escala, contraste, nitidez)
    """
    opciones = [
        ("1", (1.2, 1.1, 1.2), "×1.2 - Fast", "Light enhancement"),
        ("2", (1.5, 1.3, 1.5), "×1.5 - Balanced", "Recommended"),
        ("3", (2.0, 1.6, 2.0), "×2.0 - Max quality", "Takes longer")
    ]

    lineas = []
    colores = []
    for num, valores, label, desc in opciones:
        estrella = "⭐ " if num == "2" else "   "
        lineas.append(f"{estrella}{num}. {label} - {desc}")
        colores.append(Fore.GREEN if num == "2" else Fore.WHITE)

    print_selection_box("🖼️  ENHANCEMENT LEVEL", lineas, colores)
    
    while True:
        mostrar_cursor()
        choice = input(Fore.CYAN + "\n➜ Pick [1-3] (2=recommended): " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        opciones_dict = {
            "1": (1.2, 1.1, 1.2),
            "2": (1.5, 1.3, 1.5),
            "3": (2.0, 1.6, 2.0)
        }
        
        if choice in opciones_dict:
            return opciones_dict[choice]
        
        print(Fore.RED + "❌ Invalid option")


def mejorar_imagen(ruta_entrada: Path, escala: float, contraste: float, nitidez: float) -> tuple:
    """
    Enhance an image with upscaling and filters
    
    Args:
        ruta_entrada: Image Path
        escala: Factor de escala
        contraste: Factor de contraste
        nitidez: Factor de nitidez
        
    Returns:
        Tuple with (imagen_enhanced, exif_data)
    """
    try:
        with Image.open(ruta_entrada) as img:
            # Obtener EXIF si existe
            exif = img.info.get("exif")
            
            # Calcular nuevo tamaño
            nuevo_ancho = int(img.width * escala)
            nuevo_alto = int(img.height * escala)
            
            print(Fore.CYAN + f"   📐 Original resolution: {img.width}×{img.height} px")
            print(Fore.CYAN + f"   📐 New resolution: {nuevo_ancho}×{nuevo_alto} px")
            
            # Redimensionar con Lanczos (mejor calidad)
            print(Fore.YELLOW + "   🔄 Applying Lanczos upscaling...")
            img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
            
            # Aplicar filtros de mejora
            print(Fore.YELLOW + "   ✨ Applying enhancement filters...")
            
            # Filtro de detalles
            img = img.filter(ImageFilter.DETAIL)
            
            # Nitidez
            img = img.filter(ImageFilter.SHARPEN)
            img = ImageEnhance.Sharpness(img).enhance(nitidez)
            
            # Contraste
            img = ImageEnhance.Contrast(img).enhance(contraste)
            
            return img, exif
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error al procesar: {str(e)}")
        return None, None


def mejorar_calidad_imagen(ruta_imagen: Path):
    """
    Enhance image quality via upscaling and filters
    
    Args:
        ruta_imagen: Original image Path
    """
    ocultar_cursor()
    
    try:
        if not ruta_imagen.exists():
            print(Fore.RED + f"\n❌ File not found: {ruta_imagen}")
            return
        
        print(Fore.CYAN + f"\n📸 Processing: {ruta_imagen.name}")
        
        escala, contraste, nitidez = seleccionar_calidad()
        
        ruta_salida = generar_nombre_salida(ruta_imagen, "_enhanced")
        
        print(Fore.YELLOW + f"\n⬆️  Enhancing image ×{escala}...")
        print(Fore.CYAN + "⏳ Applying sharpness, contrast and upscaling...\n")
        
        img_enhanced, exif = mejorar_imagen(ruta_imagen, escala, contraste, nitidez)
        
        if img_enhanced is None:
            return
        
        # Guardar con máxima calidad
        print(Fore.YELLOW + "\n💾 Saving image enhanced...")
        save_params = {
            "quality": 95,
            "optimize": True,
            "progressive": True
        }
        
        # Preservar EXIF si existe
        if exif:
            save_params["exif"] = exif
            print(Fore.GREEN + "   📝 EXIF metadata preserved")
        
        img_enhanced.save(ruta_salida, **save_params)
        
        # Información del resultado
        if ruta_salida.exists():
            tamaño_original = ruta_imagen.stat().st_size / (1024 * 1024)
            tamaño_nuevo = ruta_salida.stat().st_size / (1024 * 1024)

            print_success_box("✅ IMAGE ENHANCED SUCCESSFULLY", [
                f"📝 Name: {ruta_salida.name}",
                f"📐 Resolution: {img_enhanced.width}×{img_enhanced.height} px",
                f"⬆️  Scale factor: ×{escala}",
                f"💾 Original size: {tamaño_original:.2f} MB",
                f"💾 Final size: {tamaño_nuevo:.2f} MB",
                f"📁 {ruta_salida.parent}",
            ], [Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.CYAN])

            print(Fore.CYAN + "\n💡 Sharpness, contrast and Lanczos upscaling filters applied")
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_imagen)
        else:
            print(Fore.RED + "\n❌ Error saving image")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {str(e)}")
    
    finally:
        pausar()
