"""
Módulo de mejora de calidad de audio
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import subprocess
from pathlib import Path
from colorama import Fore, Style

from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.utils.boxes import print_success_box, print_selection_box
from src.core.file_manager import generar_nombre_salida, eliminar_archivo_seguro


def seleccionar_calidad() -> str:
    """
    Permite seleccionar el bitrate de salida
    
    Returns:
        String de bitrate (ej: "320k")
    """
    opciones = [
        ("1", "128k", "128 kbps", "Calidad estándar"),
        ("2", "256k", "256 kbps", "Alta calidad - Recomendado"),
        ("3", "320k", "320 kbps", "Calidad máxima")
    ]

    lineas = []
    colores = []
    for num, bitrate, label, desc in opciones:
        estrella = "⭐ " if num == "2" else "   "
        lineas.append(f"{estrella}{num}. {label} - {desc}")
        colores.append(Fore.GREEN if num == "2" else Fore.WHITE)

    print_selection_box("🎵 CALIDAD DE AUDIO", lineas, colores)
    
    while True:
        mostrar_cursor()
        choice = input(Fore.CYAN + "\n➜ Elige [1-3] (2=recomendado): " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        opciones_dict = {"1": "128k", "2": "256k", "3": "320k"}
        if choice in opciones_dict:
            return opciones_dict[choice]
        
        print(Fore.RED + "❌ Opción inválida")


def mejorar_calidad_audio(ruta_audio: Path):
    """
    Mejora la calidad de un audio aumentando el bitrate
    Preserva portada y metadatos
    
    Args:
        ruta_audio: Path del audio original
    """
    ocultar_cursor()
    
    ruta_salida = None
    
    try:
        if not ruta_audio.exists():
            print(Fore.RED + f"\n❌ Archivo no encontrado: {ruta_audio}")
            return
        
        # Seleccionar bitrate
        bitrate = seleccionar_calidad()
        
        # Generar nombre de salida (siempre MP3)
        ruta_salida = generar_nombre_salida(ruta_audio, "_mejorado", "mp3")
        
        print(Fore.YELLOW + f"\n⬆️  Mejorando audio a {bitrate}...")
        print(Fore.CYAN + "⏳ Preservando portada y metadatos...\n")
        
        # Comando FFmpeg: convierte a MP3 y conserva portada y metadatos
        comando = [
            "ffmpeg",
            "-i", str(ruta_audio),
            "-map", "0:a?",
            "-map", "0:v?",
            "-c:a", "libmp3lame",
            "-b:a", bitrate,
            "-c:v", "copy",
            "-disposition:v", "attached_pic",
            "-id3v2_version", "3",
            "-map_metadata", "0",
            "-y",
            str(ruta_salida)
        ]
        
        # Ejecutar con progreso
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
            if any(keyword in linea for keyword in ['time=', 'size=', 'bitrate=']):
                print(f"\r{Fore.CYAN}{linea[:80]}", end="", flush=True)
        
        process.wait()
        
        # Verificar resultado
        if process.returncode == 0 and ruta_salida.exists():
            tamaño_original = ruta_audio.stat().st_size / (1024 * 1024)
            tamaño_nuevo = ruta_salida.stat().st_size / (1024 * 1024)

            print_success_box("✅ AUDIO MEJORADO EXITOSAMENTE", [
                "🖼️  Portada preservada",
                "📝 Metadatos preservados",
                f"📝 Nombre: {ruta_salida.name}",
                f"🎵 Bitrate: {bitrate}",
                f"💾 Tamaño original: {tamaño_original:.2f} MB",
                f"💾 Tamaño final: {tamaño_nuevo:.2f} MB",
                f"📁 {ruta_salida.parent}",
            ], [Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.CYAN])
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_audio)
        else:
            print(Fore.RED + "\n\n❌ Error al procesar el audio")
            print(Fore.YELLOW + "💡 Verifica que FFmpeg esté instalado correctamente")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ FFmpeg no está instalado")
        print(Fore.CYAN + "Instálalo con: pkg install ffmpeg")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Proceso cancelado por el usuario")
        if ruta_salida and ruta_salida.exists():
            ruta_salida.unlink()
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
    
    finally:
        pausar()
