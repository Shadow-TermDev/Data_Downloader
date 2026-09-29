"""
Audio download module
Author: Shadow-TermDev
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
    url_lower = url.lower()
    return 'tiktok.com' in url_lower or 'vm.tiktok.com' in url_lower or 'musical.ly' in url_lower


def es_youtube(url: str) -> bool:
    return 'youtube.com' in url.lower() or 'youtu.be' in url.lower()


def obtener_opts_base() -> dict:
    """Return base yt-dlp options"""
    return {
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        },
    }


def obtener_calidades_audio(url: str) -> Optional[Tuple[List, dict]]:
    """
    Get available audio qualities
    Returns: (format_list, ydl_opts) or None on failure
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
    """Let the user pick la calidad de audio"""
    lines = []
    colors = []
    for i, (fid, label, size) in enumerate(calidades[:6]):
        if i == 0:
            colors.append(Fore.GREEN)
            lines.append(f"▶ {i+1}. {label:<12} {size}")
        else:
            colors.append(Fore.WHITE)
            lines.append(f"  {i+1}. {label:<12} {size}")

    print_selection_box("🎵 AUDIO QUALITIES", lines, colors)

    while True:
        mostrar_cursor()
        sel = input(Fore.CYAN + "\n➜ Pick quality [1-6]: " + Style.RESET_ALL).strip()
        ocultar_cursor()

        if sel.isdigit() and 1 <= int(sel) <= min(len(calidades), 6):
            return calidades[int(sel) - 1][0]

        print(Fore.RED + "❌ Invalid option")


def progreso_hook(d):
    """Hook to show download progress"""
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
    """Build the download format with progressive fallback"""
    if formato_id == "bestaudio":
        return "bestaudio/best"
    return f"{formato_id}+bestaudio/{formato_id}/bestaudio/best"


def verificar_ffmpeg() -> bool:
    """Check if ffmpeg is available"""
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
    """Download audio from a URL and convert to MP3"""
    ocultar_cursor()

    ffmpeg_ok = verificar_ffmpeg()

    try:
        # Caja de análisis
        print_info_box("🎵 ANALYZING AUDIO")

        resultado = obtener_calidades_audio(url)

        calidades, opts_usados = resultado

        if not calidades:
            print_error_box("❌ NO QUALITIES", ["Could not fetch qualities de audio"])
            return

        formato_id = seleccionar_calidad(calidades)

        print_success_box("📥 DOWNLOADING AUDIO", [
            "Please wait... audio is downloading"
        ])

        # Usar los mismos opts que se usaron para obtener las calidades
        ydl_opts = opts_usados.copy()
        ydl_opts['outtmpl'] = str(AUDIO_DIR / '%(title)s.%(ext)s')
        ydl_opts['format'] = formatear_audio(formato_id)
        ydl_opts['progress_hooks'] = [progreso_hook]

        # Postprocessors para MP3
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]

        if ffmpeg_ok:
            # Solo descargar portada si se puede incrustar
            ydl_opts['writethumbnail'] = True
            postprocessors.append({'key': 'EmbedThumbnail'})
        else:
            print(Fore.YELLOW + " ⚠️  ffmpeg no disponible - sin portada")

        postprocessors.append({
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        })

        ydl_opts['postprocessors'] = postprocessors

        if pot_token.iniciar_si_necesario():
            print(Fore.CYAN + " ✓ PO Token active")

        if es_tiktok(url):
            ydl_opts.setdefault('extractor_args', {})
            ydl_opts['extractor_args']['tiktok'] = {'downloadaddr': True}
            print(Fore.YELLOW + " ⚠️  TikTok detected")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'audio')[:40]
            duracion = info.get('duration', 0)
            min_dur = duracion // 60
            seg_dur = duracion % 60

        print()
        print_success_box("✅ DOWNLOAD COMPLETED", [
            f"📝 Title: {titulo}",
            f"⏱️  Duration: {min_dur}:{seg_dur:02d}",
            "📁 Music/Music_Downloader"
        ])

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Download cancelled")
    except Exception as e:
        error_str = str(e)
        if "Requested format" in error_str:
            print_error_box("❌ ERROR", ["Format unavailable, try another quality"])
        else:
            print_error_box("❌ ERROR", [f"Error: {error_str[:50]}"])
    finally:
        pausar()