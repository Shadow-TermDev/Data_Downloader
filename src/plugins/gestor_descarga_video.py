import os
import yt_dlp
from colorama import Fore, Style
from src.utils import BASE_VIDEOS as ruta_videos, pausar
from src.plugins.animaciones import ocultar_cursor, mostrar_cursor

def progreso_hook(d):
    if d['status'] == 'downloading':
        try:
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', '0')
            eta = d.get('_eta_str', 'Calculando...')
            print(f"\r{Fore.YELLOW}📥 Descargando... {percent} | Vel: {speed} | ETA: {eta}", end="", flush=True)
        except:
            pass
    elif d['status'] == 'finished':
        print(f"\n{Fore.GREEN}✅ Descarga completada. Finalizando...")

def obtener_calidades_video(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formatos = []
            visto = set()

            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':  # Video + audio
                    height = f.get('height') or 0
                    vcodec = f.get('vcodec', 'h264')
                    ext = f.get('ext', 'mp4')
                    filesize = f.get('filesize') or f.get('filesize_approx', 0)
                    size_mb = f"{filesize / (1024*1024):.1f} MB" if filesize else "?? MB"
                    
                    # Priorizar H.265 (mejor calidad) y altas resoluciones
                    label = f"{height}p {vcodec.upper()}" if height else f"{ext.upper()}"
                    key = (height, vcodec)
                    
                    if key not in visto:
                        visto.add(key)
                        formatos.append((f['format_id'], label, size_mb))
            
            # Ordenar por calidad: mayor resolución primero, luego H.265
            formatos.sort(key=lambda x: (int(x[1].split('p')[0]) if 'p' in x[1] else 0, 1 if 'HEVC' in x[1] else 0), reverse=True)
            return formatos[:15]  # Más opciones para TikTok
    except Exception as e:
        print(Fore.RED + f"\n❌ Error al obtener info: {e}")
        return []

def seleccionar_calidad(calidades):
    if not calidades:
        print(Fore.RED + "\n❌ No hay formatos de video disponibles. TikTok podría estar limitando.")
        print(Fore.YELLOW + "\n💡 Tip: Prueba con snaptik.app para HD original.")
        return None

    print(Fore.CYAN + f"\n📺 Calidades disponibles (ordenadas por mejor calidad):")
    for i, (fid, label, size) in enumerate(calidades, 1):
        print(Fore.GREEN + f"  {i} - {label.ljust(12)} | Tamaño: {size}")

    while True:
        mostrar_cursor()
        sel = input(Fore.CYAN + f"\n  -> Elige [1-{len(calidades)}] (1=mejor): " + Style.RESET_ALL).strip()
        ocultar_cursor()
        if sel.isdigit() and 1 <= int(sel) <= len(calidades):
            return calidades[int(sel)-1][0]
        print(Fore.RED + "Opción inválida. Intenta de nuevo.")

def descargar_video(url):
    ocultar_cursor()

    try:
        print(Fore.YELLOW + "\n🔍 Analizando video para HD máximo...")
        calidades = obtener_calidades_video(url)

        if not calidades:
            pausar()
            return

        # Verificar si hay baja calidad (menos de 1MB o <720p)
        mejor_size = float(calidades[0][2].replace(' MB', '').replace('??', '0'))
        if mejor_size < 1 or '540p' in calidades[0][1]:
            print(Fore.YELLOW + f"\n⚠️ Advertencia: Máx. calidad detectada es baja ({calidades[0][1]}).")
            print(Fore.CYAN + "Usa snaptik.app para HD original si quieres mejor.\n")

        formato_id = seleccionar_calidad(calidades)
        if not formato_id:
            pausar()
            return

        # Configuración optimizada para HD
        ydl_opts = {
            'format': f'{formato_id}+bestaudio/best',  # Video + mejor audio
            'outtmpl': os.path.join(ruta_videos, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'embed_subs': True,
            'embed_thumbnail': True,
            'add_metadata': True,
            'progress_hooks': [progreso_hook],
            'writesubtitles': True,  # Subtítulos si hay
        }

        print(Fore.YELLOW + f"\n🎬 Descargando en {calidades[0][1]} (mejor disponible)...")
        print(Fore.CYAN + "Progreso en vivo abajo:\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(Fore.GREEN + f"\n🎉 ¡Video listo en HD máximo posible!")
        print(Fore.WHITE + f"📁 Carpeta: {ruta_videos}")

    except Exception as e:
        print(Fore.RED + f"\n❌ Error en descarga: {e}")
        print(Fore.YELLOW + "\n💡 Prueba actualizando yt-dlp: pip install -U yt-dlp")
    finally:
        pausar()  # Siempre pausa como en los otros módulos
