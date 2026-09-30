#!/usr/bin/env python3
"""
Zero-dependency navigable TUI (arrow keys + Enter).

TokenHub uses InquirerPy and `player` uses fzf / a classic
arrow-key menu — this is the stdlib equivalent so Termux
needs no extra packages.

Usage:
    from src.utils.tui import select_index

    idx = select_index("Pick an option", ["Download", "Convert", "Exit"])
    # idx -> int | None (None = cancelled with q/Esc)

Controls:
    ↑/k  move up        ↓/j  move down
    Enter select         q/Esc cancel
    1-9  quick pick      Ctrl+C cancel

Non-TTY fallback: numbered input prompt.
"""

import sys

from colorama import Fore, Style


def _is_tty() -> bool:
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        return False


def _read_key_unix():
    """Read one key (incl. arrows) on Unix. Returns: up/down/enter/esc/q/char."""
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x03":  # Ctrl+C
            raise KeyboardInterrupt
        if ch == "\r" or ch == "\n":
            return "enter"
        if ch == "\x1b":  # Esc or arrow
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                if ch3 == "A":
                    return "up"
                if ch3 == "B":
                    return "down"
                return "esc"
            return "esc"
        if ch in ("q", "Q"):
            return "q"
        if ch in ("k", "K"):
            return "up"
        if ch in ("j", "J"):
            return "down"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _read_key_windows():
    """Read one key on Windows. Returns: up/down/enter/esc/q/char."""
    import msvcrt

    ch = msvcrt.getch()
    if ch in (b"\x03",):
        raise KeyboardInterrupt
    if ch == b"\r":
        return "enter"
    if ch == b"\x1b":
        return "esc"
    if ch in (b"\x00", b"\xe0"):  # special keys (arrows)
        ch2 = msvcrt.getch()
        if ch2 == b"H":
            return "up"
        if ch2 == b"P":
            return "down"
        return "esc"
    try:
        c = ch.decode("utf-8", errors="ignore")
    except Exception:
        return ""
    if c in ("q", "Q"):
        return "q"
    if c in ("k", "K"):
        return "up"
    if c in ("j", "J"):
        return "down"
    return c


def _read_key():
    if sys.platform.startswith("win"):
        return _read_key_windows()
    return _read_key_unix()


def _render(title: str, options: list, selected: int, hint: str = "") -> int:
    """Render the list, return number of terminal lines printed."""
    from src.utils.animations import ocultar_cursor
    ocultar_cursor()
    lines_printed = 0
    if title:
        print(Fore.YELLOW + title + Style.RESET_ALL)
        lines_printed += 1
    for i, opt in enumerate(options):
        marker = "▸" if i == selected else " "
        if i == selected:
            print(Fore.BLACK + "\033[7m" + f" {marker} {opt} " + Style.RESET_ALL)
        else:
            print(f" {marker} {opt}")
        # Multiline options (e.g. search results) take extra rows
        lines_printed += 1 + opt.count("\n")
    if hint:
        print(Fore.CYAN + hint + Style.RESET_ALL)
        lines_printed += 1
    return lines_printed


def select_index(title: str, options: list, initial: int = 0,
                 hint: str = "↑/↓ navigate • Enter select • q cancel") -> int | None:
    """Interactive arrow-key picker.

    Args:
        title: Header shown above the list.
        options: Display strings (may contain newlines).
        initial: Initially highlighted index.
        hint: Footer hint line ("" to hide).

    Returns:
        Selected index or None if cancelled.
    """
    from src.utils.animations import mostrar_cursor, ocultar_cursor

    if not options:
        return None

    # Non-interactive fallback: numbered prompt
    if not _is_tty():
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        mostrar_cursor()
        try:
            sel = input(Fore.CYAN + f"  -> Pick [1-{len(options)}] (q=cancel): " + Style.RESET_ALL).strip()
        finally:
            ocultar_cursor()
        if sel.lower() in ("q", "quit", "cancel", "back", ""):
            return None
        if sel.isdigit() and 1 <= int(sel) <= len(options):
            return int(sel) - 1
        return None

    selected = max(0, min(initial, len(options) - 1))
    ocultar_cursor()
    try:
        lines = _render(title, options, selected, hint)
        while True:
            try:
                key = _read_key()
            except KeyboardInterrupt:
                return None
            if key == "up":
                selected = (selected - 1) % len(options)
            elif key == "down":
                selected = (selected + 1) % len(options)
            elif key == "enter":
                return selected
            elif key in ("q", "esc"):
                return None
            elif isinstance(key, str) and key.isdigit() and key != "0":
                n = int(key)
                if 1 <= n <= len(options):
                    return n - 1
                continue
            else:
                continue
            # Re-render in place
            sys.stdout.write(f"\033[{lines}A")
            lines = _render(title, options, selected, hint)
    finally:
        mostrar_cursor()
        print()
