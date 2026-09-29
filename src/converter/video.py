"""
Video conversion module
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import subprocess
from pathlib import Path
from colorama import Fore

from config.settings import VIDEO_FORMATS
from src.utils.animations import ocultar_cursor
from src.utils.helpers import pausar
from src.utils.boxes import print_success_box
from src.core.file_manager import generar_nombre_salida, eliminar_archivo_seguro


def convertir_video(ruta_video: Path, formato: str):
    """
    Convert a video to another format
    
    Args:
        ruta_video: Original video Path
        formato: Output format (mp4, mkv, avi, mov, webm)
    """
    ocultar_cursor()
    
    ruta_salida = None
    
    try:
        if not ruta_video.exists():
            print(Fore.RED + f"\n❌ File not found: {ruta_video}")
            return
        
        if formato.lower() not in VIDEO_FORMATS:
            print(Fore.RED + f"\n❌ Unsupported format: {formato}")
            print(Fore.CYAN + f"Available formats: {', '.join(VIDEO_FORMATS)}")
            return
        
        # Generar nombre de salida
        ruta_salida = generar_nombre_salida(ruta_video, "_converted", formato)
        
        print(Fore.YELLOW + f"\n🔄 Converting video to .{formato.upper()}...")
        print(Fore.CYAN + "⏳ This may take several minutes...\n")
        
        # Configurar codec según formato
        if formato in ["mp4", "mov"]:
            video_codec = "libx264"
            audio_codec = "aac"
        elif formato == "webm":
            video_codec = "libvpx-vp9"
            audio_codec = "libopus"
        else:  # mkv, avi
            video_codec = "copy"
            audio_codec = "copy"
        
        # Comando FFmpeg optimizado
        comando = [
            "ffmpeg", "-i", str(ruta_video),
            "-c:v", video_codec,
            "-c:a", audio_codec,
            "-preset", "medium",
            "-crf", "23",  # Calidad balanceada
            "-map_metadata", "0",  # Preservar metadatos
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
            if any(keyword in linea for keyword in ['frame=', 'time=', 'speed=']):
                print(f"\r{Fore.CYAN}{linea[:80]}", end="", flush=True)
        
        process.wait()
        
        # Verificar resultado
        if process.returncode == 0 and ruta_salida.exists():
            tamaño_mb = ruta_salida.stat().st_size / (1024 * 1024)

            print_success_box("✅ VIDEO CONVERTED SUCCESSFULLY", [
                f"📝 Name: {ruta_salida.name}",
                f"📦 Format: {formato.upper()}",
                f"💾 Size: {tamaño_mb:.2f} MB",
                f"📁 {ruta_salida.parent}",
            ])
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_video)
        else:
            print(Fore.RED + "\n\n❌ Error during conversion")
            print(Fore.YELLOW + "💡 Check that FFmpeg is installed correctly")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ FFmpeg is not installed")
        print(Fore.CYAN + "Install it with: pkg install ffmpeg")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Conversion cancelled by user")
        # Limpiar archivo incompleto
        if ruta_salida and ruta_salida.exists():
            ruta_salida.unlink()
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {str(e)}")
    
    finally:
        pausar()
