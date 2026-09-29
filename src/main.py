#!/usr/bin/env python3
"""
Data Downloader - Multimedia toolkit for Termux
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
Version: 1.7.0
"""

import sys
from pathlib import Path

# Add repo root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from colorama import init, Fore, Style
import pyfiglet

# Config
from config.settings import (
    PROJECT_NAME, VERSION, AUTHOR, AUTHOR_TITLE,
    WEBSITE, REPOSITORY, MESSAGES
)

# Utils (TokenHub/player-style UI)
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import limpiar_pantalla, centrar_texto
from src.utils.boxes import print_box, print_menu_box
from src.utils.ui import print_header

# Core modules
from src.core.menu import MenuHandler

# Init colorama
init(autoreset=True)


class DataDownloader:
    """Main app class"""

    def __init__(self):
        self.menu_handler = MenuHandler()

    def show_banner(self):
        """Show the main app banner (player-style header + pyfiglet)"""
        limpiar_pantalla()
        print_header(PROJECT_NAME, VERSION)

        # Big title with pyfiglet
        titulo = pyfiglet.figlet_format("Downloader", font="slant")
        for linea in titulo.splitlines():
            print(Fore.YELLOW + centrar_texto(linea))

        print(Fore.CYAN + centrar_texto("MUSIC, VIDEO & IMAGE DOWNLOADER\n"))

    def show_project_info(self):
        """Show project info in a box"""
        lineas = [
            "",
            "Creator:",
            f"   {AUTHOR}  ·  {AUTHOR_TITLE}",
            "",
            "Website:",
            f"   {WEBSITE}",
            "",
            "Repository:",
            f"   {REPOSITORY}",
            "",
            "Version:",
            f"   {VERSION}",
        ]
        colores = [Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.MAGENTA,
                   Fore.CYAN, Fore.WHITE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
                   Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

        print_box(titulo=f" {PROJECT_NAME} ", lineas=lineas, borde=Fore.MAGENTA,
                  color_titulo=Fore.YELLOW, colores=colores)

    def show_main_menu(self):
        """Show the main menu options"""
        opciones = [
            "1 - Download content",
            "2 - Convert files",
            "3 - Enhance file quality",
            "4 - Search YouTube",
            "5 - Help",
            "6 - Exit",
        ]
        colores = [Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.RED]

        print_menu_box(opciones, colores)
        print()

        mostrar_cursor()
        print(Fore.CYAN + "  -> Enter option number: ", end="")

    def farewell(self):
        """Show goodbye message"""
        print()
        print(Fore.RED + centrar_texto(MESSAGES["goodbye"]))
        print(Fore.CYAN + centrar_texto(f"{VERSION} - {AUTHOR}"))
        print(Fore.MAGENTA + centrar_texto(f"🌐 {WEBSITE}"))
        mostrar_cursor()

    def run(self):
        """Main app loop"""
        ocultar_cursor()

        try:
            while True:
                self.show_banner()
                self.show_project_info()
                self.show_main_menu()

                opcion = input().strip()
                ocultar_cursor()

                if opcion == "6":
                    self.farewell()
                    break

                try:
                    # Delegate to the menu handler
                    if not self.menu_handler.handle_option(opcion):
                        from src.utils.helpers import pausar
                        print(Fore.RED + centrar_texto(MESSAGES["invalid_option"]) + Style.RESET_ALL)
                        pausar(mostrar=False)
                except Exception as e:
                    # Errors in one option must not kill the app
                    from src.utils.helpers import pausar
                    print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                    pausar(mostrar=False)

        except KeyboardInterrupt:
            print("\n")
            self.farewell()

        finally:
            mostrar_cursor()

    # --- Backward-compat aliases (old Spanish API) ---
    mostrar_banner = show_banner
    mostrar_info_proyecto = show_project_info
    mostrar_menu_principal = show_main_menu
    despedida = farewell
    ejecutar = run


def main():
    """App entry point"""
    app = DataDownloader()
    app.run()


if __name__ == "__main__":
    main()
