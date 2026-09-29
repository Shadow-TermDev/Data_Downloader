"""
YouTube PO Token manager
Author: Shadow-TermDev

This module uses bgutil-ytdlp-pot-provider to auto-generate PO Tokens
when yt-dlp needs them.
"""

import subprocess
import sys
from colorama import Fore

_instalado = False
_verificado = False


def verificar_instalacion() -> bool:
    """
    Check if bgutil-ytdlp-pot-provider is installed
    """
    global _instalado, _verificado
    
    if _verificado:
        return _instalado
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "bgutil-ytdlp-pot-provider"],
            capture_output=True,
            text=True,
            timeout=10
        )
        _instalado = result.returncode == 0
    except Exception:
        _instalado = False
    
    _verificado = True
    
    if not _instalado:
        print(Fore.RED + "\n⚠️  PO Token provider is not installed")
        print(Fore.YELLOW + "   → Install with: pip install bgutil-ytdlp-pot-provider")
    
    return _instalado


def iniciar_si_necesario() -> bool:
    """
    Check and init the PO Token if available
    """
    return verificar_instalacion()


def obtener_opts_pot() -> dict:
    """
    Return options to use PO Token with yt-dlp
    The bgutil plugin activates automatically when installed
    """
    if not verificar_instalacion():
        return {}
    
    return {
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        }
    }


def obtener_opts_video() -> dict:
    """
    Optimized video options with PO Token
    """
    opts = {
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    pot_opts = obtener_opts_pot()
    if pot_opts:
        opts.update(pot_opts)
    return opts


def obtener_opts_audio() -> dict:
    """
    Optimized audio options with PO Token
    """
    return obtener_opts_video()


def mensaje_error_youtube():
    """
    Show an error message when YouTube fails
    """
    if verificar_instalacion():
        print(Fore.YELLOW + "\n⚠️  YouTube is blocking this IP")
        print(Fore.CYAN + "   → Try a VPN or wait a few minutes")
    else:
        print(Fore.RED + "\n⚠️  YouTube is blocking downloads")
        print(Fore.YELLOW + "   → Install PO Token: pip install bgutil-ytdlp-pot-provider")
    print(Fore.CYAN + "   → Or use cookies: yt-dlp --cookies-from-browser chrome URL")


# English aliases
check_installed = verificar_instalacion
ensure_started = iniciar_si_necesario
get_pot_opts = obtener_opts_pot
get_video_opts = obtener_opts_video
get_audio_opts = obtener_opts_audio
