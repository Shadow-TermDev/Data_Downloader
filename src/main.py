#!/usr/bin/env python3
"""
Data Downloader - Multimedia toolkit for Termux
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
Version: 1.8.1
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

# Utils (TokenHub/player-style UI + navigable TUI)
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import limpiar_pantalla, centrar_texto
from src.utils.boxes import print_box
from src.utils.tui import select_index

# Core modules
from src.core.menu import MenuHandler

# Init colorama
init(autoreset=True)

MAIN_OPTIONS = [
    "📥 Download content",
    "🔄 Convert files",
    "✨ Enhance file quality",
    "🔎 Search YouTube",
    "📖 Help",
    "🚪 Exit",
]


class DataDownloader:
    """Main app class"""

    def __init__(self):
        self.menu_handler = MenuHandler()

    def show_banner(self):
        """Show the main app banner (pyfiglet, no box)."""
        limpiar_pantalla()

        # Big title with pyfiglet
        titulo = pyfiglet.figlet_format("Downloader", font="slant")
        for linea in titulo.splitlines():
            print(Fore.YELLOW + centrar_texto(linea))

        print(Fore.CYAN + centrar_texto("MUSIC, VIDEO & IMAGE DOWNLOADER"))
        print(Fore.MAGENTA + centrar_texto(f"{VERSION}"))
        print()

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
        print()

    def run(self):
        """Main app loop (navigable TUI)."""
        ocultar_cursor()

        actions = [
            self.menu_handler.download_menu,
            self.menu_handler.converter_menu,
            self.menu_handler.enhancer_menu,
            self.menu_handler.search_menu,
            self.menu_handler.help_menu,
        ]

        try:
            while True:
                idx = select_index(
                    "What would you like to do?",
                    MAIN_OPTIONS,
                    header_fn=self._header,
                    hint="↑/↓ navigate • Enter select • 1-6 jump • q exit",
                )

                if idx is None or "Exit" in MAIN_OPTIONS[idx]:
                    self.farewell()
                    break

                try:
                    actions[idx]()
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

    def _header(self):
        """Repainted above the TUI list on every keypress (zoom-proof)."""
        self.show_banner()
        self.show_project_info()

    def farewell(self):
        """Show goodbye message"""
        print()
        print(Fore.RED + centrar_texto(MESSAGES["goodbye"]))
        print(Fore.CYAN + centrar_texto(f"{VERSION} - {AUTHOR}"))
        print(Fore.MAGENTA + centrar_texto(f"🌐 {WEBSITE}"))
        mostrar_cursor()

    # --- Backward-compat aliases (old API) ---
    mostrar_banner = show_banner
    mostrar_info_proyecto = show_project_info
    despedida = farewell
    ejecutar = run

    def show_main_menu(self):
        """Deprecated: main loop now uses navigable TUI."""
        idx = select_index("What would you like to do?", MAIN_OPTIONS,
                           header_fn=self._header)
        return str(idx + 1) if idx is not None else "6"

    mostrar_menu_principal = show_main_menu


def main():
    """App entry point"""
    app = DataDownloader()
    app.run()


if __name__ == "__main__":
    main()
