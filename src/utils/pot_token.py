"""
Módulo de gestión de PO Token para YouTube
Autor: Shadow-TermDev

Este módulo usa bgutil-ytdlp-pot-provider para generar PO Tokens
automáticamente cuando yt-dlp los necesita.
"""

import subprocess
import sys
from colorama import Fore

_instalado = False
_verificado = False


def verificar_instalacion() -> bool:
    """
    Verifica si bgutil-ytdlp-pot-provider está instalado
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
        print(Fore.RED + "\n⚠️  PO Token Provider no está instalado")
        print(Fore.YELLOW + "   → Instala con: pip install bgutil-ytdlp-pot-provider")
    
    return _instalado


def iniciar_si_necesario() -> bool:
    """
    Verifica e inicializa el PO Token si está disponible
    """
    return verificar_instalacion()


def obtener_opts_pot() -> dict:
    """
    Retorna las opciones para usar PO Token con yt-dlp
    El plugin bgutil se activa automáticamente al estar instalado
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
    Opciones optimizadas para video con PO Token
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
    Opciones optimizadas para audio con PO Token
    """
    return obtener_opts_video()


def mensaje_error_youtube():
    """
    Muestra mensaje de error cuando YouTube falla
    """
    if verificar_instalacion():
        print(Fore.YELLOW + "\n⚠️  YouTube está bloqueando esta IP")
        print(Fore.CYAN + "   → Intenta usar VPN o esperar unos minutos")
    else:
        print(Fore.RED + "\n⚠️  YouTube está bloqueando las descargas")
        print(Fore.YELLOW + "   → Instala PO Token: pip install bgutil-ytdlp-pot-provider")
    print(Fore.CYAN + "   → O usa cookies: yt-dlp --cookies-from-browser chrome URL")
