"""
Módulo de descarga de audio
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import yt_dlp
from colorama import Fore, Style
from typing import Optional, Tuple, List

from config.settings import AUDIO_DIR
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.utils import pot_token
from src.utils.boxes import (
    print_info_box, print_success_box, print_error_box, print_selection_box,
    print_progress_bar, print_progress_done
)


def es_tiktok(url: str) -> bool:
    return 'tiktok.com' in url.lower()


def es_youtube(url: str) -> bool:
    return 'youtube.com' in url.lower() or 'youtu.be' in url.lower()


def obtener_opts_base() -> dict:
    """Retorna opciones base para yt-dlp"""
    return {
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        },
    }


def obtener_calidades_audio(url: str) -> Optional[Tuple[List, dict]]:
    """
    Obtiene las calidades de audio disponibles
    Retorna: (lista_formatos, ydl_opts) o None si falla
    """
    pot_iniciado = pot_token.iniciar_si_necesario()
    pot_opts = pot_token.obtener_opts_audio() if pot_iniciado else {}

    metodos = [pot_opts, {}]

    for extra_opts in metodos:
        ydl_opts = obtener_opts_base()
        ydl_opts.update(extra_opts)

        if es_tiktok(url):
            ydl_opts.setdefault('extractor_args', {})
            ydl_opts['extractor_args']['tiktok'] = {'downloadaddr': True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formatos = []
                visto = set()

                for f in info.get('formats', []):
                    if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                        acodec = f.get('acodec', '')
                        ext = f.get('ext', 'm4a')
                        filesize = f.get('filesize') or f.get('filesize_approx', 0)
                        size_mb = f"{filesize / (1024*1024):.1f} MB" if filesize else "?? MB"

                        if 'mp3' in acodec.lower():
                            label = "MP3"
                        elif 'aac' in acodec.lower():
                            label = "AAC"
                        elif 'opus' in acodec.lower():
                            label = "Opus"
                        elif 'vorbis' in acodec.lower():
                            label = "OGG"
                        else:
                            label = ext.upper()

                        key = (label, ext)
                        if key not in visto:
                            visto.add(key)
                            formatos.append((f['format_id'], label, size_mb))

                if not formatos:
                    formatos = [("bestaudio", "Best", "?? MB")]

                return formatos[:8], ydl_opts

        except Exception as e:
            ultimo_error = str(e)
            if "Sign in to confirm" in ultimo_error:
                pot_token.mensaje_error_youtube()
                return None, None
            continue

    return None, None


def seleccionar_calidad(calidades: list) -> str:
    """Permite seleccionar la calidad de audio"""
    lines = []
    colors = []
    for i, (fid, label, size) in enumerate(calidades[:6]):
        if i == 0:
            colors.append(Fore.GREEN)
            lines.append(f"▶ {i+1}. {label:<12} {size}")
        else:
            colors.append(Fore.WHITE)
            lines.append(f"  {i+1}. {label:<12} {size}")

    print_selection_box("🎵 CALIDADES DE AUDIO", lines, colors)

    while True:
        mostrar_cursor()
        sel = input(Fore.CYAN + "\n➜ Elige calidad [1-6]: " + Style.RESET_ALL).strip()
        ocultar_cursor()

        if sel.isdigit() and 1 <= int(sel) <= min(len(calidades), 6):
            return calidades[int(sel) - 1][0]

        print(Fore.RED + "❌ Opción inválida")


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


def formatear_audio(formato_id: str) -> str:
    """Genera el formato de descarga con fallback progresivo"""
    if formato_id == "bestaudio":
        return "bestaudio/best"
    return f"{formato_id}+bestaudio/{formato_id}/bestaudio/best"


def verificar_ffmpeg() -> bool:
    """Verifica si ffmpeg está disponible"""
    import subprocess
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def descargar_audio(url: str):
    """Descarga audio de una URL y convierte a MP3"""
    ocultar_cursor()

    ffmpeg_ok = verificar_ffmpeg()

    try:
        # Caja de análisis
        print_info_box("🎵 ANALIZANDO AUDIO")

        resultado = obtener_calidades_audio(url)

        calidades, opts_usados = resultado

        if not calidades:
            print_error_box("❌ SIN CALIDADES", ["No se pudieron obtener las calidades de audio"])
            return

        formato_id = seleccionar_calidad(calidades)

        print_success_box("📥 DESCARGANDO AUDIO", [
            "Por favor espera... el audio se está descargando"
        ])

        # Usar los mismos opts que se usaron para obtener las calidades
        ydl_opts = opts_usados.copy()
        ydl_opts['outtmpl'] = str(AUDIO_DIR / '%(title)s.%(ext)s')
        ydl_opts['format'] = formatear_audio(formato_id)
        ydl_opts['progress_hooks'] = [progreso_hook]
        ydl_opts['writethumbnail'] = True

        # Postprocessors para MP3
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]

        if ffmpeg_ok:
            postprocessors.append({'key': 'EmbedThumbnail'})
        else:
            print(Fore.YELLOW + " ⚠️  ffmpeg no disponible - sin portada")

        postprocessors.append({
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        })

        ydl_opts['postprocessors'] = postprocessors

        if pot_token.iniciar_si_necesario():
            print(Fore.CYAN + " ✓ PO Token activo")

        if es_tiktok(url):
            ydl_opts.setdefault('extractor_args', {})
            ydl_opts['extractor_args']['tiktok'] = {'downloadaddr': True}
            print(Fore.YELLOW + " ⚠️  TikTok detectado")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'audio')[:40]
            duracion = info.get('duration', 0)
            min_dur = duracion // 60
            seg_dur = duracion % 60

        print()
        print_success_box("✅ DESCARGA COMPLETADA", [
            f"📝 Título: {titulo}",
            f"⏱️  Duración: {min_dur}:{seg_dur:02d}",
            "📁 Music/Music_Downloader"
        ])

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Descarga cancelada")
    except Exception as e:
        error_str = str(e)
        if "Requested format" in error_str:
            print_error_box("❌ ERROR", ["Formato no disponible, intenta con otra calidad"])
        else:
            print_error_box("❌ ERROR", [f"Error: {error_str[:50]}"])
    finally:
        pausar()