#!/usr/bin/env python3
"""
Shared UI helpers — inspired by TokenHub (rich Panel + robust clear)
and the `player` bash script (~/.local/bin/player).

Style guide:
  - Always clear with clear_screen() (scrollback-safe, like TokenHub).
  - Print the app header with print_header() (player-style box).
  - Menus are numbered lists with a "▶" prompt (player-style).
  - Pause with pause() ("Press Enter to continue...").

Author: Shadow-TermDev
Web: https://Shadow-TermDev.github.io
"""

import os
import sys

from colorama import Fore, Style

APP_NAME = "Data Downloader"

# Player-style box width (number of ─)
HEADER_WIDTH = 42


def clear_screen() -> None:
    """Clear screen + scrollback (TokenHub-style, no leftovers).

    Uses ANSI erase (ESC[2J scrollback ESC[3J home ESC[H) then falls
    back to the OS `clear`/`cls` command.
    """
    try:
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
        try:
            sys.stderr.write("\033[2J\033[3J\033[H")
            sys.stderr.flush()
        except Exception:
            pass
    except Exception:
        pass
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


def print_header(app_name: str = APP_NAME, version: str = "") -> None:
    """Player-style header box:

    ╔══════════════════════════════════════════╗
    ║   Data Downloader v1.7.0                 ║
    ╚══════════════════════════════════════════╝
    """
    bar = "═" * HEADER_WIDTH
    title = f"{app_name} {version}".strip()
    # Pad/truncate to fit inside the box
    inner = f"  {title}  "
    if len(inner) > HEADER_WIDTH:
        inner = inner[:HEADER_WIDTH]
    inner = inner.ljust(HEADER_WIDTH)
    print(Fore.CYAN + f"╔{bar}╗")
    print(Fore.CYAN + "║" + Fore.YELLOW + inner + Fore.CYAN + "║")
    print(Fore.CYAN + f"╚{bar}╝" + Style.RESET_ALL)
    print()


def print_status_line(text: str) -> None:
    """One-line status (player `short_status` vibe)."""
    print(Fore.CYAN + f"♪ {text}" + Style.RESET_ALL)


def prompt_choice(prompt: str = "  -> Enter option number: ") -> str:
    """Show cursor, read input with a player-style ▶ prompt."""
    from src.utils.animations import mostrar_cursor, ocultar_cursor
    mostrar_cursor()
    try:
        return input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
    finally:
        ocultar_cursor()


def pause(message: str = "\n🔹 Press Enter to continue...") -> None:
    """TokenHub-style pause (Enter to continue)."""
    from src.utils.helpers import pausar as _pausar
    _pausar(mensaje=message, mostrar=True)
