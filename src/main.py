#!/usr/bin/env python3
"""
Data Downloader - Herramienta multimedia para Termux
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
Versión: 1.4.2
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from colorama import init, Fore, Style
import pyfiglet

# Importar configuración
from config.settings import (
    PROJECT_NAME, VERSION, AUTHOR, AUTHOR_TITLE,
    WEBSITE, REPOSITORY, BOX_WIDTH, MESSAGES
)

# Importar utilidades
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import limpiar_pantalla, centrar_texto

# Importar módulos principales
from src.core.menu import MenuHandler

# Inicializar colorama
init(autoreset=True)


class DataDownloader:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        self.menu_handler = MenuHandler()
        
    def mostrar_banner(self):
        """Muestra el banner principal de la aplicación"""
        limpiar_pantalla()
        
        # Título grande con pyfiglet
        titulo = pyfiglet.figlet_format("Downloader", font="slant")
        for linea in titulo.splitlines():
            print(Fore.YELLOW + centrar_texto(linea))
        
        print(Fore.CYAN + centrar_texto("MUSIC, VIDEO & IMAGE DOWNLOADER\n"))
    
    def mostrar_info_proyecto(self):
        """Muestra información del proyecto en un cuadro"""
        borde = "─" * (BOX_WIDTH - 2)
        linea_vacia = Fore.MAGENTA + "│" + " " * (BOX_WIDTH - 2) + "│"
        
        print(Fore.MAGENTA + "╭" + borde + "╮")
        print(Fore.MAGENTA + "│" + Fore.YELLOW + f" {PROJECT_NAME} ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(linea_vacia)
        print(Fore.MAGENTA + "│" + Fore.CYAN + " Creador: ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "│" + Fore.WHITE + f" {AUTHOR} ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "│" + Fore.CYAN + f" {AUTHOR_TITLE} ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(linea_vacia)
        print(Fore.MAGENTA + "│" + Fore.CYAN + " Sitio Web: ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "│" + Fore.WHITE + f" {WEBSITE} ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(linea_vacia)
        print(Fore.MAGENTA + "│" + Fore.CYAN + " Repositorio: ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "│" + Fore.WHITE + f" {REPOSITORY} ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(linea_vacia)
        print(Fore.MAGENTA + "│" + Fore.CYAN + " Versión: ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "│" + Fore.WHITE + f" {VERSION} ".center(BOX_WIDTH - 2) + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "╰" + borde + "╯\n")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal con opciones"""
        opciones = [
            (Fore.GREEN,  "1 - Descargar contenido"),
            (Fore.BLUE,   "2 - Convertir archivos"),
            (Fore.CYAN,   "3 - Mejorar calidad de archivos"),
            (Fore.YELLOW, "4 - Ayuda"),
            (Fore.RED,    "5 - Salir"),
        ]
        
        borde = "─" * (BOX_WIDTH - 2)
        
        print(Fore.MAGENTA + "╭" + borde + "╮")
        for color, texto in opciones:
            print(Fore.MAGENTA + "│ " + color + texto.ljust(BOX_WIDTH - 4) + Fore.MAGENTA + " │")
        print(Fore.MAGENTA + "╰" + borde + "╯\n")
        
        mostrar_cursor()
        print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")
    
    def despedida(self):
        """Muestra mensaje de despedida"""
        print()
        print(Fore.RED + centrar_texto(MESSAGES["goodbye"]))
        print(Fore.CYAN + centrar_texto(f"{VERSION} - {AUTHOR}"))
        print(Fore.MAGENTA + centrar_texto(f"🌐 {WEBSITE}"))
        mostrar_cursor()
    
    def ejecutar(self):
        """Bucle principal de la aplicación"""
        ocultar_cursor()
        
        try:
            while True:
                self.mostrar_banner()
                self.mostrar_info_proyecto()
                self.mostrar_menu_principal()
                
                opcion = input().strip()
                ocultar_cursor()
                
                if opcion == "5":
                    self.despedida()
                    break
                
                # Delegar al manejador de menús
                if not self.menu_handler.manejar_opcion(opcion):
                    print(Fore.RED + centrar_texto(MESSAGES["invalid_option"]) + Style.RESET_ALL)
                    input(Fore.YELLOW + centrar_texto(MESSAGES["press_enter"]))
        
        except KeyboardInterrupt:
            print("\n")
            self.despedida()
        
        except Exception as e:
            print(Fore.RED + f"\n{MESSAGES['error_occurred']}: {e}")
            mostrar_cursor()
        
        finally:
            mostrar_cursor()


def main():
    """Punto de entrada de la aplicación"""
    app = DataDownloader()
    app.ejecutar()


if __name__ == "__main__":
    main()
