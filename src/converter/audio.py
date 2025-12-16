"""
Módulo de conversión de audio
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import subprocess
from pathlib import Path
from colorama import Fore, Style

from config.settings import AUDIO_FORMATS, AUDIO_EXTENSIONS, FORMATS_WITH_COVER
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.core.file_manager import eliminar_archivo_seguro


def convertir_audio(ruta_audio: Path, formato: str):
    """
    Convierte un audio a otro formato preservando portada y metadatos
    
    Args:
        ruta_audio: Path del audio original
        formato: Formato de salida (mp3, wav, aac, flac, ogg, m4a)
    """
    ocultar_cursor()
    
    try:
        if not ruta_audio.exists():
            print(Fore.RED + f"\n❌ Archivo no encontrado: {ruta_audio}")
            pausar()
            return
        
        # Validar formato
        formato = formato.lower()
        if formato not in AUDIO_FORMATS:
            print(Fore.RED + f"\n❌ Formato no soportado: {formato}")
            print(Fore.CYAN + f"Formatos disponibles: {', '.join(AUDIO_FORMATS)}")
            pausar()
            return
        
        # Generar nombre de salida con extensión correcta
        nombre_base = ruta_audio.stem
        extension = AUDIO_EXTENSIONS.get(formato, formato)
        ruta_salida = ruta_audio.parent / f"{nombre_base}_convertido.{extension}"
        
        # Título para mostrar
        titulo = "AAC → .M4A" if formato == "aac" else formato.upper()
        
        print(Fore.YELLOW + f"\n🔄 Convirtiendo audio a {titulo}...")
        print(Fore.CYAN + "⏳ Preservando portada y metadatos...\n")
        
        # Construir comando base
        comando = ["ffmpeg", "-i", str(ruta_audio)]
        
        # Manejo especial de portada según formato
        if formato in FORMATS_WITH_COVER:
            if formato == "ogg":
                # OGG requiere PNG para portada
                comando += [
                    "-map", "0:v?",
                    "-c:v", "png",
                    "-disposition:v", "attached_pic"
                ]
            else:
                # MP3, FLAC, M4A, AAC: copiar portada directamente
                comando += [
                    "-map", "0:v?",
                    "-c:v", "copy",
                    "-disposition:v", "attached_pic"
                ]
        
        # Mapear audio
        comando += ["-map", "0:a"]
        
        # Configurar codec de audio según formato
        if formato == "mp3":
            comando += ["-c:a", "libmp3lame", "-b:a", "320k", "-q:a", "0"]
        elif formato == "wav":
            comando += ["-c:a", "pcm_s16le"]
        elif formato == "flac":
            comando += ["-c:a", "flac", "-compression_level", "8"]
        elif formato in ["aac", "m4a"]:
            comando += ["-c:a", "aac", "-b:a", "320k"]
        elif formato == "ogg":
            comando += ["-c:a", "libvorbis", "-q:a", "9"]
        
        # Preservar metadatos
        comando += ["-map_metadata", "0", "-y", str(ruta_salida)]
        
        # Ejecutar conversión con progreso
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
            if any(keyword in linea for keyword in ['time=', 'size=', 'bitrate=', 'speed=']):
                print(f"\r{Fore.CYAN}{linea[:80]}", end="", flush=True)
        
        process.wait()
        
        # Verificar resultado
        if process.returncode == 0 and ruta_salida.exists() and ruta_salida.stat().st_size > 50000:
            tamaño_mb = ruta_salida.stat().st_size / (1024 * 1024)
            
            print(Fore.GREEN + f"\n\n🎉 ¡Audio convertido exitosamente!")
            
            # Mensaje sobre portada
            if formato in FORMATS_WITH_COVER:
                print(Fore.GREEN + "   🖼️  Portada preservada correctamente")
            elif formato == "wav":
                print(Fore.YELLOW + "   ⚠️  WAV no soporta portadas")
            
            print(Fore.WHITE + f"   📝 Nombre: {ruta_salida.name}")
            print(Fore.WHITE + f"   📦 Formato: {titulo}")
            print(Fore.WHITE + f"   💾 Tamaño: {tamaño_mb:.2f} MB")
            print(Fore.WHITE + f"   📁 Ubicación: {ruta_salida.parent}")
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_audio)
        else:
            print(Fore.RED + "\n\n❌ Error durante la conversión")
            print(Fore.YELLOW + "💡 Verifica que FFmpeg esté instalado correctamente")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ FFmpeg no está instalado")
        print(Fore.CYAN + "Instálalo con: pkg install ffmpeg")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Conversión cancelada por el usuario")
        if ruta_salida.exists():
            ruta_salida.unlink()
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Error inesperado: {str(e)}")
    
    finally:
        pausar()
