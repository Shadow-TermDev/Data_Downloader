"""
Módulo de descarga de imágenes
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import requests
import hashlib
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from pathlib import Path
from colorama import Fore, Style

from config.settings import IMAGES_DIR, MESSAGES
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar


def mostrar_progreso_descarga(recibido: int, total: int):
    """
    Muestra barra de progreso de descarga
    
    Args:
        recibido: Bytes recibidos
        total: Total de bytes
    """
    if total > 0:
        porcentaje = (recibido / total) * 100
        barra_ancho = 30
        bloques = int((porcentaje / 100) * barra_ancho)
        barra = "█" * bloques + "░" * (barra_ancho - bloques)
        
        # Calcular tamaño en MB
        recibido_mb = recibido / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        
        print(
            f"\r{Fore.CYAN}[{barra}] {porcentaje:.1f}% | "
            f"{recibido_mb:.2f}/{total_mb:.2f} MB",
            end="",
            flush=True
        )


def generar_nombre_limpio(url: str, formato: str) -> str:
    """
    Genera un nombre limpio para la imagen
    
    Args:
        url: URL de la imagen
        formato: Formato de la imagen
        
    Returns:
        Nombre de archivo limpio
    """
    # Intentar extraer nombre de la URL
    nombre = url.split("/")[-1].split("?")[0]
    
    # Si no hay nombre válido, generar uno con hash
    if not nombre or "." not in nombre:
        hash_name = hashlib.md5(url.encode()).hexdigest()[:12]
        extension = f".{formato.lower()}" if formato != "Desconocido" else ".jpg"
        nombre = f"imagen_{hash_name}{extension}"
    else:
        # Decodificar URL encoding
        nombre = requests.utils.unquote(nombre)
        
        # Limpiar caracteres no válidos
        caracteres_invalidos = '<>:"|?*'
        for char in caracteres_invalidos:
            nombre = nombre.replace(char, '_')
    
    return nombre


def descargar_imagen(url: str):
    """
    Descarga una imagen de una URL
    
    Args:
        url: URL de la imagen
    """
    ocultar_cursor()
    
    try:
        print(Fore.CYAN + "\n╔" + "═" * 50 + "╗")
        print(Fore.CYAN + "║" + Fore.YELLOW + " 🖼️  DESCARGANDO IMAGEN ".center(50) + Fore.CYAN + "║")
        print(Fore.CYAN + "╚" + "═" * 50 + "╝\n")
        
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
        
        print(Fore.CYAN + "▓" + "░" * 25 + "▓ 0%", end="\r")
        
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                chunks.append(chunk)
                recibido += len(chunk)
                if total_size > 0:
                    percent = (recibido / total_size) * 100
                    barra = int(percent / 100 * 25)
                    print(Fore.CYAN + f"▓{'█'*barra}{'░'*(25-barra)}▓ {percent:.0f}%", end="\r")
        
        data = BytesIO(b''.join(chunks))
        
        try:
            img = Image.open(data)
        except UnidentifiedImageError:
            print(Fore.RED + "\n❌ El enlace no es una imagen válida")
            return
        
        ancho, alto = img.size
        formato = img.format or "Desconocido"
        modo = img.mode
        tamaño_mb = total_size / (1024 * 1024) if total_size > 0 else recibido / (1024 * 1024)
        
        nombre_limpio = generar_nombre_limpio(url, formato)
        ruta_final = IMAGES_DIR / nombre_limpio
        
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
            
            print(Fore.GREEN + "\n\n╭" + "─" * 50 + "╮")
            print(Fore.GREEN + "│" + Fore.WHITE + " ✅ DESCARGA COMPLETADA ".center(50) + Fore.GREEN + "│")
            print(Fore.GREEN + "├" + "─" * 50 + "┤")
            print(Fore.GREEN + "│" + Fore.WHITE + f" 📐 Resolución: {ancho} × {alto}".ljust(51) + Fore.GREEN + "│")
            print(Fore.GREEN + "│" + Fore.WHITE + f" 📦 Formato: {formato}".ljust(51) + Fore.GREEN + "│")
            print(Fore.GREEN + "│" + Fore.WHITE + f" 💾 Tamaño: {tamaño_guardado:.2f} MB".ljust(51) + Fore.GREEN + "│")
            print(Fore.GREEN + "│" + Fore.CYAN + " 📁 Pictures/Picture_Downloader".ljust(51) + Fore.GREEN + "│")
            print(Fore.GREEN + "╰" + "─" * 50 + "╯")
        else:
            print(Fore.RED + "\n❌ Error al guardar la imagen")
    
    except requests.exceptions.Timeout:
        print(Fore.RED + "\n❌ Timeout: La imagen tardó demasiado")
    
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "\n❌ Error de conexión")
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        print(Fore.RED + f"\n❌ Error HTTP {status_code}")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Descarga cancelada")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {str(e)[:50]}")
    
    finally:
        pausar()
