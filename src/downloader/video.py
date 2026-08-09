"""
Módulo de descarga de videos
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import yt_dlp
from pathlib import Path
from colorama import Fore, Style

from config.settings import VIDEOS_DIR
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.utils import pot_token
from src.utils.boxes import (
    print_info_box, print_success_box, print_error_box, print_selection_box,
    print_progress_bar, print_progress_done
)


def es_facebook(url: str) -> bool:
    """Detecta si la URL es de Facebook (cualquier tipo)"""
    url_lower = url.lower()
    return (
        'facebook.com' in url_lower or
        'fb.com' in url_lower or
        'fb.watch' in url_lower or
        'fb.gg' in url_lower
    )


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


def obtener_archivo_descargado(info: dict) -> Path:
    """
    Obtiene el Path del archivo descargado desde la info de yt-dlp
    """
    try:
        for download in info.get('requested_downloads', []):
            filepath = download.get('filepath')
            rutas = filepath if isinstance(filepath, list) else [filepath]
            for ruta in rutas:
                if ruta and Path(ruta).exists():
                    return Path(ruta)
    except Exception:
        pass
    return None


def progreso_hook(d):
    """Hook para mostrar progreso de descarga"""
    if d['status'] == 'downloading':
        try:
            percent = d.get('_percent_str', '0%').strip()
            speed = d.get('_speed_str', 'N/A').strip()
            eta = d.get('_eta_str', '...').strip()

            porcentaje_num = float(percent.replace('%', ''))
            print_progress_bar(porcentaje_num, speed, eta)
        except:
            pass
    elif d['status'] == 'finished':
        print_progress_done()


def es_tiktok(url: str) -> bool:
    """Detecta si la URL es de TikTok"""
    url_lower = url.lower()
    return 'tiktok.com' in url_lower or 'vm.tiktok.com' in url_lower or 'musical.ly' in url_lower


def obtener_opciones_ytdlp(es_tiktok: bool = False, cookies_path: str = None, es_facebook: bool = False) -> dict:
    """Obtiene opciones optimizadas para yt-dlp"""
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


def obtener_calidades_video(url: str) -> list:
    """
    Obtiene las calidades disponibles para un video
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
    """Permite al usuario seleccionar una calidad"""
    if not calidades:
        print_error_box("❌ NO HAY FORMATOS", ["No hay formatos de video disponibles"])
        return None

    lines = []
    colors = []
    for i, (fid, label, size) in enumerate(calidades[:8]):
        if i == 0:
            colors.append(Fore.GREEN)
            lines.append(f"▶ {i+1}. {label:<20} {size}")
        else:
            colors.append(Fore.WHITE)
            lines.append(f"  {i+1}. {label:<20} {size}")

    print_selection_box("📺 SELECCIONA CALIDAD", lines, colors)
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


def _descargar_con_opts(url: str, ydl_opts: dict, plataforma: str) -> bool:
    """Descarga interna común. Retorna True si éxito."""
    try:
        print()
        print_success_box(f"📥 DESCARGANDO {plataforma.upper()}", [
            "Por favor espera... el video se está descargando"
        ])

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'video')[:35]
            duracion = info.get('duration', 0)
            archivo = obtener_archivo_descargado(info)
            tamanho = f"{archivo.stat().st_size / (1024*1024):.1f} MB" if archivo else "?"

            min_duracion = duracion // 60
            seg_duracion = duracion % 60

        print()
        print_success_box("✅ DESCARGA EXITOSA", [
            f"📝 {titulo}",
            f"⏱️  Duración: {min_duracion}:{seg_duracion:02d}   │   💾 Tamaño: {tamanho}",
            f"📁 {VIDEOS_DIR.name}"
        ])
        return True

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        _mostrar_error_descarga(error_msg, plataforma, es_tiktok(url), es_facebook(url))
        return False
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Descarga cancelada")
        return False
    except Exception as e:
        print_error_box("❌ ERROR", [f"Error: {str(e)[:50]}"])
        return False


def _mostrar_error_descarga(error_msg: str, plataforma: str, es_tk: bool, es_fb: bool):
    """Muestra error de descarga en caja consistente"""
    lines = []
    if "429" in error_msg:
        lines.append("Demasiadas solicitudes. Espera unos minutos.")
    elif "403" in error_msg or "Forbidden" in error_msg:
        if es_tk:
            lines.extend(["TikTok: Acceso bloqueado.", "Usa cookies de navegador para descargar"])
        elif es_fb:
            lines.append("Facebook: Acceso bloqueado.")
        else:
            lines.append("Acceso bloqueado. Video privado o restringido.")
    elif "404" in error_msg:
        lines.append("Video no encontrado. Verifica la URL.")
    else:
        lines.append(error_msg[:50])
    print_error_box("❌ ERROR DE DESCARGA", lines)


def descargar_video(url: str):
    """
    Descarga un video de una URL
    """
    ocultar_cursor()

    url = resolver_facebook_url(url)
    es_tk = es_tiktok(url)
    es_fb = es_facebook(url)

    try:
        plataforma = "TikTok" if es_tk else ("Facebook" if es_fb else "Video")

        # Caja de análisis (info)
        print_info_box(f"🎬 ANALIZANDO {plataforma.upper()}")

        if es_tk:
            print(Fore.YELLOW + " ⚠️  TikTok detectado - intentando métodos alternativos...")

            # Intentar métodos TikTok simplificados
            metodos = [
                {'quiet': False, 'no_warnings': False, 'extractor_args': {}},
                {
                    'quiet': False, 'no_warnings': False,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
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

                print(f"  ⏳ Método {i+1}/{len(metodos)}...")
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        if info:
                            titulo = info.get('title', 'video')[:35]
                            archivo = obtener_archivo_descargado(info)
                            tamanho = f"{archivo.stat().st_size / (1024*1024):.1f} MB" if archivo else "?"
                            print()
                            print_success_box("✅ DESCARGA COMPLETADA", [
                                f"📝 {titulo}",
                                f"💾 Tamaño: {tamanho}",
                                f"📁 {VIDEOS_DIR.name}"
                            ])
                            pausar()
                            return
                except Exception:
                    continue

            print_error_box("❌ ERROR TIKTOK", ["No se pudo descargar con métodos disponibles"])
            return

        if es_fb:
            print(Fore.YELLOW + " ⚠️  Facebook detectado - puede requerir cookies")

        # Obtener calidades para selección
        calidades = obtener_calidades_video(url)

        if not calidades:
            print_error_box("❌ SIN CALIDADES", ["No se pudieron obtener las calidades disponibles"])
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

        _descargar_con_opts(url, ydl_opts, plataforma)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Descarga cancelada")
    except Exception as e:
        print_error_box("❌ ERROR", [f"Error: {str(e)[:50]}"])
    finally:
        pausar()