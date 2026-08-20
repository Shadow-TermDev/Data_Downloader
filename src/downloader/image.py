"""
Módulo de descarga de imágenes
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import requests
import hashlib
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from colorama import Fore

from config.settings import IMAGES_DIR
from src.utils.animations import ocultar_cursor
from src.utils.helpers import pausar
from src.utils.boxes import (
    print_info_box, print_success_box, print_error_box,
    print_progress_bar, clear_progress_line
)


def generar_nombre_limpio(url: str, formato: str) -> str:
    """Genera un nombre limpio para la imagen"""
    nombre = url.split("/")[-1].split("?")[0]

    if not nombre or "." not in nombre:
        hash_name = hashlib.md5(url.encode()).hexdigest()[:12]
        extension = f".{formato.lower()}" if formato != "Desconocido" else ".jpg"
        nombre = f"imagen_{hash_name}{extension}"
    else:
        nombre = requests.utils.unquote(nombre)
        caracteres_invalidos = '<>:"|?*'
        for char in caracteres_invalidos:
            nombre = nombre.replace(char, '_')

    return nombre


def descargar_imagen(url: str):
    """Descarga una imagen de una URL"""
    ocultar_cursor()

    try:
        # Caja de análisis
        print_info_box("🖼️  DESCARGANDO IMAGEN")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Referer': 'https://www.google.com/'
        }

        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        recibido = 0
        chunks = []

        if total_size > 0:
            print_progress_bar(0)

        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                chunks.append(chunk)
                recibido += len(chunk)
                if total_size > 0:
                    percent = (recibido / total_size) * 100
                    print_progress_bar(percent)

        clear_progress_line()

        data = BytesIO(b''.join(chunks))

        try:
            img = Image.open(data)
        except UnidentifiedImageError:
            print_error_box("❌ ERROR", ["El enlace no es una imagen válida"])
            return

        ancho, alto = img.size
        formato = img.format or "Desconocido"

        nombre_limpio = generar_nombre_limpio(url, formato)
        ruta_final = IMAGES_DIR / nombre_limpio

        # Corregir la extensión si no coincide con el formato real de la imagen
        if formato != "Desconocido":
            ext_real = formato.lower()
            if ext_real == "jpeg":
                ext_real = "jpg"
            if ruta_final.suffix.lower() != f".{ext_real}":
                ruta_final = ruta_final.with_suffix(f".{ext_real}")
                nombre_limpio = ruta_final.name

        # JPEG no soporta transparencia: pegar sobre fondo blanco
        if ruta_final.suffix.lower() in (".jpg", ".jpeg") and img.mode in ("RGBA", "LA", "P"):
            fondo = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            if img.mode in ("RGBA", "LA"):
                fondo.paste(img, mask=img.split()[-1])
            else:
                fondo.paste(img)
            img = fondo

        save_params = {}
        if formato == "PNG":
            save_params = {"compress_level": 6, "optimize": True}
        elif formato in ["JPEG", "JPG"]:
            save_params = {"quality": 95, "optimize": True, "progressive": True}
        elif formato == "WEBP":
            save_params = {"quality": 95, "method": 6}

        img.save(ruta_final, **save_params)

        if ruta_final.exists():
            tamaño_guardado = ruta_final.stat().st_size / (1024 * 1024)

            print()
            print_success_box("✅ DESCARGA COMPLETADA", [
                f"📐 Resolución: {ancho} × {alto}",
                f"📦 Formato: {formato}",
                f"💾 Tamaño: {tamaño_guardado:.2f} MB",
                "📁 Pictures/Picture_Downloader"
            ])
        else:
            print_error_box("❌ ERROR", ["Error al guardar la imagen"])

    except requests.exceptions.Timeout:
        print_error_box("❌ TIMEOUT", ["La imagen tardó demasiado en descargarse"])
    except requests.exceptions.ConnectionError:
        print_error_box("❌ ERROR DE CONEXIÓN", ["No se pudo conectar al servidor"])
    except requests.exceptions.HTTPError as e:
        print_error_box("❌ ERROR HTTP", [f"Código: {e.response.status_code}"])
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Descarga cancelada")
    except Exception as e:
        print_error_box("❌ ERROR", [f"Error: {str(e)[:50]}"])
    finally:
        pausar()