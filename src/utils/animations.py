"""
Animation and visual effects system
Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import sys
import time
import json

from config.settings import ASSETS_DIR, DEFAULT_TRANSITION, ANIMATION_SPEED


# Config file path
CONFIG_PATH = ASSETS_DIR / "config.json"


# ============================================================
# CURSOR HANDLING
# ============================================================

def ocultar_cursor():
    """Hide the cursor for cleaner visuals"""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def mostrar_cursor():
    """Show the cursor again"""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


# ============================================================
# CONFIG HANDLING
# ============================================================

def cargar_config() -> dict:
    """
    Load current settings from config.json (supports legacy Spanish keys)
    
    Returns:
        Config dict
    """
    # Create file if missing
    if not CONFIG_PATH.exists():
        config_inicial = {
            "transition": DEFAULT_TRANSITION,
            "animation_speed": ANIMATION_SPEED,
            "theme": "default"
        }
        guardar_config(config_inicial)
        return config_inicial
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Migrate legacy Spanish keys
            if "transicion" in data and "transition" not in data:
                data["transition"] = data.pop("transicion")
            if "velocidad_animacion" in data and "animation_speed" not in data:
                data["animation_speed"] = data.pop("velocidad_animacion")
            if "tema" in data and "theme" not in data:
                data["theme"] = data.pop("tema")
            return data
    except (json.JSONDecodeError, IOError):
        print("\033[91m⚠️ Error reading config.json, using defaults.\033[0m")
        return {"transition": DEFAULT_TRANSITION}


def guardar_config(config: dict) -> bool:
    """
    Save settings to config.json
    
    Args:
        config: Config dict
        
    Returns:
        True if saved successfully
    """
    try:
        # Ensure directory exists
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        print("\033[91m⚠️ Could not save settings.\033[0m")
        return False


def obtener_transicion() -> str:
    """
    Get the user-selected transition
    
    Returns:
        Transition name
    """
    cfg = cargar_config()
    return cfg.get("transition", cfg.get("transicion", DEFAULT_TRANSITION))


def cambiar_transicion(nueva_transicion: str):
    """
    Change and save the transition
    
    Args:
        nueva_transicion: New transition name
    """
    config = cargar_config()
    config["transition"] = nueva_transicion
    config.pop("transicion", None)
    guardar_config(config)


# ============================================================
# TRANSICIONES Y EFECTOS
# ============================================================

def transicion_fade(texto: str, color_final: str = "\033[37m", velocidad: float = 0.05):
    """
    Efecto de aparición gradual (fade-in)
    
    Args:
        texto: Texto a mostrar
        color_final: Color ANSI del texto
        velocidad: Velocidad de la animación
    """
    ocultar_cursor()
    
    # Gradiente de grises a color final
    for intensidad in range(30, 38):
        sys.stdout.write(f"\r\033[{intensidad}m{texto}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    
    # Color final
    sys.stdout.write(f"\r{color_final}{texto}\033[0m\n")
    sys.stdout.flush()
    
    mostrar_cursor()


def transicion_slide(texto: str, color_final: str = "\033[37m", velocidad: float = 0.02):
    """
    Efecto de deslizamiento desde la derecha
    
    Args:
        texto: Texto a mostrar
        color_final: Color ANSI del texto
        velocidad: Velocidad de la animación
    """
    ocultar_cursor()
    
    try:
        import shutil
        ancho = shutil.get_terminal_size(fallback=(80, 24)).columns
    except Exception:
        ancho = 80
    
    for i in range(len(texto) + 1):
        espacios = " " * max(0, ancho - i)
        sys.stdout.write(f"\r{color_final}{espacios}{texto[:i]}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    
    print()
    mostrar_cursor()


def transicion_zoom(texto: str, color_final: str = "\033[37m", velocidad: float = 0.05):
    """
    Efecto de zoom-in simulado
    
    Args:
        texto: Texto a mostrar
        color_final: Color ANSI del texto
        velocidad: Velocidad de la animación
    """
    ocultar_cursor()
    
    # Simular zoom con 3 niveles
    for escala in range(1, 4):
        sys.stdout.write(f"\r\033[{escala}m{color_final}{texto}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    
    print()
    mostrar_cursor()


def transicion_wipe(texto: str, color_final: str = "\033[37m", velocidad: float = 0.02):
    """
    Efecto de revelado como cortina
    
    Args:
        texto: Texto a mostrar
        color_final: Color ANSI del texto
        velocidad: Velocidad de la animación
    """
    ocultar_cursor()
    
    texto_mostrado = ""
    for letra in texto:
        texto_mostrado += letra
        sys.stdout.write(f"\r{color_final}{texto_mostrado}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
    
    print()
    mostrar_cursor()


def transicion_flash(texto: str, color_final: str = "\033[37m", velocidad: float = 0.1):
    """
    Efecto de parpadeo antes de mostrar
    
    Args:
        texto: Texto a mostrar
        color_final: Color ANSI del texto
        velocidad: Velocidad de la animación
    """
    ocultar_cursor()
    
    # Parpadear 3 veces
    for _ in range(3):
        sys.stdout.write(f"\r\033[5m{color_final}{texto}\033[0m")
        sys.stdout.flush()
        time.sleep(velocidad)
        
        sys.stdout.write(f"\r{' ' * len(texto)}")
        sys.stdout.flush()
        time.sleep(velocidad)
    
    # Mostrar final
    print(f"{color_final}{texto}\033[0m")
    mostrar_cursor()


def aplicar_transicion(texto: str, color_final: str = "\033[37m"):
    """
    Aplica la transición configurada
    
    Args:
        texto: Texto a mostrar
        color_final: Color ANSI del texto
    """
    transicion_actual = obtener_transicion()
    
    transiciones = {
        "Fade": transicion_fade,
        "Slide": transicion_slide,
        "Zoom": transicion_zoom,
        "Wipe": transicion_wipe,
        "Flash": transicion_flash,
    }
    
    # Obtener función de transición o usar print simple
    funcion_transicion = transiciones.get(transicion_actual)
    
    if funcion_transicion:
        funcion_transicion(texto, color_final)
    else:
        # Fallback: mostrar sin animación
        print(color_final + texto + "\033[0m")


# ============================================================
# EFECTOS ADICIONALES
# ============================================================

def barra_cargando(duracion: float = 2.0, mensaje: str = "Loading"):
    """
    Show an animated loading bar
    
    Args:
        duracion: Duration in seconds
        mensaje: Message to show
    """
    ocultar_cursor()
    
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    inicio = time.time()
    i = 0
    
    while time.time() - inicio < duracion:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r\033[96m{frame} {mensaje}...\033[0m")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    
    sys.stdout.write(f"\r\033[92m✓ {mensaje} done!\033[0m\n")
    sys.stdout.flush()
    
    mostrar_cursor()


def puntos_suspensivos(mensaje: str = "Processing", duracion: float = 2.0):
    """
    Show animated ellipsis
    
    Args:
        mensaje: Base message
        duracion: Duration in seconds
    """
    ocultar_cursor()
    
    inicio = time.time()
    puntos = 0
    
    while time.time() - inicio < duracion:
        sys.stdout.write(f"\r\033[93m{mensaje}{'.' * puntos}   \033[0m")
        sys.stdout.flush()
        time.sleep(0.5)
        puntos = (puntos + 1) % 4
    
    sys.stdout.write(f"\r\033[92m{mensaje} ✓\033[0m\n")
    sys.stdout.flush()
    
    mostrar_cursor()


# ============================================================
# INIT
# ============================================================

# Ensure assets dir exists
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Create initial config if missing
if not CONFIG_PATH.exists():
    cargar_config()


# English aliases (new API)
hide_cursor = ocultar_cursor
show_cursor = mostrar_cursor
load_config = cargar_config
save_config = guardar_config
get_transition = obtener_transicion
set_transition = cambiar_transicion
apply_transition = aplicar_transicion
loading_bar = barra_cargando
loading_dots = puntos_suspensivos
