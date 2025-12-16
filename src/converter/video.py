"""
Módulo de conversión de videos
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import subprocess
from pathlib import Path
from colorama import Fore, Style

from config.settings import VIDEO_FORMATS
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.core.file_manager import generar_nombre_salida, eliminar_archivo_seguro


def convertir_video(ruta_video: Path, formato: str):
    """
    Convierte un video a otro formato
    
    Args:
        ruta_video: Path del video original
        formato: Formato de salida (mp4, mkv, avi, mov, webm)
    """
    ocultar_cursor()
    
    try:
        if not ruta_video.exists():
            print(Fore.RED + f"\n❌ Archivo no encontrado: {ruta_video}")
            pausar()
            return
        
        # Validar formato
        if formato.lower() not in VIDEO_FORMATS:
            print(Fore.RED + f"\n❌ Formato no soportado: {formato}")
            print(Fore.CYAN + f"Formatos disponibles: {', '.join(VIDEO_FORMATS)}")
            pausar()
            return
        
        # Generar nombre de salida
        ruta_salida = generar_nombre_salida(ruta_video, "_convertido", formato)
        
        print(Fore.YELLOW + f"\n🔄 Convirtiendo video a .{formato.upper()}...")
        print(Fore.CYAN + "⏳ Esto puede tomar varios minutos...\n")
        
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
            
            print(Fore.GREEN + f"\n\n🎉 ¡Video convertido exitosamente!")
            print(Fore.WHITE + f"   📝 Nombre: {ruta_salida.name}")
            print(Fore.WHITE + f"   📦 Formato: {formato.upper()}")
            print(Fore.WHITE + f"   💾 Tamaño: {tamaño_mb:.2f} MB")
            print(Fore.WHITE + f"   📁 Ubicación: {ruta_salida.parent}")
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_video)
        else:
            print(Fore.RED + "\n\n❌ Error durante la conversión")
            print(Fore.YELLOW + "💡 Verifica que FFmpeg esté instalado correctamente")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ FFmpeg no está instalado")
        print(Fore.CYAN + "Instálalo con: pkg install ffmpeg")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Conversión cancelada por el usuario")
        # Limpiar archivo incompleto
        if ruta_salida.exists():
            ruta_salida.unlink()
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
    
    finally:
        pausar()
