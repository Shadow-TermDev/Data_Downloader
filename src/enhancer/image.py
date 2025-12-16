"""
Módulo de mejora de calidad de imágenes
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
from colorama import Fore, Style

from config.settings import IMAGE_SCALE_FACTORS
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.core.file_manager import generar_nombre_salida, eliminar_archivo_seguro


def seleccionar_calidad() -> tuple:
    """
    Permite seleccionar el nivel de mejora
    
    Returns:
        Tupla con (escala, contraste, nitidez)
    """
    print(Fore.CYAN + "\n🖼️  Selecciona el nivel de mejora:")
    print(Fore.MAGENTA + "─" * 50)
    
    opciones = [
        ("1", (1.2, 1.1, 1.2), "×1.2 - Rápido", "Mejora ligera"),
        ("2", (1.5, 1.3, 1.5), "×1.5 - Balanceado", "Recomendado"),
        ("3", (2.0, 1.6, 2.0), "×2.0 - Máxima calidad", "Tarda más")
    ]
    
    for num, valores, label, desc in opciones:
        color = Fore.GREEN if num == "2" else Fore.WHITE
        estrella = "⭐ " if num == "2" else "   "
        print(f"{color}{estrella}{num}. {label} - {desc}")
    
    print(Fore.MAGENTA + "─" * 50)
    
    while True:
        mostrar_cursor()
        choice = input(Fore.CYAN + "\n➜ Elige [1-3] (2=recomendado): " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        opciones_dict = {
            "1": (1.2, 1.1, 1.2),
            "2": (1.5, 1.3, 1.5),
            "3": (2.0, 1.6, 2.0)
        }
        
        if choice in opciones_dict:
            return opciones_dict[choice]
        
        print(Fore.RED + "❌ Opción inválida")


def mejorar_imagen(ruta_entrada: Path, escala: float, contraste: float, nitidez: float) -> tuple:
    """
    Mejora una imagen con upscaling y filtros
    
    Args:
        ruta_entrada: Path de la imagen
        escala: Factor de escala
        contraste: Factor de contraste
        nitidez: Factor de nitidez
        
    Returns:
        Tupla con (imagen_mejorada, exif_data)
    """
    try:
        with Image.open(ruta_entrada) as img:
            # Obtener EXIF si existe
            exif = img.info.get("exif")
            
            # Calcular nuevo tamaño
            nuevo_ancho = int(img.width * escala)
            nuevo_alto = int(img.height * escala)
            
            print(Fore.CYAN + f"   📐 Resolución original: {img.width}×{img.height} px")
            print(Fore.CYAN + f"   📐 Resolución nueva: {nuevo_ancho}×{nuevo_alto} px")
            
            # Redimensionar con Lanczos (mejor calidad)
            print(Fore.YELLOW + "   🔄 Aplicando upscaling Lanczos...")
            img = img.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
            
            # Aplicar filtros de mejora
            print(Fore.YELLOW + "   ✨ Aplicando filtros de mejora...")
            
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
    Mejora la calidad de una imagen mediante upscaling y filtros
    
    Args:
        ruta_imagen: Path de la imagen original
    """
    ocultar_cursor()
    
    try:
        if not ruta_imagen.exists():
            print(Fore.RED + f"\n❌ Archivo no encontrado: {ruta_imagen}")
            pausar()
            return
        
        print(Fore.CYAN + f"\n📸 Procesando: {ruta_imagen.name}")
        
        # Seleccionar nivel de mejora
        escala, contraste, nitidez = seleccionar_calidad()
        
        # Generar nombre de salida
        ruta_salida = generar_nombre_salida(ruta_imagen, "_mejorada")
        
        print(Fore.YELLOW + f"\n⬆️  Mejorando imagen ×{escala}...")
        print(Fore.CYAN + "⏳ Aplicando nitidez, contraste y upscaling...\n")
        
        # Mejorar imagen
        img_mejorada, exif = mejorar_imagen(ruta_imagen, escala, contraste, nitidez)
        
        if img_mejorada is None:
            pausar()
            return
        
        # Guardar con máxima calidad
        print(Fore.YELLOW + "\n💾 Guardando imagen mejorada...")
        save_params = {
            "quality": 95,
            "optimize": True,
            "progressive": True
        }
        
        # Preservar EXIF si existe
        if exif:
            save_params["exif"] = exif
            print(Fore.GREEN + "   📝 Metadatos EXIF preservados")
        
        img_mejorada.save(ruta_salida, **save_params)
        
        # Información del resultado
        if ruta_salida.exists():
            tamaño_original = ruta_imagen.stat().st_size / (1024 * 1024)
            tamaño_nuevo = ruta_salida.stat().st_size / (1024 * 1024)
            
            print(Fore.GREEN + f"\n🎉 ¡Imagen mejorada exitosamente!")
            print(Fore.WHITE + f"   📝 Nombre: {ruta_salida.name}")
            print(Fore.WHITE + f"   📐 Resolución: {img_mejorada.width}×{img_mejorada.height} px")
            print(Fore.WHITE + f"   ⬆️  Factor de escala: ×{escala}")
            print(Fore.WHITE + f"   💾 Tamaño original: {tamaño_original:.2f} MB")
            print(Fore.WHITE + f"   💾 Tamaño final: {tamaño_nuevo:.2f} MB")
            print(Fore.WHITE + f"   📁 Ubicación: {ruta_salida.parent}")
            
            print(Fore.CYAN + f"\n💡 Se aplicaron filtros de nitidez, contraste y upscaling Lanczos")
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_imagen)
        else:
            print(Fore.RED + "\n❌ Error al guardar la imagen")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
    
    finally:
        pausar()
