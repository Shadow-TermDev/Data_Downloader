"""
Image conversion module
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

from pathlib import Path
from PIL import Image
from colorama import Fore

from config.settings import IMAGE_FORMATS
from src.utils.animations import ocultar_cursor
from src.utils.helpers import pausar
from src.utils.boxes import print_success_box
from src.core.file_manager import eliminar_archivo_seguro


# Quality params per format
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
    Convert an image to another format
    
    Args:
        ruta_imagen: Original image Path
        formato: Output format
    """
    ocultar_cursor()
    
    try:
        if not ruta_imagen.exists():
            print(Fore.RED + f"\n❌ File not found: {ruta_imagen}")
            return
        
        formato = formato.lower()
        if formato == "jpeg":
            formato = "jpg"
        
        if formato not in IMAGE_FORMATS:
            print(Fore.RED + f"\n❌ Unsupported format: {formato.upper()}")
            print(Fore.CYAN + f"Available formats: {', '.join(sorted(IMAGE_FORMATS))}")
            return
        
        # Generar nombre de salida
        nombre_base = ruta_imagen.stem
        ruta_salida = ruta_imagen.parent / f"{nombre_base}_converted.{formato}"
        
        print(Fore.YELLOW + f"\n🔄 Converting image to .{formato.upper()}...")
        print(Fore.CYAN + "⏳ Preserving maximum quality...\n")
        
        # Abrir imagen
        with Image.open(ruta_imagen) as img:
            ancho, alto = img.size
            modo_original = img.mode
            
            print(Fore.CYAN + "📊 Original info:")
            print(Fore.WHITE + f"   Resolution: {ancho} × {alto} px")
            print(Fore.WHITE + f"   Mode: {modo_original}")
            
            # Convertir modo si es necesario
            if formato in ["jpg", "jpeg", "webp"] and img.mode in ("RGBA", "LA", "P"):
                print(Fore.YELLOW + "   🎨 Applying white background (no transparency)")
                
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
                print(Fore.CYAN + "   🔄 Adjusting color mode...")
                img = img.convert("RGB")
            
            # Manejo especial para ICO
            if formato == "ico":
                print(Fore.CYAN + "   🔧 Resizing for ICO format (256×256)...")
                img = img.resize((256, 256), Image.LANCZOS)
            
            # Obtener parámetros de calidad
            save_kwargs = CALIDAD_POR_FORMATO.get(formato, {})
            
            # Guardar
            print(Fore.YELLOW + "\n💾 Saving image...")
            img.save(ruta_salida, **save_kwargs)
        
        # Verificar resultado
        if ruta_salida.exists():
            tamaño_original = ruta_imagen.stat().st_size / (1024 * 1024)
            tamaño_nuevo = ruta_salida.stat().st_size / (1024 * 1024)
            reduccion = ((tamaño_original - tamaño_nuevo) / tamaño_original * 100)

            lineas = [
                f"📝 Name: {ruta_salida.name}",
                f"📦 Format: {formato.upper()}",
                f"💾 Original size: {tamaño_original:.2f} MB",
                f"💾 Final size: {tamaño_nuevo:.2f} MB",
            ]
            colores = [Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE]

            if reduccion > 0:
                lineas.append(f"📉 Reduction: {reduccion:.1f}%")
                colores.append(Fore.GREEN)
            elif reduccion < 0:
                lineas.append(f"📈 Increase: {abs(reduccion):.1f}%")
                colores.append(Fore.YELLOW)

            lineas.append(f"📁 {ruta_salida.parent}")
            colores.append(Fore.CYAN)

            print_success_box("✅ IMAGE CONVERTED SUCCESSFULLY", lineas, colores)
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_imagen)
        else:
            print(Fore.RED + "\n❌ Error saving image")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ File not found")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error converting: {str(e)}")
    
    finally:
        pausar()
