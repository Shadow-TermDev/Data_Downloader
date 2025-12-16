"""
Módulo de descarga de videos
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import yt_dlp
from pathlib import Path
from colorama import Fore, Style

from config.settings import VIDEOS_DIR, MESSAGES
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar, mostrar_progreso


def progreso_hook(d):
    """Hook para mostrar progreso de descarga"""
    if d['status'] == 'downloading':
        try:
            percent = d.get('_percent_str', '0%').strip()
            speed = d.get('_speed_str', '0 B/s').strip()
            eta = d.get('_eta_str', 'Calculando...').strip()
            
            barra_ancho = 30
            porcentaje_num = float(percent.replace('%', ''))
            bloques = int((porcentaje_num / 100) * barra_ancho)
            barra = "█" * bloques + "░" * (barra_ancho - bloques)
            
            print(f"\r{Fore.CYAN}[{barra}] {percent} | {speed} | ETA: {eta}", end="", flush=True)
        except:
            pass
    elif d['status'] == 'finished':
        print(f"\n{Fore.GREEN}✅ Descarga completada. Procesando...")


def obtener_calidades_video(url: str) -> list:
    """
    Obtiene las calidades disponibles para un video
    
    Args:
        url: URL del video
        
    Returns:
        Lista de tuplas (format_id, label, size)
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formatos = []
            visto = set()
            
            for f in info.get('formats', []):
                # Solo formatos con video Y audio
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    height = f.get('height') or 0
                    vcodec = f.get('vcodec', 'h264')[:10]  # Limitar longitud
                    ext = f.get('ext', 'mp4')
                    filesize = f.get('filesize') or f.get('filesize_approx', 0)
                    
                    # Calcular tamaño
                    if filesize > 0:
                        size_mb = f"{filesize / (1024*1024):.1f} MB"
                    else:
                        size_mb = "?? MB"
                    
                    # Crear etiqueta descriptiva
                    if height > 0:
                        codec_label = "HEVC" if "hevc" in vcodec.lower() or "h265" in vcodec.lower() else "H264"
                        label = f"{height}p {codec_label}"
                    else:
                        label = f"{ext.upper()}"
                    
                    # Evitar duplicados por altura y codec
                    key = (height, codec_label if height > 0 else ext)
                    
                    if key not in visto:
                        visto.add(key)
                        formatos.append((f['format_id'], label, size_mb, height))
            
            # Ordenar: mayor resolución primero, luego por codec
            formatos.sort(key=lambda x: (x[3], 1 if 'HEVC' in x[1] else 0), reverse=True)
            
            return [(fid, label, size) for fid, label, size, _ in formatos[:15]]
    
    except yt_dlp.utils.DownloadError as e:
        print(Fore.RED + f"\n❌ Error al acceder al video: {str(e)}")
        return []
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
        return []


def seleccionar_calidad(calidades: list) -> str:
    """
    Permite al usuario seleccionar una calidad
    
    Args:
        calidades: Lista de calidades disponibles
        
    Returns:
        format_id seleccionado o None
    """
    if not calidades:
        print(Fore.RED + "\n❌ No hay formatos de video disponibles.")
        print(Fore.YELLOW + "💡 Tip: Algunos servicios (TikTok) pueden requerir herramientas especializadas.")
        return None
    
    print(Fore.CYAN + f"\n📺 Calidades disponibles:")
    print(Fore.MAGENTA + "─" * 50)
    
    for i, (fid, label, size) in enumerate(calidades, 1):
        # Destacar la mejor calidad
        color = Fore.GREEN if i == 1 else Fore.WHITE
        estrella = "⭐ " if i == 1 else "   "
        print(f"{color}{estrella}{i}. {label.ljust(15)} | Tamaño: {size}")
    
    print(Fore.MAGENTA + "─" * 50)
    
    while True:
        mostrar_cursor()
        sel = input(Fore.CYAN + f"\n➜ Elige [1-{len(calidades)}] (1=mejor calidad): " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        if sel.isdigit() and 1 <= int(sel) <= len(calidades):
            return calidades[int(sel) - 1][0]
        
        print(Fore.RED + "❌ Opción inválida. Intenta de nuevo.")


def descargar_video(url: str):
    """
    Descarga un video de una URL
    
    Args:
        url: URL del video a descargar
    """
    ocultar_cursor()
    
    try:
        print(Fore.YELLOW + "\n🔍 Analizando video y calidades disponibles...")
        print(Fore.CYAN + "Esto puede tomar unos segundos...\n")
        
        calidades = obtener_calidades_video(url)
        
        if not calidades:
            pausar()
            return
        
        # Advertencia si la mejor calidad es baja
        mejor_calidad = calidades[0][1]
        if '360p' in mejor_calidad or '480p' in mejor_calidad:
            print(Fore.YELLOW + f"\n⚠️  La máxima calidad disponible es: {mejor_calidad}")
            print(Fore.CYAN + "   Esto es normal en algunos servicios.")
        
        formato_id = seleccionar_calidad(calidades)
        
        if not formato_id:
            pausar()
            return
        
        # Configuración optimizada para descarga
        ydl_opts = {
            'format': f'{formato_id}+bestaudio/best',
            'outtmpl': str(VIDEOS_DIR / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'embed_thumbnail': True,
            'embed_subs': True,
            'writesubtitles': True,
            'progress_hooks': [progreso_hook],
            'quiet': False,
            'no_warnings': False,
        }
        
        print(Fore.YELLOW + f"\n🎬 Descargando video en calidad seleccionada...")
        print(Fore.CYAN + "Progreso:\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'video')
            duracion = info.get('duration', 0)
            
            min_duracion = duracion // 60
            seg_duracion = duracion % 60
        
        print(Fore.GREEN + f"\n\n🎉 ¡Video descargado exitosamente!")
        print(Fore.WHITE + f"   📝 Título: {titulo}")
        print(Fore.WHITE + f"   ⏱️  Duración: {min_duracion}:{seg_duracion:02d}")
        print(Fore.WHITE + f"   📁 Carpeta: {VIDEOS_DIR}")
        print(Fore.CYAN + f"\n💡 Tip: Encuentra tu video en la carpeta VMovies/Videos_Downloader")
    
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(Fore.RED + f"\n❌ Error en la descarga:")
        
        if "429" in error_msg:
            print(Fore.YELLOW + "   → Demasiadas solicitudes. Espera unos minutos.")
        elif "403" in error_msg or "Forbidden" in error_msg:
            print(Fore.YELLOW + "   → Acceso bloqueado. El video puede ser privado o restringido.")
        elif "404" in error_msg:
            print(Fore.YELLOW + "   → Video no encontrado. Verifica la URL.")
        else:
            print(Fore.YELLOW + f"   → {error_msg[:100]}")
        
        print(Fore.CYAN + "\n💡 Sugerencias:")
        print(Fore.WHITE + "   • Verifica que la URL sea correcta")
        print(Fore.WHITE + "   • Actualiza yt-dlp: pip install -U yt-dlp")
        print(Fore.WHITE + "   • Algunos servicios requieren herramientas especializadas")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Descarga cancelada por el usuario")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
        print(Fore.CYAN + "\n💡 Intenta actualizar yt-dlp: pip install -U yt-dlp")
    
    finally:
        pausar()
