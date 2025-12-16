"""
Sistema de animaciones y efectos visuales
Autor: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import sys
import time
import json
import os
from pathlib import Path
from typing import Optional

from config.settings import ASSETS_DIR, DEFAULT_TRANSITION, ANIMATION_SPEED


# Ruta del archivo de configuración
CONFIG_PATH = ASSETS_DIR / "config.json"


# ============================================================
# MANEJO DEL CURSOR
# ============================================================

def ocultar_cursor():
    """Oculta el cursor para mejorar la estética"""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def mostrar_cursor():
    """Vuelve a mostrar el cursor"""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


# ============================================================
# MANEJO DE CONFIGURACIÓN
# ============================================================

def cargar_config() -> dict:
    """
    Carga la configuración actual desde config.json
    
    Returns:
        Diccionario con la configuración
    """
    # Crear archivo si no existe
    if not CONFIG_PATH.exists():
        config_inicial = {
            "transicion": DEFAULT_TRANSITION,
            "velocidad_animacion": ANIMATION_SPEED,
            "tema": "default"
        }
        guardar_config(config_inicial)
        return config_inicial
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("\033[91m⚠️ Error al leer config.json, usando valores predeterminados.\033[0m")
        return {"transicion": DEFAULT_TRANSITION}


def guardar_config(config: dict) -> bool:
    """
    Guarda la configuración en config.json
    
    Args:
        config: Diccionario con la configuración
        
    Returns:
        True si se guardó correctamente
    """
    try:
        # Asegurar que el directorio existe
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        print("\033[91m⚠️ No se pudo guardar la configuración.\033[0m")
        return False


def obtener_transicion() -> str:
    """
    Obtiene la transición seleccionada por el usuario
    
    Returns:
        Nombre de la transición
    """
    return cargar_config().get("transicion", DEFAULT_TRANSITION)


def cambiar_transicion(nueva_transicion: str):
    """
    Cambia la transición y la guarda
    
    Args:
        nueva_transicion: Nombre de la nueva transición
    """
    config = cargar_config()
    config["transicion"] = nueva_transicion
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
    except:
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

def barra_cargando(duracion: float = 2.0, mensaje: str = "Cargando"):
    """
    Muestra una barra de carga animada
    
    Args:
        duracion: Duración en segundos
        mensaje: Mensaje a mostrar
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
    
    sys.stdout.write(f"\r\033[92m✓ {mensaje} completado!\033[0m\n")
    sys.stdout.flush()
    
    mostrar_cursor()


def puntos_suspensivos(mensaje: str = "Procesando", duracion: float = 2.0):
    """
    Muestra puntos suspensivos animados
    
    Args:
        mensaje: Mensaje base
        duracion: Duración en segundos
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
# INICIALIZACIÓN
# ============================================================

# Asegurar que el directorio de assets existe
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Crear config inicial si no existe
if not CONFIG_PATH.exists():
    cargar_config()
