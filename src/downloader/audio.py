"""
Módulo de descarga de audio
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import subprocess
from pathlib import Path
from colorama import Fore, Style

from config.settings import AUDIO_DIR, MESSAGES
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar


def obtener_calidades_audio(url: str) -> list:
    """
    Obtiene las calidades de audio disponibles
    
    Args:
        url: URL del audio/video
        
    Returns:
        Lista de tuplas (format_id, bitrate)
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "-F", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return None
        
        calidades = []
        for linea in result.stdout.splitlines():
            # Buscar líneas que contengan "audio only"
            if "audio only" in linea.lower():
                partes = linea.split()
                if len(partes) >= 4:
                    formato = partes[0]
                    
                    # Buscar el bitrate
                    bitrate = "?? kbps"
                    for parte in partes:
                        if "k" in parte.lower() and any(c.isdigit() for c in parte):
                            bitrate = parte.replace('k', ' kbps')
                            break
                    
                    # Evitar formatos m4a de baja calidad o extraños
                    if "m4a" in linea.lower() and "tiny" in linea.lower():
                        continue
                    
                    calidades.append((formato, bitrate))
        
        # Ordenar por bitrate (mayor primero)
        def extraer_numero(bitrate_str):
            nums = ''.join(c for c in bitrate_str if c.isdigit())
            return int(nums) if nums else 0
        
        calidades.sort(key=lambda x: extraer_numero(x[1]), reverse=True)
        
        return calidades[:10] if calidades else None
    
    except subprocess.TimeoutExpired:
        print(Fore.RED + "\n❌ Timeout al obtener información del audio")
        return None
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {str(e)}")
        return None


def seleccionar_calidad(calidades: list) -> str:
    """
    Permite seleccionar la calidad de audio
    
    Args:
        calidades: Lista de calidades disponibles
        
    Returns:
        format_id seleccionado
    """
    print(Fore.CYAN + "\n🎵 Calidades de audio disponibles:")
    print(Fore.MAGENTA + "─" * 40)
    
    for i, (formato, bitrate) in enumerate(calidades, 1):
        color = Fore.GREEN if i == 1 else Fore.WHITE
        estrella = "⭐ " if i == 1 else "   "
        print(f"{color}{estrella}{i}. {bitrate.ljust(12)} - Formato {formato}")
    
    print(Fore.MAGENTA + "─" * 40)
    
    while True:
        mostrar_cursor()
        sel = input(Fore.CYAN + f"\n➜ Elige [1-{len(calidades)}] (1=mejor): " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        if sel.isdigit() and 1 <= int(sel) <= len(calidades):
            return calidades[int(sel) - 1][0]
        
        print(Fore.RED + "❌ Opción inválida.")


def descargar_audio(url: str):
    """
    Descarga audio de una URL y convierte a MP3
    
    Args:
        url: URL del audio/video
    """
    ocultar_cursor()
    
    try:
        print(Fore.YELLOW + "\n🔍 Obteniendo información del audio...")
        calidades = obtener_calidades_audio(url)
        
        if not calidades:
            print(Fore.RED + "\n❌ No se encontraron calidades de audio o URL inválida.")
            print(Fore.CYAN + "\n💡 Sugerencias:")
            print(Fore.WHITE + "   • Verifica que la URL sea correcta")
            print(Fore.WHITE + "   • Asegúrate de tener conexión a internet")
            pausar()
            return
        
        formato = seleccionar_calidad(calidades)
        
        print(Fore.YELLOW + f"\n🎵 Descargando audio en la mejor calidad...")
        print(Fore.CYAN + "⏳ Esto puede tardar unos segundos/minutos...\n")
        
        # Comando optimizado para descarga de audio
        comando = [
            "yt-dlp",
            "-f", formato,
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",  # Mejor calidad
            "--embed-thumbnail",
            "--add-metadata",
            "--embed-metadata",
            "-o", str(AUDIO_DIR / "%(title)s.%(ext)s"),
            url
        ]
        
        # Ejecutar con output en tiempo real
        process = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Mostrar progreso
        for linea in process.stdout:
            linea = linea.strip()
            if linea:
                # Filtrar solo líneas importantes
                if any(keyword in linea for keyword in [
                    'Downloading', 'download', '%', 'ETA',
                    'Extracting', 'Converting', 'Embedding'
                ]):
                    print(f"\r{Fore.CYAN}{linea[:80]}", end="", flush=True)
        
        process.wait()
        
        if process.returncode == 0:
            print(Fore.GREEN + f"\n\n🎉 ¡Audio descargado y convertido exitosamente!")
            print(Fore.WHITE + f"   🎵 Formato: MP3 (máxima calidad)")
            print(Fore.WHITE + f"   🖼️  Portada: Incluida")
            print(Fore.WHITE + f"   📁 Carpeta: {AUDIO_DIR}")
            print(Fore.CYAN + f"\n💡 Tip: Encuentra tu audio en Music/Music_Downloader")
        else:
            print(Fore.RED + "\n\n❌ Error durante la descarga")
            print(Fore.YELLOW + "💡 Intenta actualizar yt-dlp: pip install -U yt-dlp")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Descarga cancelada por el usuario")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ Error: yt-dlp no está instalado")
        print(Fore.CYAN + "Instálalo con: pip install yt-dlp")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
    
    finally:
        pausar()
