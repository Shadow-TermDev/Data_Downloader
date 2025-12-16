"""
Módulo de conversión de imágenes
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
from pathlib import Path
from PIL import Image
from colorama import Fore, Style

from config.settings import IMAGE_FORMATS
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.core.file_manager import eliminar_archivo_seguro


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


def convertir_imagen(ruta_imagen: Path, formato: str):
    """
    Convierte una imagen a otro formato
    
    Args:
        ruta_imagen: Path de la imagen original
        formato: Formato de salida
    """
    ocultar_cursor()
    
    try:
        if not ruta_imagen.exists():
            print(Fore.RED + f"\n❌ Archivo no encontrado: {ruta_imagen}")
            pausar()
            return
        
        # Validar formato
        formato = formato.lower()
        if formato == "jpeg":
            formato = "jpg"  # PIL usa "jpg" internamente
        
        if formato not in IMAGE_FORMATS:
            print(Fore.RED + f"\n❌ Formato no soportado: {formato.upper()}")
            print(Fore.CYAN + f"Formatos disponibles: {', '.join(sorted(IMAGE_FORMATS))}")
            pausar()
            return
        
        # Generar nombre de salida
        nombre_base = ruta_imagen.stem
        ruta_salida = ruta_imagen.parent / f"{nombre_base}_convertida.{formato}"
        
        print(Fore.YELLOW + f"\n🔄 Convirtiendo imagen a .{formato.upper()}...")
        print(Fore.CYAN + "⏳ Preservando calidad máxima...\n")
        
        # Abrir imagen
        with Image.open(ruta_imagen) as img:
            ancho, alto = img.size
            modo_original = img.mode
            
            print(Fore.CYAN + f"📊 Información original:")
            print(Fore.WHITE + f"   Resolución: {ancho} × {alto} px")
            print(Fore.WHITE + f"   Modo: {modo_original}")
            
            # Convertir modo si es necesario
            if formato in ["jpg", "jpeg", "webp"] and img.mode in ("RGBA", "LA", "P"):
                print(Fore.YELLOW + "   🎨 Aplicando fondo blanco (sin transparencia)")
                
                # Crear fondo blanco
                fondo = Image.new("RGB", img.size, (255, 255, 255))
                
                # Convertir paleta a RGBA si es necesario
                if img.mode == "P":
                    img = img.convert("RGBA")
                
                # Pegar imagen sobre fondo
                if img.mode in ("RGBA", "LA"):
                    fondo.paste(img, mask=img.split()[-1])
                else:
                    fondo.paste(img)
                
                img = fondo
            
            elif img.mode not in ("RGB", "RGBA", "L", "P"):
                print(Fore.CYAN + "   🔄 Ajustando modo de color...")
                img = img.convert("RGB")
            
            # Manejo especial para ICO
            if formato == "ico":
                print(Fore.CYAN + "   🔧 Redimensionando para formato ICO (256×256)...")
                img = img.resize((256, 256), Image.LANCZOS)
            
            # Obtener parámetros de calidad
            save_kwargs = CALIDAD_POR_FORMATO.get(formato, {})
            
            # Guardar
            print(Fore.YELLOW + "\n💾 Guardando imagen...")
            img.save(ruta_salida, **save_kwargs)
        
        # Verificar resultado
        if ruta_salida.exists():
            tamaño_original = ruta_imagen.stat().st_size / (1024 * 1024)
            tamaño_nuevo = ruta_salida.stat().st_size / (1024 * 1024)
            reduccion = ((tamaño_original - tamaño_nuevo) / tamaño_original * 100)
            
            print(Fore.GREEN + f"\n🎉 ¡Imagen convertida exitosamente!")
            print(Fore.WHITE + f"   📝 Nombre: {ruta_salida.name}")
            print(Fore.WHITE + f"   📦 Formato: {formato.upper()}")
            print(Fore.WHITE + f"   💾 Tamaño original: {tamaño_original:.2f} MB")
            print(Fore.WHITE + f"   💾 Tamaño final: {tamaño_nuevo:.2f} MB")
            
            if reduccion > 0:
                print(Fore.GREEN + f"   📉 Reducción: {reduccion:.1f}%")
            elif reduccion < 0:
                print(Fore.YELLOW + f"   📈 Aumento: {abs(reduccion):.1f}%")
            
            print(Fore.WHITE + f"   📁 Ubicación: {ruta_salida.parent}")
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_imagen)
        else:
            print(Fore.RED + "\n❌ Error al guardar la imagen")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ Archivo no encontrado")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error al convertir: {str(e)}")
    
    finally:
        pausar()
