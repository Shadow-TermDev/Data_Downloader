"""
Menu and navigation handler (navigable arrow-key TUI)
Author: Shadow-TermDev
"""

from colorama import Fore, Style
from typing import Callable, Dict

from src.utils.helpers import limpiar_pantalla, centrar_texto
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.tui import select_index
from config.settings import MESSAGES


class MenuHandler:
    """Handles navigation between menus"""

    def __init__(self):
        self.menu_map: Dict[str, Callable] = {
            "1": self.download_menu,
            "2": self.converter_menu,
            "3": self.enhancer_menu,
            "4": self.search_menu,
            "5": self.help_menu,
        }

    def handle_option(self, opcion: str) -> bool:
        """
        Handle the selected main-menu option (numeric string, legacy API).

        Args:
            opcion: Selected option number

        Returns:
            True if the option was valid, False otherwise
        """
        if opcion in self.menu_map:
            self.menu_map[opcion]()
            return True
        return False

    def _get_url(self, tipo: str) -> str:
        """
        Get and validate a URL from the user

        Args:
            tipo: Content type ('video', 'audio', 'image')

        Returns:
            Valid URL or empty string
        """
        mensajes = {
            "video": "Enter the video URL",
            "audio": "Enter the audio URL",
            "image": "Enter the image URL",
        }

        iconos = {
            "video": "🎬",
            "audio": "🎵",
            "image": "🖼️",
        }

        print()
        print(Fore.CYAN + f"{iconos[tipo]} {mensajes[tipo]}: " + Style.RESET_ALL, end="")

        mostrar_cursor()
        try:
            url = input().strip()
        finally:
            ocultar_cursor()

        if not url:
            print(Fore.RED + f"❌ {MESSAGES['empty_input']}")
            return ""

        if not url.startswith(('http://', 'https://')):
            print(Fore.RED + "❌ URL must start with http:// or https://")
            return ""

        return url

    def _pick(self, titulo: str, subtitulo: str, opciones: list) -> int | None:
        """Render header + navigable list. Returns index or None (back/cancel)."""
        import pyfiglet

        limpiar_pantalla()
        figlet = pyfiglet.Figlet(font="slant")
        for linea in figlet.renderText(titulo).splitlines():
            print(Fore.YELLOW + centrar_texto(linea))
        print(Fore.CYAN + centrar_texto(f"{subtitulo}\n"))
        return select_index(subtitulo, opciones)

    def download_menu(self):
        """Content download menu"""
        from src.downloader.video import descargar_video
        from src.downloader.audio import descargar_audio
        from src.downloader.image import descargar_imagen

        opciones = [
            "Download video",
            "Download audio",
            "Download image",
            "Search YouTube & download",
            "Back to main menu",
        ]

        while True:
            idx = self._pick("Downloader", "DOWNLOAD MEDIA FILES", opciones)
            if idx is None or idx == 4:
                return

            if idx == 3:
                url = self._search_youtube_url()
                if not url:
                    continue
                # Ask video or audio after search
                tipo = self._ask_search_media_type()
                try:
                    if tipo == "audio":
                        descargar_audio(url)
                    else:
                        descargar_video(url)
                except Exception as e:
                    print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                continue

            funciones = {
                0: ("video", descargar_video),
                1: ("audio", descargar_audio),
                2: ("image", descargar_imagen),
            }

            tipo, funcion = funciones[idx]
            url = self._get_url(tipo)

            if not url:
                continue

            try:
                funcion(url)
            except Exception as e:
                print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)

    def converter_menu(self):
        """File conversion menu"""
        from src.converter.video import convertir_video
        from src.converter.video_to_audio import convertir_video_a_audio
        from src.converter.image import convertir_imagen
        from src.converter.audio import convertir_audio
        from src.core.file_manager import buscar_archivo

        opciones = [
            "Convert video",
            "Video → Audio",
            "Convert image",
            "Convert audio",
            "Back to main menu",
        ]

        while True:
            idx = self._pick("Converter", "VIDEO, AUDIO & IMAGE CONVERTER", opciones)
            if idx is None or idx == 4:
                return

            configs = {
                0: ("Enter video name: ", convertir_video, ["mp4", "mkv", "avi", "mov", "webm"]),
                1: ("Enter video name: ", convertir_video_a_audio, ["mp3", "wav", "ogg", "aac", "flac"]),
                2: ("Enter image name: ", convertir_imagen, ["png", "jpg", "jpeg", "webp", "bmp"]),
                3: ("Enter audio name: ", convertir_audio, ["mp3", "wav", "ogg", "aac", "flac"]),
            }

            mensaje, funcion, formatos = configs[idx]

            mostrar_cursor()
            print()
            try:
                nombre = input(Fore.YELLOW + mensaje).strip()
            finally:
                ocultar_cursor()

            if not nombre:
                print(Fore.RED + centrar_texto(MESSAGES["empty_input"]) + Style.RESET_ALL)
                continue

            ruta = buscar_archivo(nombre)
            if not ruta:
                # buscar_archivo already shows the error, just continue
                continue

            while True:
                mostrar_cursor()
                try:
                    fmt = input(Fore.CYAN + f"Output format ({', '.join(formatos)}): " + Style.RESET_ALL).strip().lower()
                finally:
                    ocultar_cursor()

                if fmt in formatos:
                    try:
                        funcion(ruta, fmt)
                    except Exception as e:
                        print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                        # No pause, functions already do it
                    break
                else:
                    print(Fore.RED + centrar_texto(f"Unsupported format. Options: {', '.join(formatos)}") + Style.RESET_ALL)

    def enhancer_menu(self):
        """Quality enhancement menu"""
        from src.enhancer.video import mejorar_calidad_video
        from src.enhancer.audio import mejorar_calidad_audio
        from src.enhancer.image import mejorar_calidad_imagen
        from src.core.file_manager import buscar_archivo

        opciones = [
            "Enhance video quality",
            "Enhance audio quality",
            "Enhance image quality",
            "Back to main menu",
        ]

        while True:
            idx = self._pick("Quality Boost", "IMPROVE IMAGE, VIDEO & AUDIO QUALITY", opciones)
            if idx is None or idx == 3:
                return

            mensajes = {
                0: "Enter video name: ",
                1: "Enter audio name: ",
                2: "Enter image name: ",
            }

            funciones = {
                0: mejorar_calidad_video,
                1: mejorar_calidad_audio,
                2: mejorar_calidad_imagen,
            }

            mostrar_cursor()
            print()
            try:
                nombre = input(Fore.YELLOW + mensajes[idx]).strip()
            finally:
                ocultar_cursor()

            if not nombre:
                print(Fore.RED + centrar_texto(MESSAGES["empty_input"]) + Style.RESET_ALL)
                input(Fore.YELLOW + centrar_texto(MESSAGES["press_enter"]))
                continue

            ruta = buscar_archivo(nombre)
            if not ruta:
                # buscar_archivo already shows message + pause
                continue

            try:
                funciones[idx](ruta)
            except Exception as e:
                print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                # No pause, functions already do it

    def search_menu(self):
        """Standalone YouTube search -> download"""
        from src.downloader.video import descargar_video
        from src.downloader.audio import descargar_audio

        opciones = [
            "Search & download video",
            "Search & download audio",
            "Back to main menu",
        ]

        while True:
            idx = self._pick("YT Search", "🔎 YOUTUBE SEARCH", opciones)
            if idx is None or idx == 2:
                return

            url = self._search_youtube_url()
            if not url:
                continue

            try:
                if idx == 1:
                    descargar_audio(url)
                else:
                    descargar_video(url)
            except Exception as e:
                print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)

    def _search_youtube_url(self) -> str:
        """Run the search and return a URL (or '')."""
        from src.searcher.youtube import search_and_pick
        from src.utils.helpers import pausar
        url = search_and_pick()
        if not url:
            print(Fore.YELLOW + centrar_texto("Search cancelled — no URL picked."))
            pausar(mostrar=False)
        return url

    def _ask_search_media_type(self) -> str:
        """Ask whether the searched URL is video or audio (navigable)."""
        idx = select_index(
            "Download as?",
            ["Video", "Audio"],
            hint="↑/↓ navigate • Enter select • q = video",
        )
        return "audio" if idx == 1 else "video"

    def help_menu(self):
        """Help menu"""
        from src.utils.helpers import mostrar_ayuda

        opciones = [
            "How to download content",
            "How to convert files",
            "How to enhance quality",
            "How to search YouTube",
            "Back to main menu",
        ]

        while True:
            idx = self._pick("Help", "📖 USER MANUAL 📖", opciones)
            if idx is None or idx == 4:
                return

            mostrar_ayuda(str(idx + 1))

    def _show_submenu(self, titulo: str, subtitulo: str, opciones: list, color_opciones=None):
        """Deprecated: submenus now use navigable _pick(). Kept for compat."""
        import pyfiglet

        limpiar_pantalla()
        figlet = pyfiglet.Figlet(font="slant")
        for linea in figlet.renderText(titulo).splitlines():
            print(Fore.YELLOW + centrar_texto(linea))
        print(Fore.CYAN + centrar_texto(f"{subtitulo}\n"))

    def _show_error(self):
        """Show invalid-option error"""
        print(Fore.RED + centrar_texto(MESSAGES["invalid_option"]) + Style.RESET_ALL)
        input(Fore.YELLOW + centrar_texto(MESSAGES["press_enter"]))

    # --- Backward-compat aliases (old Spanish API) ---
    manejar_opcion = handle_option
    menu_descargador = download_menu
    menu_convertidor = converter_menu
    menu_mejorador = enhancer_menu
    menu_ayuda = help_menu
