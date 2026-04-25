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
from src.utils.helpers import pausar
from src.utils import pot_token, mostrar_progreso


def progreso_hook(d):
    """Hook para mostrar progreso de descarga"""
    if d['status'] == 'downloading':
        try:
            percent = d.get('_percent_str', '0%').strip()
            speed = d.get('_speed_str', 'N/A').strip()
            eta = d.get('_eta_str', '...').strip()
            
            barra_ancho = 25
            porcentaje_num = float(percent.replace('%', ''))
            bloques = int((porcentaje_num / 100) * barra_ancho)
            barra = "█" * bloques + "░" * (barra_ancho - bloques)
            
            print(f"\r{Fore.CYAN}▓{barra}▓ {percent.ljust(5)} │ {speed.ljust(10)} │ ETA: {eta}", end="", flush=True)
        except:
            pass
    elif d['status'] == 'finished':
        print(f"\r{Fore.GREEN}✓ Completado".ljust(60) + "\n")


def es_tiktok(url: str) -> bool:
    """Detecta si la URL es de TikTok"""
    return 'tiktok.com' in url.lower() or 'vm.tiktok.com' in url.lower()


def obtener_opciones_ytdlp(es_tiktok: bool = False, cookies_path: str = None) -> dict:
    """
    Obtiene opciones optimizadas para yt-dlp
    Ayuda a evitar detección de bot
    """
    opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    
    if cookies_path:
        opts['cookiefile'] = cookies_path
    
    return opts


def intentar_descarga_fallback(url: str, tipo: str = "video") -> dict:
    """
    Intenta descargar con diferentes métodos si falla el principal
    """
    metodos = [
        {},  # Intento normal
        {'extractor_args': {'youtube': {'player_client': 'android'}}},
        {'extractor_args': {'youtube': {'player_client': 'web_creator'}}},
        {'extractor_args': {'youtube': {'player_skip': 'webpage,configs'}}},
    ]
    
    for i, extra_opts in enumerate(metodos):
        ydl_opts = obtener_opciones_ytdlp()
        ydl_opts.update(extra_opts)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {'success': True, 'info': info, 'method': i + 1}
        except Exception as e:
            if i == len(metodos) - 1:
                return {'success': False, 'error': str(e)}
            continue
    
    return {'success': False, 'error': 'Todos los métodos fallaron'}


def obtener_calidades_video(url: str) -> list:
    """
    Obtiene las calidades disponibles para un video
    Intenta múltiples métodos para evitar errores
    """
    pot_iniciado = pot_token.iniciar_si_necesario()
    
    metodos = [
        pot_token.obtener_opts_video() if pot_iniciado else {},
        {},
    ]
    
    ultimo_error = None
    
    for i, extra_opts in enumerate(metodos):
        ydl_opts = obtener_opciones_ytdlp(es_tiktok(url))
        ydl_opts.update(extra_opts)
        
        if es_tiktok(url):
            ydl_opts['extractor_args'] = {'tiktok': {'downloadaddr': True}}
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if es_tiktok(url):
                    formatos = []
                    for f in info.get('formats', []):
                        if f.get('url'):
                            height = f.get('height', 0) or 0
                            size = f.get('filesize') or f.get('filesize_approx', 0)
                            size_mb = f"{size / (1024*1024):.1f} MB" if size else "?? MB"
                            label = f"{height}p" if height > 0 else "HD"
                            formatos.append((f['format_id'], label, size_mb))
                    return formatos[:8]
                
                formatos = []
                visto = set()
                
                for f in info.get('formats', []):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        height = f.get('height', 0) or 0
                        vcodec = str(f.get('vcodec', 'h264'))[:10] or 'h264'
                        ext = f.get('ext', 'mp4')
                        filesize = f.get('filesize') or f.get('filesize_approx', 0)
                        size_mb = f"{filesize / (1024*1024):.1f} MB" if filesize else "?? MB"
                        
                        if height > 0:
                            codec_label = "HEVC" if "hevc" in vcodec.lower() else "H264"
                            label = f"{height}p {codec_label}"
                        else:
                            label = f"{ext.upper()}"
                        
                        key = (height, codec_label if height > 0 else ext)
                        
                        if key not in visto:
                            visto.add(key)
                            formatos.append((f['format_id'], label, size_mb))
                
                formatos.sort(key=lambda x: int(x[1].split('p')[0]) if 'p' in x[1] else 0, reverse=True)
                return formatos[:15]
                
        except Exception as e:
            ultimo_error = str(e)
            continue
    
    if ultimo_error:
        if "Sign in to confirm" in ultimo_error:
            pot_token.mensaje_error_youtube()
        else:
            print(Fore.RED + f"\n❌ Error: {ultimo_error[:60]}")




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
        return None
    
    print(Fore.CYAN + "\n╔" + "═" * 48 + "╗")
    print(Fore.CYAN + "║" + Fore.YELLOW + " 📺 CALIDADES DISPONIBLES ".center(48) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 48 + "╣")
    
    for i, (fid, label, size) in enumerate(calidades[:8], 1):
        color = Fore.GREEN if i == 1 else Fore.WHITE
        estrella = "★" if i == 1 else " "
        linea = f"║ {color}{estrella} {i}. {label.ljust(12)} │ Tamaño: {size.ljust(10)}{Fore.CYAN}║"
        print(linea)
    
    print(Fore.CYAN + "╚" + "═" * 48 + "╝")
    
    while True:
        mostrar_cursor()
        sel = input(Fore.CYAN + "\n➜ Elige calidad [1-8]: " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        if sel.isdigit() and 1 <= int(sel) <= min(len(calidades), 8):
            return calidades[int(sel) - 1][0]
        
        print(Fore.RED + "❌ Opción inválida")


def descargar_video(url: str):
    """
    Descarga un video de una URL
    
    Args:
        url: URL del video a descargar
    """
    ocultar_cursor()
    
    try:
        print(Fore.CYAN + "\n╔" + "═" * 50 + "╗")
        print(Fore.CYAN + "║" + Fore.YELLOW + " 🎬 ANALIZANDO VIDEO ".center(50) + Fore.CYAN + "║")
        print(Fore.CYAN + "╚" + "═" * 50 + "╝\n")
        
        calidades = obtener_calidades_video(url)
        
        if not calidades:
            print(Fore.RED + "\n❌ No se pudieron obtener las calidades disponibles")
            return
        
        mejor_calidad = calidades[0][1]
        if '360p' in mejor_calidad or '480p' in mejor_calidad:
            print(Fore.YELLOW + f" ⚠️  Mejor calidad disponible: {mejor_calidad}")
        
        formato_id = seleccionar_calidad(calidades)
        
        if not formato_id:
            return
        
        # Fallback progresivo para el formato
        if formato_id.isdigit():
            formato_descarga = f'{formato_id}+bestaudio/{formato_id}/bestaudio/best'
        else:
            formato_descarga = f'{formato_id}+bestaudio/best'
        
        ydl_opts = {
            'format': formato_descarga,
            'outtmpl': str(VIDEOS_DIR / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }],
            'embed_thumbnail': True,
            'progress_hooks': [progreso_hook],
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            },
        }
        
        # Agregar PO Token si está disponible
        pot_opts = pot_token.obtener_opts_pot()
        if pot_opts:
            ydl_opts.update(pot_opts)
            print(Fore.CYAN + " ✓ PO Token activo")
        
        if es_tiktok(url):
            ydl_opts['extractor_args'] = {'tiktok': {'downloadaddr': True}}
            print(Fore.YELLOW + " ⚠️  TikTok detectado")
        
        print(Fore.GREEN + "\n╔" + "═" * 50 + "╗")
        print(Fore.GREEN + "║" + Fore.YELLOW + " 📥 DESCARGANDO VIDEO ".center(50) + Fore.GREEN + "║")
        print(Fore.GREEN + "╚" + "═" * 50 + "╝\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'video')[:40]
            duracion = info.get('duration', 0)
            
            min_duracion = duracion // 60
            seg_duracion = duracion % 60
        
        print(Fore.GREEN + "\n╭" + "─" * 50 + "╮")
        print(Fore.GREEN + "│" + Fore.WHITE + " ✅ DESCARGA COMPLETADA ".center(50) + Fore.GREEN + "│")
        print(Fore.GREEN + "├" + "─" * 50 + "┤")
        print(Fore.GREEN + "│" + Fore.WHITE + f" 📝 Título: {titulo}".ljust(51) + Fore.GREEN + "│")
        print(Fore.GREEN + "│" + Fore.WHITE + f" ⏱️  Duración: {min_duracion}:{seg_duracion:02d}".ljust(51) + Fore.GREEN + "│")
        print(Fore.GREEN + "│" + Fore.CYAN + f" 📁 Guardado en: VMovies/Videos_Downloader".ljust(51) + Fore.GREEN + "│")
        print(Fore.GREEN + "╰" + "─" * 50 + "╯")
    
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(Fore.RED + "\n╭" + "─" * 50 + "╮")
        print(Fore.RED + "│" + Fore.WHITE + " ❌ ERROR DE DESCARGA ".center(50) + Fore.RED + "│")
        print(Fore.RED + "├" + "─" * 50 + "┤")
        
        if "429" in error_msg:
            print(Fore.RED + "│" + Fore.YELLOW + " Demasiadas solicitudes. Espera unos minutos.".ljust(51) + Fore.RED + "│")
        elif "403" in error_msg or "Forbidden" in error_msg:
            print(Fore.RED + "│" + Fore.YELLOW + " Acceso bloqueado. Video privado o restringido.".ljust(51) + Fore.RED + "│")
        elif "404" in error_msg:
            print(Fore.RED + "│" + Fore.YELLOW + " Video no encontrado. Verifica la URL.".ljust(51) + Fore.RED + "│")
        else:
            print(Fore.RED + "│" + Fore.YELLOW + f" {error_msg[:45]}".ljust(51) + Fore.RED + "│")
        
        print(Fore.RED + "╰" + "─" * 50 + "╯")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Descarga cancelada")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {str(e)[:50]}")
    
    finally:
        pausar()
