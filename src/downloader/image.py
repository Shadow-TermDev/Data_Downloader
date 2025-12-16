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
        print(Fore.YELLOW + "\n🔍 Obteniendo información de la imagen...")
        
        # Headers para evitar bloqueos
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        # Descarga con streaming
        print(Fore.CYAN + "⏳ Descargando imagen...")
        
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        recibido = 0
        chunks = []
        
        # Descargar con progreso
        for chunk in response.iter_content(chunk_size=65536):  # 64KB chunks
            if chunk:
                chunks.append(chunk)
                recibido += len(chunk)
                if total_size > 0:
                    mostrar_progreso_descarga(recibido, total_size)
        
        print(f"\n{Fore.GREEN}✅ Descarga completada")
        
        # Procesar imagen
        print(Fore.CYAN + "🖼️  Procesando imagen...")
        data = BytesIO(b''.join(chunks))
        
        try:
            img = Image.open(data)
        except UnidentifiedImageError:
            print(Fore.RED + "\n❌ El enlace no es una imagen válida")
            print(Fore.YELLOW + "💡 Verifica que la URL apunte directamente a una imagen")
            pausar()
            return
        
        # Información de la imagen
        ancho, alto = img.size
        formato = img.format or "Desconocido"
        modo = img.mode
        tamaño_mb = total_size / (1024 * 1024) if total_size > 0 else recibido / (1024 * 1024)
        
        print(Fore.CYAN + f"\n📊 Información de la imagen:")
        print(Fore.WHITE + f"   🖼️  Resolución: {ancho} × {alto} píxeles")
        print(Fore.WHITE + f"   📦 Formato: {formato}")
        print(Fore.WHITE + f"   🎨 Modo de color: {modo}")
        print(Fore.WHITE + f"   💾 Tamaño: {tamaño_mb:.2f} MB")
        
        # Generar nombre y guardar
        nombre_limpio = generar_nombre_limpio(url, formato)
        ruta_final = IMAGES_DIR / nombre_limpio
        
        # Guardar con máxima calidad
        save_params = {}
        if formato == "PNG":
            save_params = {"compress_level": 6, "optimize": True}
        elif formato in ["JPEG", "JPG"]:
            save_params = {"quality": 95, "optimize": True, "progressive": True}
        elif formato == "WEBP":
            save_params = {"quality": 95, "method": 6}
        
        print(Fore.YELLOW + "\n💾 Guardando imagen...")
        img.save(ruta_final, **save_params)
        
        # Verificar que se guardó correctamente
        if ruta_final.exists():
            tamaño_guardado = ruta_final.stat().st_size / (1024 * 1024)
            
            print(Fore.GREEN + f"\n🎉 ¡Imagen descargada exitosamente!")
            print(Fore.WHITE + f"   📝 Nombre: {nombre_limpio}")
            print(Fore.WHITE + f"   💾 Tamaño final: {tamaño_guardado:.2f} MB")
            print(Fore.WHITE + f"   📁 Carpeta: {IMAGES_DIR}")
            print(Fore.CYAN + f"\n💡 Tip: Encuentra tu imagen en Pictures/Picture_Downloader")
        else:
            print(Fore.RED + "\n❌ Error al guardar la imagen")
    
    except requests.exceptions.Timeout:
        print(Fore.RED + "\n❌ Timeout: La imagen tardó demasiado en responder")
        print(Fore.YELLOW + "💡 Verifica tu conexión a internet")
    
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "\n❌ Error de conexión")
        print(Fore.YELLOW + "💡 Verifica tu conexión a internet")
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        print(Fore.RED + f"\n❌ Error HTTP {status_code}")
        
        if status_code == 404:
            print(Fore.YELLOW + "💡 La imagen no existe o fue eliminada")
        elif status_code == 403:
            print(Fore.YELLOW + "💡 Acceso prohibido. La imagen puede estar protegida")
        elif status_code == 429:
            print(Fore.YELLOW + "💡 Demasiadas solicitudes. Espera unos minutos")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Descarga cancelada por el usuario")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
    
    finally:
        pausar()
