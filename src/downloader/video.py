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

def es_facebook_share(url: str) -> bool:
    """Detecta si es un link share de Facebook"""
    url = url.lower()
    return "facebook.com/share/" in url or "fb.watch/" in url


def resolver_facebook_url(url: str) -> str:
    """
    Convierte un link de Facebook share a su URL real
    usando yt-dlp sin descargar
    """
    if not es_facebook(url):
        return url

    print("🔄 Resolviendo enlace de Facebook...")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if 'webpage_url' in info:
                real_url = info['webpage_url']
                print(f"✅ URL resuelta: {real_url}")
                return real_url

    except Exception as e:
        print(f"⚠️ No se pudo resolver el link: {str(e)[:60]}")

    return url


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
    url_lower = url.lower()
    return 'tiktok.com' in url_lower or 'vm.tiktok.com' in url_lower or 'musical.ly' in url_lower


def descargar_tiktok_metodos(url: str) -> bool:
    """
    Intenta descargar TikTok con múltiples métodos
    Retorna True si exitoso
    """
    metodos = [
        {
            'quiet': False,
            'no_warnings': False,
            'extractor_args': {},
        },
        {
            'quiet': False,
            'no_warnings': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            },
        },
    ]
    
    for i, extra_opts in enumerate(metodos):
        ydl_opts = {
            'format': 'best',
            'outtmpl': str(VIDEOS_DIR / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [progreso_hook],
            **extra_opts
        }
        
        try:
            print(f"  ⏳ Método {i+1}/{len(metodos)}...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    titulo = info.get('title', 'video')[:35]
                    archivos = list(VIDEOS_DIR.glob('*.mp4'))
                    ultimo = archivos[-1] if archivos else None
                    tamanho = f"{ultimo.stat().st_size / (1024*1024):.1f} MB" if ultimo else "?"
                    
                    print()
                    print(Fore.GREEN + "╭" + "─" * 54 + "╮")
                    print(Fore.GREEN + "│" + Fore.YELLOW + " ✅ DESCARGA COMPLETADA ".center(54) + Fore.GREEN + "│")
                    print(Fore.GREEN + "├" + "─" * 54 + "┤")
                    print(Fore.GREEN + "│" + Fore.CYAN + f"   📝 {titulo}".ljust(55) + Fore.GREEN + "│")
                    print(Fore.GREEN + "│" + Fore.WHITE + f"   💾 Tamaño: {tamanho}".ljust(55) + Fore.GREEN + "│")
                    print(Fore.GREEN + "│" + Fore.YELLOW + f"   📁 {VIDEOS_DIR.name}".ljust(55) + Fore.GREEN + "│")
                    print(Fore.GREEN + "╰" + "─" * 54 + "╯")
                    return True
        except Exception as e:
            continue
    
    return False


def es_facebook(url: str) -> bool:
    """Detecta si la URL es de Facebook (cualquier tipo)"""
    url_lower = url.lower()
    return (
        'facebook.com' in url_lower or
        'fb.com' in url_lower or
        'fb.watch' in url_lower or
        'fb.gg' in url_lower
    )


def obtener_opciones_ytdlp(es_tiktok: bool = False, cookies_path: str = None, es_facebook: bool = False) -> dict:
    """
    Obtiene opciones optimizadas para yt-dlp
    Ayuda a evitar detección de bot
    """
    opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    
    if es_tiktok:
        opts['extractor_args'] = {
            'tiktok': {
                'downloadaddr': True,
                'watermark': False,
            }
        }
    elif es_facebook:
        opts['extractor_args'] = {
            'facebook': {
                'download': True,
                'use_cache': True,
            }
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

    url = resolver_facebook_url(url)
    
    es_tk = es_tiktok(url)
    es_fb = es_facebook(url)
    
    metodos = [
        pot_token.obtener_opts_video() if pot_iniciado else {},
        {},
    ]
    
    ultimo_error = None
    
    for i, extra_opts in enumerate(metodos):
        ydl_opts = obtener_opciones_ytdlp(es_tk, es_facebook=es_fb)
        ydl_opts.update(extra_opts)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if es_tk or es_fb:
                    formatos = []
                    for f in info.get('formats', []):
                        if f.get('url'):
                            height = f.get('height', 0) or 0
                            size = f.get('filesize') or f.get('filesize_approx', 0)
                            size_mb = f"{size / (1024*1024):.1f} MB" if size else "?? MB"
                            label = f"{height}p" if height > 0 else "HD"
                            formatos.append((f['format_id'], label, size_mb))
                    if not formatos:
                        formatos.append(('best', 'HD', '?? MB'))
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
        elif es_tk and "403" in ultimo_error:
            print(Fore.YELLOW + "\n⚠️  TikTok requiere cookies de sesión")
            print(Fore.CYAN + "   → Exporta cookies de TikTok desde navegador")
        elif es_fb and "403" in ultimo_error:
            print(Fore.YELLOW + "\n⚠️  Facebook requiere cookies de sesión")
            print(Fore.CYAN + "   → Exporta cookies de Facebook desde navegador")
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
    
    print()
    print(Fore.CYAN + "╭" + "─" * 56 + "╮")
    print(Fore.CYAN + "│" + Fore.YELLOW + " 📺 SELECCIONA CALIDAD ".center(56) + Fore.CYAN + "│")
    print(Fore.CYAN + "├" + "─" * 56 + "┤")
    
    for i, (fid, label, size) in enumerate(calidades[:8], 1):
        if i == 1:
            color = Fore.GREEN
            estrella = "★ MEJOR"
            indicador = "▶"
        else:
            color = Fore.WHITE
            estrella = ""
            indicador = "  "
        
        label_formato = f"{indicador} {label}"
        linea = f"│ {color}{str(i).ljust(2)}. {label_formato.ljust(20)} │ {size.ljust(12)} {estrella}{Fore.CYAN}│"
        print(linea)
    
    print(Fore.CYAN + "╰" + "─" * 56 + "╯")
    print(Fore.CYAN + "   ℹ️  La opción 1 es la mejor calidad disponible")
    
    while True:
        mostrar_cursor()
        sel = input(Fore.YELLOW + "\n➜ " + Fore.CYAN + "Elige calidad [1-8]: " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        if sel.isdigit() and 1 <= int(sel) <= min(len(calidades), 8):
            calidad_elegida = calidades[int(sel) - 1]
            print(Fore.GREEN + f"   ✓ Seleccionado: {calidad_elegida[1]}")
            return calidad_elegida[0]
        
        print(Fore.RED + "   ❌ Opción inválida")


def descargar_video(url: str):
    """
    Descarga un video de una URL
    
    Args:
        url: URL del video a descargar
    """
    ocultar_cursor()

    url = resolver_facebook_url(url)
    es_tk = es_tiktok(url)
    es_fb = es_facebook(url)
    
    try:
        plataforma = "TikTok" if es_tk else ("Facebook" if es_fb else "Video")
        print(Fore.CYAN + "\n╔" + "═" * 50 + "╗")
        print(Fore.CYAN + "║" + Fore.YELLOW + f" 🎬 ANALIZANDO {plataforma.upper()} ".center(50) + Fore.CYAN + "║")
        print(Fore.CYAN + "╚" + "═" * 50 + "╝\n")
        
        if es_tk:
            print(Fore.YELLOW + " ⚠️  TikTok detectado - intentando métodos alternativos...")
            
            if descargar_tiktok_metodos(url):
                pausar()
                return
        
        if es_fb:
            print(Fore.YELLOW + " ⚠️  Facebook detectado - puede requerir cookies")
        
        if es_tk:
            return
        
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
        
        if es_tk or es_fb:
            formato_descarga = 'best'
        elif formato_id.isdigit():
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
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            },
        }
        
        pot_opts = pot_token.obtener_opts_pot()
        if pot_opts:
            ydl_opts.update(pot_opts)
            print(Fore.CYAN + " ✓ PO Token activo")
        
        if es_tk:
            ydl_opts['extractor_args'] = {
                'tiktok': {
                    'downloadaddr': True,
                    'watermark': False,
                }
            }
        elif es_fb:
            ydl_opts['extractor_args'] = {
                'facebook': {
                    'download': True,
                }
            }
        
        if es_tk or es_fb:
            ydl_opts['format'] = 'best'
        
        print()
        print(Fore.GREEN + "╭" + "─" * 54 + "╮")
        print(Fore.GREEN + "│" + Fore.YELLOW + f" 📥 DESCARGANDO {plataforma.upper()} ".center(54) + Fore.GREEN + "│")
        print(Fore.GREEN + "├" + "─" * 54 + "┤")
        print(Fore.GREEN + "│" + Fore.CYAN + "   Por favor espera... el video se está descargando".ljust(55) + Fore.GREEN + "│")
        print(Fore.GREEN + "╰" + "─" * 54 + "╯\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'video')[:35]
            duracion = info.get('duration', 0)
            archivos = list(VIDEOS_DIR.glob('*.mp4'))
            ultimo = archivos[-1] if archivos else None
            tamanho = f"{ultimo.stat().st_size / (1024*1024):.1f} MB" if ultimo else "?"
            
            min_duracion = duracion // 60
            seg_duracion = duracion % 60
        
        print()
        print(Fore.GREEN + "╭" + "─" * 54 + "╮")
        print(Fore.GREEN + "│" + Fore.YELLOW + " ✅ DESCARGA EXITOSA ".center(54) + Fore.GREEN + "│")
        print(Fore.GREEN + "├" + "─" * 54 + "┤")
        print(Fore.GREEN + "│" + Fore.CYAN + f"   📝 {titulo}".ljust(55) + Fore.GREEN + "│")
        print(Fore.GREEN + "│" + Fore.WHITE + f"   ⏱️  Duración: {min_duracion}:{seg_duracion:02d}   │   💾 Tamaño: {tamanho}".ljust(55) + Fore.GREEN + "│")
        print(Fore.GREEN + "│" + Fore.YELLOW + f"   📁 {VIDEOS_DIR.name}".ljust(55) + Fore.GREEN + "│")
        print(Fore.GREEN + "╰" + "─" * 54 + "╯")
    
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        
        if ("403" in error_msg or "Forbidden" in error_msg) and (es_tk or es_fb):
            print(Fore.YELLOW + "\n⚠️  Reintentando con método alternativo...")
            
            ydl_opts2 = {
                'format': 'best',
                'outtmpl': str(VIDEOS_DIR / '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                },
            }
            
            if es_tk:
                ydl_opts2['extractor_args'] = {'tiktok': {'no_watermark': True}}
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
                    info = ydl.extract_info(url, download=True)
                    titulo = info.get('title', 'video')[:40]
                    print(Fore.GREEN + f"\n✅ Descargado: {titulo}")
                    pausar()
                    return
            except:
                pass
        
        print(Fore.RED + "\n╭" + "─" * 54 + "╮")
        print(Fore.RED + "│" + Fore.WHITE + " ❌ ERROR DE DESCARGA ".center(54) + Fore.RED + "│")
        print(Fore.RED + "├" + "─" * 54 + "┤")
        
        if "429" in error_msg:
            print(Fore.RED + "│" + Fore.YELLOW + "   Demasiadas solicitudes. Espera unos minutos.".ljust(55) + Fore.RED + "│")
        elif "403" in error_msg or "Forbidden" in error_msg:
            if es_tk:
                print(Fore.RED + "│" + Fore.YELLOW + "   TikTok: Acceso bloqueado.".ljust(55) + Fore.RED + "│")
                print(Fore.CYAN + "│" + "   ℹ️  Usa cookies de navegador para descargar".ljust(55) + Fore.RED + "│")
            elif es_fb:
                print(Fore.RED + "│" + Fore.YELLOW + "   Facebook: Acceso bloqueado.".ljust(55) + Fore.RED + "│")
            else:
                print(Fore.RED + "│" + Fore.YELLOW + "   Acceso bloqueado. Video privado o restringido.".ljust(55) + Fore.RED + "│")
        elif "404" in error_msg:
            print(Fore.RED + "│" + Fore.YELLOW + "   Video no encontrado. Verifica la URL.".ljust(55) + Fore.RED + "│")
        else:
            print(Fore.RED + "│" + Fore.YELLOW + f"   {error_msg[:48]}".ljust(55) + Fore.RED + "│")
        
        print(Fore.RED + "╰" + "─" * 54 + "╯")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Descarga cancelada")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {str(e)[:50]}")
    
    finally:
        pausar()
