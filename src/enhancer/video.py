"""
Video quality enhancement module
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import subprocess
from pathlib import Path
from colorama import Fore, Style

from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import pausar
from src.utils.boxes import print_success_box, print_selection_box
from src.core.file_manager import generar_nombre_salida, eliminar_archivo_seguro


def obtener_resolucion() -> str:
    """
    Let the user pick la resolución de salida
    
    Returns:
        Resolution string (e.g.: "1920x1080")
    """
    opciones = [
        ("1", "720p", "1280x720", "HD - Fast"),
        ("2", "1080p", "1920x1080", "Full HD - Recommended"),
        ("3", "4k", "3840x2160", "4K - Max quality")
    ]

    lineas = []
    colores = []
    for num, label, res, desc in opciones:
        estrella = "⭐ " if num == "2" else "   "
        lineas.append(f"{estrella}{num}. {label.upper()} ({res}) - {desc}")
        colores.append(Fore.GREEN if num == "2" else Fore.WHITE)

    print_selection_box("📺 OUTPUT QUALITY", lineas, colores)
    
    while True:
        mostrar_cursor()
        choice = input(Fore.CYAN + "\n➜ Pick [1-3] (2=recommended): " + Style.RESET_ALL).strip()
        ocultar_cursor()
        
        opciones_dict = {"1": "1280x720", "2": "1920x1080", "3": "3840x2160"}
        if choice in opciones_dict:
            return opciones_dict[choice]
        
        print(Fore.RED + "❌ Invalid option")


def mejorar_calidad_video(ruta_video: Path):
    """
    Enhance video quality via upscaling
    
    Args:
        ruta_video: Original video Path
    """
    ocultar_cursor()
    
    ruta_salida = None
    
    try:
        if not ruta_video.exists():
            print(Fore.RED + f"\n❌ File not found: {ruta_video}")
            return
        
        # Seleccionar resolución
        resolucion = obtener_resolucion()
        
        # Generar nombre de salida
        ruta_salida = generar_nombre_salida(ruta_video, "_enhanced")
        
        print(Fore.YELLOW + f"\n⬆️  Enhancing video to {resolucion}...")
        print(Fore.CYAN + "⏳ This may take quite a while...\n")
        print(Fore.MAGENTA + "💡 Tip: This process is intensive. Be patient.\n")
        
        # Comando FFmpeg optimizado para upscaling
        # force_original_aspect_ratio=decrease evita distorsión y
        # el filtro pad redondea a dimensiones pares (requerido por x264)
        comando = [
            "ffmpeg",
            "-i", str(ruta_video),
            "-vf", f"scale={resolucion}:force_original_aspect_ratio=decrease:flags=lanczos,pad=ceil(iw/2)*2:ceil(ih/2)*2",
            "-c:v", "libx264",
            "-preset", "slow",  # Mejor calidad (más lento)
            "-crf", "18",  # Calidad alta (18-23 es bueno, menor=mejor)
            "-c:a", "copy",  # Copiar audio sin recodificar
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
            if any(keyword in linea for keyword in ['frame=', 'fps=', 'time=', 'speed=']):
                print(f"\r{Fore.CYAN}{linea[:80]}", end="", flush=True)
        
        process.wait()
        
        # Verificar resultado
        if process.returncode == 0 and ruta_salida.exists():
            tamaño_original = ruta_video.stat().st_size / (1024 * 1024)
            tamaño_nuevo = ruta_salida.stat().st_size / (1024 * 1024)

            print_success_box("✅ VIDEO ENHANCED SUCCESSFULLY", [
                f"📝 Name: {ruta_salida.name}",
                f"📺 Resolution: {resolucion}",
                f"💾 Original size: {tamaño_original:.2f} MB",
                f"💾 Final size: {tamaño_nuevo:.2f} MB",
                f"📁 {ruta_salida.parent}",
            ], [Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.WHITE, Fore.CYAN])

            print(Fore.CYAN + "\n💡 Video enhanced with Lanczos algorithm (high quality)")
            
            # Preguntar si eliminar original
            eliminar_archivo_seguro(ruta_video)
        else:
            print(Fore.RED + "\n\n❌ Error during processing")
            print(Fore.YELLOW + "💡 Check that FFmpeg is installed correctly")
    
    except FileNotFoundError:
        print(Fore.RED + "\n❌ FFmpeg is not installed")
        print(Fore.CYAN + "Install it with: pkg install ffmpeg")
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Process cancelled by user")
        if ruta_salida and ruta_salida.exists():
            ruta_salida.unlink()
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {str(e)}")
    
    finally:
        pausar()
