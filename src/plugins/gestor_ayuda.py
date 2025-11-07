import json
import os

# Ruta del archivo JSON
RUTA_AYUDA = os.path.join(os.path.dirname(__file__), "ayuda.json")

def cargar_ayuda():
    """Carga los datos de ayuda desde el archivo JSON."""
    try:
        with open(RUTA_AYUDA, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def obtener_ayuda(opcion):
    """Devuelve el título y mensaje de una opción de ayuda."""
    ayuda = cargar_ayuda()
    return ayuda.get(opcion, {"titulo": "Opción no encontrada", "mensaje": "La opción seleccionada no existe."})

