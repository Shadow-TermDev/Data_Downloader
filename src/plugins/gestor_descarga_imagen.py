import os
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from colorama import Fore, Style
from src.utils import BASE_IMAGENES as ruta_imagenes, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def mostrar_progreso_descarga(recibido, total):
    if total > 0:
        porcentaje = recibido / total * 100
        barra = "█" * int(porcentaje / 5) + "░" * (20 - int(porcentaje / 5))
        print(f"\r{Fore.YELLOW}Descargando... [{barra}] {porcentaje:.1f}%", end="", flush=True)

def descargar_imagen(url):
    ocultar_cursor()

    try:
        print(Fore.YELLOW + "\nObteniendo información de la imagen...")

        # Headers para parecer un navegador real (evita bloqueos)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
        }

        # Descarga con streaming + progreso
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        recibido = 0
        chunks = []

        print(Fore.CYAN + "Descargando imagen con calidad original...")
        for chunk in response.iter_content(1024 * 64):  # 64KB chunks
            if chunk:
                chunks.append(chunk)
                recibido += len(chunk)
                mostrar_progreso_descarga(recibido, total_size)
        print(f"\n{Fore.GREEN}Descarga completada.")

        # Cargar imagen
        data = BytesIO(b''.join(chunks))
        try:
            img = Image.open(data)
        except UnidentifiedImageError:
            print(Fore.RED + "\nEl enlace no es una imagen válida.")
            pausar()
            return

        # Info de calidad
        ancho, alto = img.size
        formato = img.format or "Desconocido"
        tamaño_mb = total_size / (1024 * 1024)

        print(Fore.CYAN + f"\nCalidad detectada:")
        print(Fore.WHITE + f"   Resolución: {ancho}×{alto} píxeles")
        print(Fore.WHITE + f"   Formato: {formato}")
        print(Fore.WHITE + f"   Tamaño: {tamaño_mb:.2f} MB")

        # Nombre limpio y bonito
        nombre_limpio = url.split("/")[-1].split("?")[0]
        if not nombre_limpio or "." not in nombre_limpio:
            import hashlib
            hash_name = hashlib.md5(url.encode()).hexdigest()[:12]
            extension = f".{formato.lower()}" if formato != "Desconocido" else ".jpg"
            nombre_limpio = f"imagen_{hash_name}{extension}"
        else:
            nombre_limpio = requests.utils.unquote(nombre_limpio)

        ruta_final = os.path.join(ruta_imagenes, nombre_limpio)

        # Guardar con máxima calidad
        save_params = {}
        if formato == "PNG":
            save_params = {"compress_level": 6}
        elif formato in ["JPEG", "JPG"]:
            save_params = {"quality": 95, "optimize": True}

        img.save(ruta_final, **save_params)

        print(Fore.GREEN + f"\nImagen descargada y guardada con calidad original!")
        print(Fore.WHITE + f"   Ruta: {ruta_final}")

    except requests.exceptions.Timeout:
        print(Fore.RED + "\nTimeout: La imagen tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "\nError de conexión. Revisa tu internet.")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(Fore.RED + "\n404: Imagen no encontrada.")
        else:
            print(Fore.RED + f"\nError HTTP {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"\nError inesperado: {e}")
    finally:
        pausar()  # ← Siempre espera Enter como en todos los demás
