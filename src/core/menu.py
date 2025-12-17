"""
Manejador de menús y navegación
Autor: Shadow-TermDev
"""

from colorama import Fore, Style
from typing import Callable, Dict

from src.utils.helpers import limpiar_pantalla, centrar_texto
from src.utils.animations import ocultar_cursor, mostrar_cursor
from config.settings import BOX_WIDTH, MESSAGES


class MenuHandler:
    """Maneja la navegación entre diferentes menús"""
    
    def __init__(self):
        self.menu_map: Dict[str, Callable] = {
            "1": self.menu_descargador,
            "2": self.menu_convertidor,
            "3": self.menu_mejorador,
            "4": self.menu_ayuda
        }
    
    def manejar_opcion(self, opcion: str) -> bool:
        """
        Maneja la opción seleccionada del menú principal
        
        Args:
            opcion: Número de opción seleccionada
            
        Returns:
            True si la opción fue válida, False en caso contrario
        """
        if opcion in self.menu_map:
            self.menu_map[opcion]()
            return True
        return False
    
    def menu_descargador(self):
        """Menú de descarga de contenido"""
        from src.downloader.video import descargar_video
        from src.downloader.audio import descargar_audio
        from src.downloader.image import descargar_imagen
        
        while True:
            self._mostrar_submenu(
                titulo="Downloader",
                subtitulo="DESCARGA ARCHIVOS MULTIMEDIA",
                opciones=[
                    "1 - Descargar video",
                    "2 - Descargar audio",
                    "3 - Descargar imagen",
                    "4 - Volver al menú principal"
                ]
            )
            
            opcion = input().strip()
            ocultar_cursor()
            
            if opcion == "4":
                return
            
            if opcion not in ["1", "2", "3"]:
                self._mostrar_error()
                continue
            
            funciones = {
                "1": descargar_video,
                "2": descargar_audio,
                "3": descargar_imagen
            }
            
            mensajes = {
                "1": "Ingresa la URL del video: ",
                "2": "Ingresa la URL del audio: ",
                "3": "Ingresa la URL de la imagen: "
            }
            
            mostrar_cursor()
            print()
            url = input(Fore.YELLOW + mensajes[opcion]).strip()
            ocultar_cursor()
            
            if not url:
                print(Fore.RED + centrar_texto(MESSAGES["empty_input"]) + Style.RESET_ALL)
                input(Fore.YELLOW + centrar_texto(MESSAGES["press_enter"]))
                continue
            
            # Las funciones ya tienen su propio pausar(), no agregamos otro
            try:
                funciones[opcion](url)
            except Exception as e:
                print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                # No pausar aquí porque las funciones ya lo hacen
    
    def menu_convertidor(self):
        """Menú de conversión de archivos"""
        from src.converter.video import convertir_video
        from src.converter.video_to_audio import convertir_video_a_audio
        from src.converter.image import convertir_imagen
        from src.converter.audio import convertir_audio
        from src.core.file_manager import buscar_archivo
        
        while True:
            self._mostrar_submenu(
                titulo="Converter",
                subtitulo="VIDEO, AUDIO & IMAGE CONVERTER",
                opciones=[
                    "1 - Convertir video",
                    "2 - Video → Audio",
                    "3 - Convertir imagen",
                    "4 - Convertir audio",
                    "5 - Volver al menú principal"
                ]
            )
            
            opcion = input().strip()
            ocultar_cursor()
            
            if opcion == "5":
                return
            
            if opcion not in ["1", "2", "3", "4"]:
                self._mostrar_error()
                continue
            
            configs = {
                "1": ("Ingresa el nombre del video: ", convertir_video, ["mp4", "mkv", "avi", "mov", "webm"]),
                "2": ("Ingresa el nombre del video: ", convertir_video_a_audio, ["mp3", "wav", "ogg", "aac", "flac"]),
                "3": ("Ingresa el nombre de la imagen: ", convertir_imagen, ["png", "jpg", "jpeg", "webp", "bmp"]),
                "4": ("Ingresa el nombre del audio: ", convertir_audio, ["mp3", "wav", "ogg", "aac", "flac"])
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
                # buscar_archivo ya muestra error, solo continuamos
                continue
            
            while True:
                mostrar_cursor()
                fmt = input(Fore.CYAN + f"Formato de salida ({', '.join(formatos)}): " + Style.RESET_ALL).strip().lower()
                ocultar_cursor()
                
                if fmt in formatos:
                    try:
                        funcion(ruta, fmt)
                    except Exception as e:
                        print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                        # No pausar, las funciones ya lo hacen
                    break
                else:
                    print(Fore.RED + centrar_texto(f"Formato no soportado. Opciones: {', '.join(formatos)}") + Style.RESET_ALL)
    
    def menu_mejorador(self):
        """Menú de mejora de calidad"""
        from src.enhancer.video import mejorar_calidad_video
        from src.enhancer.audio import mejorar_calidad_audio
        from src.enhancer.image import mejorar_calidad_imagen
        from src.core.file_manager import buscar_archivo
        
        while True:
            self._mostrar_submenu(
                titulo="Quality Boost",
                subtitulo="IMPROVE IMAGE, VIDEO & AUDIO QUALITY",
                opciones=[
                    "1 - Mejorar calidad de video",
                    "2 - Mejorar calidad de audio",
                    "3 - Mejorar calidad de imagen",
                    "4 - Volver al menú principal"
                ]
            )
            
            opcion = input().strip()
            ocultar_cursor()
            
            if opcion == "4":
                return
            
            if opcion not in ["1", "2", "3"]:
                self._mostrar_error()
                continue
            
            mensajes = {
                "1": "Ingresa el nombre del video: ",
                "2": "Ingresa el nombre del audio: ",
                "3": "Ingresa el nombre de la imagen: "
            }
            
            funciones = {
                "1": mejorar_calidad_video,
                "2": mejorar_calidad_audio,
                "3": mejorar_calidad_imagen
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
                # buscar_archivo ya muestra mensaje y pausa
                continue
            
            try:
                funciones[opcion](ruta)
            except Exception as e:
                print(Fore.RED + centrar_texto(f"{MESSAGES['error_occurred']}: {e}") + Style.RESET_ALL)
                # No pausar, las funciones ya lo hacen
    
    def menu_ayuda(self):
        """Menú de ayuda"""
        from src.utils.helpers import mostrar_ayuda
        
        while True:
            self._mostrar_submenu(
                titulo="Ayuda",
                subtitulo="📖 MANUAL DE USUARIO 📖",
                opciones=[
                    "1 - Cómo descargar contenido",
                    "2 - Cómo convertir archivos",
                    "3 - Cómo mejorar calidad",
                    "4 - Volver al menú principal"
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
                self._mostrar_error()
    
    def _mostrar_submenu(self, titulo: str, subtitulo: str, opciones: list, color_opciones=None):
        """
        Muestra un submenú genérico
        
        Args:
            titulo: Título principal del menú
            subtitulo: Subtítulo descriptivo
            opciones: Lista de opciones del menú
            color_opciones: Color por defecto para las opciones
        """
        limpiar_pantalla()
        
        import pyfiglet
        figlet = pyfiglet.Figlet(font="slant")
        titulo_ascii = figlet.renderText(titulo)
        
        for linea in titulo_ascii.splitlines():
            print(Fore.YELLOW + centrar_texto(linea))
        print(Fore.CYAN + centrar_texto(f"{subtitulo}\n"))
        
        borde = "─" * (BOX_WIDTH - 2)
        print(Fore.MAGENTA + "╭" + borde + "╮")
        
        for i, texto in enumerate(opciones):
            # Última opción siempre en rojo
            if i == len(opciones) - 1:
                color = Fore.RED
            elif color_opciones:
                color = color_opciones
            else:
                color = Fore.GREEN
            
            print(Fore.MAGENTA + "│ " + color + texto.ljust(BOX_WIDTH - 4) + Fore.MAGENTA + " │")
        
        print(Fore.MAGENTA + "╰" + borde + "╯\n")
        
        mostrar_cursor()
        print(Fore.CYAN + "  -> Ingresa el número de la opción: ", end="")
    
    def _mostrar_error(self):
        """Muestra mensaje de error para opción inválida"""
        print(Fore.RED + centrar_texto(MESSAGES["invalid_option"]) + Style.RESET_ALL)
        input(Fore.YELLOW + centrar_texto(MESSAGES["press_enter"]))
