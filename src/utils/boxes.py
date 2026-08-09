"""
Cajas UI consistentes para todo el proyecto
Autor: Shadow-TermDev
Estándar visual:
  - Usar SOLO líneas simples (─) coherente con menú principal
  - Ancho estándar: 54 (BOX_WIDTH) · Info: 50 (INFO_WIDTH)
  - Colores: GREEN=éxito, CYAN=info/progreso, RED=error, YELLOW=títulos

NUNCA imprimas bordes manualmente. Usa print_box() o las cajas con nombre.
El ancho se calcula automáticamente según el contenido más largo.
"""

import re

from colorama import Fore

# Constantes de diseño - ancho de borde (número de ─)
BOX_WIDTH = 54
INFO_WIDTH = 50

# Caracteres de caja simples
TL = "╭"  # top-left
TR = "╮"  # top-right
BL = "╰"  # bottom-left
BR = "╯"  # bottom-right
HL = "─"  # horizontal line
VL = "│"  # vertical line
TL_D = "├"  # separador izquierdo
TR_D = "┤"  # separador derecho

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def ancho_visual(texto: str) -> int:
    """
    Ancho visible de un texto para alinear cajas.
    Ignora códigos ANSI y estima ancho de emojis/caracteres anchos.

    Args:
        texto: Texto a medir (puede contener códigos de color)

    Returns:
        Ancho en columnas de terminal
    """
    texto = _ANSI_RE.sub("", texto)
    try:
        from wcwidth import wcswidth

        ancho = wcswidth(texto)
        return ancho if ancho >= 0 else len(texto)
    except Exception:
        try:
            import unicodedata

            total = 0
            for ch in texto:
                if unicodedata.combining(ch):
                    continue
                total += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
            return total
        except Exception:
            return len(texto)


def _padd(texto: str, ancho: int, alinear: str = "left") -> str:
    """
    Rellena un texto (que puede incluir color) hasta el ancho visible pedido

    Args:
        texto: Texto a rellenar
        ancho: Ancho visible objetivo
        alinear: 'left', 'center' o 'right'

    Returns:
        Texto rellenado con espacios
    """
    diff = ancho - ancho_visual(texto)
    if diff <= 0:
        return texto
    if alinear == "center":
        izq = diff // 2
        return " " * izq + texto + " " * (diff - izq)
    if alinear == "right":
        return " " * diff + texto
    return texto + " " * diff


def _ancho_optimo(titulo: str, lineas: list, minimo: int) -> int:
    """Calcula el ancho de contenido necesario para que nada se desborde"""
    ancho = minimo
    if titulo:
        ancho = max(ancho, ancho_visual(titulo))
    for linea in lineas:
        ancho = max(ancho, ancho_visual(linea))
    return ancho


def print_box(
    titulo: str = None,
    lineas: list = None,
    borde=Fore.GREEN,
    color_titulo: str = Fore.WHITE,
    colores: list = None,
    ancho: int = None,
    separador: bool = True,
):
    """
    Caja genérica con ajuste automático de ancho.

    Args:
        titulo: Texto del título (centrado). None para omitir.
        lineas: Lista de líneas de contenido (alineadas a la izquierda)
        borde: Color del borde (colorama)
        color_titulo: Color del texto del título
        colores: Lista opcional de colores por línea de contenido
        ancho: Ancho mínimo del contenido. Auto por defecto.
        separador: Si True imprime línea bajo el título
    """
    if lineas is None:
        lineas = []

    minimo = ancho if ancho else (BOX_WIDTH - 2)
    ancho_cont = _ancho_optimo(titulo, lineas, minimo)
    lineas = [str(linea) for linea in lineas]

    print()
    print(f"{borde}{TL}{HL * (ancho_cont + 2)}{TR}")

    if titulo:
        print(f"{borde}{VL} {_padd(color_titulo + str(titulo), ancho_cont, 'center')} {borde}{VL}")
        if separador:
            print(f"{borde}{TL_D}{HL * (ancho_cont + 2)}{TR_D}")

    for i, linea in enumerate(lineas):
        color = colores[i] if colores and i < len(colores) else Fore.WHITE
        color_linea = color + _padd(linea, ancho_cont)
        print(f"{borde}{VL} {color_linea} {borde}{VL}")

    print(f"{borde}{BL}{HL * (ancho_cont + 2)}{BR}")


# ===== CAJA GENÉRICA (configurable) =====
def print_generic_box(titulo: str = None, lineas: list = None, borde=Fore.GREEN,
                      color_titulo: str = Fore.WHITE, colores: list = None,
                      ancho: int = None, separador: bool = True):
    """Alias de print_box para casos de uso generales"""
    print_box(titulo=titulo, lineas=lineas, borde=borde, color_titulo=color_titulo,
              colores=colores, ancho=ancho, separador=separador)


# ===== CAJA DE ÉXITO (VERDE) =====
def print_success_box(titulo: str, lineas: list, colores: list = None):
    """Imprime caja de éxito completa"""
    print_box(titulo=titulo, lineas=lineas, borde=Fore.GREEN, color_titulo=Fore.YELLOW, colores=colores)


# ===== CAJA DE INFO/ANÁLISIS (CYAN) =====
def print_info_box(titulo: str):
    """Imprime caja de info simple (solo título, sin contenido)"""
    print_box(titulo=titulo, lineas=[], borde=Fore.CYAN, color_titulo=Fore.WHITE,
              ancho=INFO_WIDTH - 2, separador=False)


# ===== CAJA DE ERROR (ROJO) =====
def print_error_box(titulo: str, lineas: list = None, colores: list = None):
    """Imprime caja de error"""
    print_box(titulo=titulo, lineas=lineas or [], borde=Fore.RED, color_titulo=Fore.WHITE, colores=colores)


# ===== CAJA DE ADVERTENCIA (AMARILLO) =====
def print_warning_box(titulo: str, lineas: list = None, colores: list = None):
    """Imprime caja de advertencia/confirmación"""
    print_box(titulo=titulo, lineas=lineas or [], borde=Fore.YELLOW,
              color_titulo=Fore.WHITE, colores=colores)


# ===== CAJA DE SELECCIÓN/MENÚ (CYAN) =====
def print_selection_box(titulo: str, lineas: list, colores: list = None):
    """Imprime caja de selección (calidades, opciones)"""
    print_box(titulo=titulo, lineas=lineas, borde=Fore.CYAN,
              color_titulo=Fore.YELLOW, colores=colores)


# ===== CAJA DE MENÚ PRINCIPAL (MAGENTA) =====
def print_menu_box(lineas: list, colores: list = None):
    """Imprime caja para menús (sin título interno, elegante y compacta)"""
    print_box(titulo=None, lineas=lineas, borde=Fore.MAGENTA, colores=colores)


# ===== PROGRESO =====
def print_progress_bar(percent: float, speed: str = "", eta: str = "", width: int = 25):
    """Barra de progreso simple"""
    blocks = int((percent / 100) * width)
    blocks = max(0, min(blocks, width))
    bar = "█" * blocks + "░" * (width - blocks)
    extra = f" │ {speed}" if speed else ""
    extra += f" │ ETA: {eta}" if eta else ""
    print(f"\r{Fore.CYAN}▓{bar}▓ {percent:.1f}%{extra}", end="", flush=True)


def print_progress_done():
    """Limpia y muestra completado"""
    print(f"\r{Fore.GREEN}✓ Completado".ljust(50) + "\n")


def clear_progress_line(width: int = 50):
    print(" " * width, end="\r")