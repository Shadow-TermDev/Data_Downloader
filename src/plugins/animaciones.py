import time
import sys
import json
import os
import shutil

# Se define la ruta del archivo de configuraci贸n correctamente
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

# --- Manejo del cursor ---
def ocultar_cursor():
    """Oculta el cursor para mejorar la est茅tica."""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def mostrar_cursor():
    """Vuelve a mostrar el cursor."""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

# --- Manejo de configuraci贸n ---
def cargar_config():
    """Carga la configuraci贸n actual desde config.json de forma segura."""
    if not os.path.exists(CONFIG_PATH):
        return {"transicion": "Fade"}  # Valor predeterminado
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("\033[91m鈿狅笍 Error al leer config.json, usando valores predeterminados.\033[0m")
        return {"transicion": "Fade"}

def obtener_transicion():
    """Obtiene la transici贸n seleccionada por el usuario."""
    return cargar_config().get("transicion", "Fade")

def cambiar_transicion(nueva_transicion):
    """Cambia la transici贸n y la guarda en config.json."""
    config = cargar_config()
    config["transicion"] = nueva_transicion
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except IOError:
        print("\033[91m鉂� No se pudo guardar la configuraci贸n.\033[0m")

# --- Definici贸n de transiciones ---
def transicion_fade(texto, color_final="\033[37m", velocidad=0.05):
    """Aparece el texto gradualmente con efecto de fade-in."""
    ocultar_cursor()
    for intensidad in range(30, 38):  # Colores del gris al blanco
        sys.stdout.write(f"\r\033[{intensidad}m{texto}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    print("")
    mostrar_cursor()

def transicion_slide(texto, color_final="\033[37m", velocidad=0.02):
    """Texto aparece desliz谩ndose desde la derecha."""
    ocultar_cursor()
    ancho = shutil.get_terminal_size(fallback=(80, 24)).columns
    for i in range(len(texto) + 1):
        sys.stdout.write(f"\r{color_final}{' ' * max(0, ancho - i)}{texto[:i]}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    print("")
    mostrar_cursor()

def transicion_zoom(texto, color_final="\033[37m", velocidad=0.05):
    """Texto aparece simulando un efecto de zoom-in."""
    ocultar_cursor()
    for escala in range(1, 4):  # Simula zoom con 3 niveles
        sys.stdout.write(f"\r\033[{escala}m{color_final}{texto}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    print("")
    mostrar_cursor()

def transicion_wipe(texto, color_final="\033[37m", velocidad=0.02):
    """Texto aparece como si fuera revelado por una cortina."""
    ocultar_cursor()
    texto_mostrado = ""
    for letra in texto:
        texto_mostrado += letra
        sys.stdout.write(f"\r{color_final}{texto_mostrado}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    print("")
    mostrar_cursor()

def transicion_flash(texto, color_final="\033[37m", velocidad=0.1):
    """Texto parpadea antes de mostrarse completamente."""
    ocultar_cursor()
    for _ in range(3):  # Parpadeo 3 veces
        sys.stdout.write(f"\r\033[5m{color_final}{texto}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
        sys.stdout.write(f"\r{' ' * len(texto)}")
        sys.stdout.flush()
        time.sleep(velocidad)
    print(f"{color_final}{texto}\033[0m")
    mostrar_cursor()

def aplicar_transicion(texto, color_final="\033[37m"):
    """Aplica la transici贸n seleccionada en la configuraci贸n."""
    transicion_actual = obtener_transicion()
    transiciones = {
        "Fade": transicion_fade,
        "Slide": transicion_slide,
        "Zoom": transicion_zoom,
        "Wipe": transicion_wipe,
        "Flash": transicion_flash,
    }
    transiciones.get(transicion_actual, lambda t, c: print(c + t))(texto, color_final)

