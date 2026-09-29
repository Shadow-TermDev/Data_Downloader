"""
Menu and navigation handler
Author: Shadow-TermDev
"""

from colorama import Fore, Style
from typing import Callable, Dict

from src.utils.helpers import limpiar_pantalla, centrar_texto
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.boxes import print_menu_box
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
        Handle the selected main-menu option

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

        url = input().strip()

        if not url:
            print(Fore.RED + f"❌ {MESSAGES['empty_input']}")
            return ""

        if not url.startswith(('http://', 'https://')):
            print(Fore.RED + "❌ URL must start with http:// or https://")
            return ""

        return url

    def download_menu(self):
        """Content download menu"""
        from src.downloader.video import descargar_video
        from src.downloader.audio import descargar_audio
        from src.downloader.image import descargar_imagen

        while True:
            self._show_submenu(
                titulo="Downloader",
                subtitulo="DOWNLOAD MEDIA FILES",
                opciones=[
                    "1 - Download video",
                    "2 - Download audio",
                    "3 - Download image",
                    "4 - Search YouTube & download",
                    "5 - Back to main menu",
                ]
            )

            opcion = input().strip()
            ocultar_cursor()

            if opcion == "5":
                return

            if opcion not in ["1", "2", "3", "4"]:
                self._show_error()
                continue

            if opcion == "4":
                url = self._search_youtube_url()
                if not url:
                    continue
                # Ask video or audio after search
                tipo = self._ask_search_media_type()
                if tipo == "audio":
                    try:
                        descargar_audio(url)
                    except Exception as e:
                        print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                else:
                    try:
                        descargar_video(url)
                    except Exception as e:
                        print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                continue

            funciones = {
                "1": ("video", descargar_video),
                "2": ("audio", descargar_audio),
                "3": ("image", descargar_imagen),
            }

            tipo, funcion = funciones[opcion]
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

        while True:
            self._show_submenu(
                titulo="Converter",
                subtitulo="VIDEO, AUDIO & IMAGE CONVERTER",
                opciones=[
                    "1 - Convert video",
                    "2 - Video → Audio",
                    "3 - Convert image",
                    "4 - Convert audio",
                    "5 - Back to main menu",
                ]
            )

            opcion = input().strip()
            ocultar_cursor()

            if opcion == "5":
                return

            if opcion not in ["1", "2", "3", "4"]:
                self._show_error()
                continue

            configs = {
                "1": ("Enter video name: ", convertir_video, ["mp4", "mkv", "avi", "mov", "webm"]),
                "2": ("Enter video name: ", convertir_video_a_audio, ["mp3", "wav", "ogg", "aac", "flac"]),
                "3": ("Enter image name: ", convertir_imagen, ["png", "jpg", "jpeg", "webp", "bmp"]),
                "4": ("Enter audio name: ", convertir_audio, ["mp3", "wav", "ogg", "aac", "flac"]),
            }

            mensaje, funcion, formatos = configs[opcion]

            mostrar_cursor()
            print()
            nombre = input(Fore.YELLOW + mensaje).strip()
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
                fmt = input(Fore.CYAN + f"Output format ({', '.join(formatos)}): " + Style.RESET_ALL).strip().lower()
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

        while True:
            self._show_submenu(
                titulo="Quality Boost",
                subtitulo="IMPROVE IMAGE, VIDEO & AUDIO QUALITY",
                opciones=[
                    "1 - Enhance video quality",
                    "2 - Enhance audio quality",
                    "3 - Enhance image quality",
                    "4 - Back to main menu",
                ]
            )

            opcion = input().strip()
            ocultar_cursor()

            if opcion == "4":
                return

            if opcion not in ["1", "2", "3"]:
                self._show_error()
                continue

            mensajes = {
                "1": "Enter video name: ",
                "2": "Enter audio name: ",
                "3": "Enter image name: ",
            }

            funciones = {
                "1": mejorar_calidad_video,
                "2": mejorar_calidad_audio,
                "3": mejorar_calidad_imagen,
            }

            mostrar_cursor()
            print()
            nombre = input(Fore.YELLOW + mensajes[opcion]).strip()
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
                funciones[opcion](ruta)
            except Exception as e:
                print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                # No pause, functions already do it

    def search_menu(self):
        """Standalone YouTube search (prototype) -> download"""
        from src.downloader.video import descargar_video
        from src.downloader.audio import descargar_audio

        while True:
            self._show_submenu(
                titulo="YT Search",
                subtitulo="🔎 YOUTUBE SEARCH (PROTOTYPE)",
                opciones=[
                    "1 - Search & download video",
                    "2 - Search & download audio",
                    "3 - Back to main menu",
                ]
            )

            opcion = input().strip()
            ocultar_cursor()

            if opcion == "3":
                return

            if opcion not in ["1", "2"]:
                self._show_error()
                continue

            url = self._search_youtube_url()
            if not url:
                continue

            try:
                if opcion == "2":
                    descargar_audio(url)
                else:
                    descargar_video(url)
            except Exception as e:
                print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)

    def _search_youtube_url(self) -> str:
        """Run the search prototype and return a URL (or '')."""
        from src.searcher.youtube import search_and_pick
        from src.utils.helpers import pausar
        url = search_and_pick()
        if not url:
            print(Fore.YELLOW + centrar_texto("Search cancelled — no URL picked."))
            pausar(mostrar=False)
        return url

    def _ask_search_media_type(self) -> str:
        """Ask whether the searched URL is video or audio."""
        mostrar_cursor()
        print()
        sel = input(Fore.YELLOW + "Download as video or audio? [V/a]: " + Style.RESET_ALL).strip().lower()
        ocultar_cursor()
        return "audio" if sel in ("a", "audio") else "video"

    def help_menu(self):
        """Help menu"""
        from src.utils.helpers import mostrar_ayuda

        while True:
            self._show_submenu(
                titulo="Help",
                subtitulo="📖 USER MANUAL 📖",
                opciones=[
                    "1 - How to download content",
                    "2 - How to convert files",
                    "3 - How to enhance quality",
                    "4 - Back to main menu",
                ],
                color_opciones=Fore.GREEN
            )

            opcion = input().strip()
            ocultar_cursor()

            if opcion == "4":
                return

            if opcion in ["1", "2", "3"]:
                mostrar_ayuda(opcion)
            else:
                self._show_error()

    def _show_submenu(self, titulo: str, subtitulo: str, opciones: list, color_opciones=None):
        """
        Show a generic submenu (TokenHub-style clear + player-style prompt)

        Args:
            titulo: Main menu title
            subtitulo: Descriptive subtitle
            opciones: Menu option list
            color_opciones: Default color for options
        """
        limpiar_pantalla()

        from src.utils.ui import print_header
        from config.settings import VERSION
        print_header("Data Downloader", VERSION)

        import pyfiglet
        figlet = pyfiglet.Figlet(font="slant")
        titulo_ascii = figlet.renderText(titulo)

        for linea in titulo_ascii.splitlines():
            print(Fore.YELLOW + centrar_texto(linea))
        print(Fore.CYAN + centrar_texto(f"{subtitulo}\n"))

        colores = []
        for i, texto in enumerate(opciones):
            # Last option always red
            if i == len(opciones) - 1:
                colores.append(Fore.RED)
            elif color_opciones:
                colores.append(color_opciones)
            else:
                colores.append(Fore.GREEN)

        print_menu_box(opciones, colores)
        print()

        mostrar_cursor()
        print(Fore.CYAN + "  -> Enter option number: ", end="")

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
