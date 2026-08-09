#!/usr/bin/env python3
"""
Data Downloader - Herramienta multimedia para Termux
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
Versión: 1.6.0
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from colorama import init, Fore, Style
import pyfiglet

# Importar configuración
from config.settings import (
    PROJECT_NAME, VERSION, AUTHOR, AUTHOR_TITLE,
    WEBSITE, REPOSITORY, MESSAGES
)

# Importar utilidades
from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.helpers import limpiar_pantalla, centrar_texto
from src.utils.boxes import print_box, print_menu_box

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
        lineas = [
            "",
            "Creador:",
            f"   {AUTHOR}  ·  {AUTHOR_TITLE}",
            "",
            "Sitio Web:",
            f"   {WEBSITE}",
            "",
            "Repositorio:",
            f"   {REPOSITORY}",
            "",
            "Versión:",
            f"   {VERSION}",
        ]
        colores = [Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.MAGENTA,
                   Fore.CYAN, Fore.WHITE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
                   Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

        print_box(titulo=f" {PROJECT_NAME} ", lineas=lineas, borde=Fore.MAGENTA,
                  color_titulo=Fore.YELLOW, colores=colores)

    def mostrar_menu_principal(self):
        """Muestra el menú principal con opciones"""
        opciones = [
            "1 - Descargar contenido",
            "2 - Convertir archivos",
            "3 - Mejorar calidad de archivos",
            "4 - Ayuda",
            "5 - Salir",
        ]
        colores = [Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.YELLOW, Fore.RED]

        print_menu_box(opciones, colores)
        print()

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
                
                try:
                    # Delegar al manejador de menús
                    if not self.menu_handler.manejar_opcion(opcion):
                        from src.utils.helpers import pausar
                        print(Fore.RED + centrar_texto(MESSAGES["invalid_option"]) + Style.RESET_ALL)
                        pausar(mostrar=False)
                except Exception as e:
                    # Los errores de una opción no deben cerrar la app
                    from src.utils.helpers import pausar
                    print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                    pausar(mostrar=False)
        
        except KeyboardInterrupt:
            print("\n")
            self.despedida()
        
        finally:
            mostrar_cursor()


def main():
    """Punto de entrada de la aplicación"""
    app = DataDownloader()
    app.ejecutar()


if __name__ == "__main__":
    main()
