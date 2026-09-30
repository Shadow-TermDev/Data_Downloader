#!/usr/bin/env python3
"""
Zero-dependency navigable TUI in the style of TokenHub
(InquirerPy: green `?` prompt + `❯` pointer) and `player`
(full redraw on every key, like menu_clasico).

Why full redraw instead of cursor-up re-render?
  - Pinch-zoom / font-size changes alter terminal columns mid-session.
  - Long lines + emoji wrap to extra rows, so "move cursor up N lines"
    math drifts and leaves garbage on screen.
  - Clearing and repainting (player pattern) is immune to all of that.

Usage:
    from src.utils.tui import select_index

    idx = select_index(
        "What would you like to do?",
        ["📥 Download content", "🔄 Convert files", "🚪 Exit"],
        header_fn=lambda: print("BANNER..."),
    )
    # idx -> int | None (None = cancelled with q/Esc)

Controls:
    ↑/k  move up        ↓/j  move down
    Enter select         q/Esc cancel
    1-9  quick pick      Ctrl+C cancel

Non-TTY fallback: numbered input prompt.
"""

import sys

from colorama import Fore, Style

POINTER = "❯"
PROMPT_SYMBOL = "?"


def _is_tty() -> bool:
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        return False


def _read_key_unix():
    """Read one key (incl. arrows) on Unix. Returns: up/down/enter/esc/q/char."""
    import select
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        def _read(timeout=None):
            if timeout is None:
                return sys.stdin.read(1)
            r, _, _ = select.select([sys.stdin], [], [], timeout)
            return sys.stdin.read(1) if r else ""

        ch = _read()
        if ch == "\x03":  # Ctrl+C
            raise KeyboardInterrupt
        if ch == "\r" or ch == "\n":
            return "enter"
        if ch == "\x1b":  # Esc alone OR arrow sequence
            ch2 = _read(timeout=0.15)
            if ch2 == "[":
                ch3 = _read(timeout=0.15)
                if ch3 == "A":
                    return "up"
                if ch3 == "B":
                    return "down"
                return "esc"
            return "esc"  # plain Esc, no hang waiting for more bytes
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


def _draw(title: str, options: list, selected: int, hint: str,
          header_fn=None) -> None:
    """Full repaint: optional header, InquirerPy-style prompt, options, hint."""
    from src.utils.animations import ocultar_cursor
    from src.utils.helpers import limpiar_pantalla

    limpiar_pantalla()
    ocultar_cursor()

    if header_fn is not None:
        try:
            header_fn()
        except Exception:
            pass

    # TokenHub/InquirerPy-style question line
    print(
        Fore.GREEN + Style.BRIGHT + f"{PROMPT_SYMBOL} "
        + Style.RESET_ALL + Fore.WHITE + Style.BRIGHT + title
        + Style.RESET_ALL
    )
    print()

    for i, opt in enumerate(options):
        first, *rest = str(opt).split("\n")
        number = f"{i + 1}."
        if i == selected:
            print(
                Fore.CYAN + Style.BRIGHT + f"{POINTER} {number} {first}"
                + Style.RESET_ALL
            )
            for cont in rest:
                print(Fore.CYAN + f"    {cont}" + Style.RESET_ALL)
        else:
            print(Fore.WHITE + f"  {number} {first}" + Style.RESET_ALL)
            for cont in rest:
                print(Fore.LIGHTBLACK_EX + f"    {cont}" + Style.RESET_ALL)
    print()
    if hint:
        print(Fore.LIGHTBLACK_EX + hint + Style.RESET_ALL)


def select_index(title: str, options: list, initial: int = 0,
                 header_fn=None, hint: str = None) -> int | None:
    """Interactive arrow-key picker (TokenHub-style).

    Args:
        title: Question shown InquirerPy-style (`? title`).
        options: Display strings (may contain newlines for subtitles).
        initial: Initially highlighted index.
        header_fn: Optional callable repainted above the list (banner, etc).
        hint: Footer hint (default mentions arrows/Enter/quick-pick).

    Returns:
        Selected index or None if cancelled.
    """
    from src.utils.animations import mostrar_cursor

    if not options:
        return None

    if hint is None:
        if len(options) <= 9:
            hint = "↑/↓ navigate • Enter select • 1-{} jump • q back".format(len(options))
        else:
            hint = "↑/↓ navigate • Enter select • q back"

    # Non-interactive fallback: numbered prompt
    if not _is_tty():
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        mostrar_cursor()
        try:
            sel = input(Fore.CYAN + f"  -> Pick [1-{len(options)}] (q=cancel): " + Style.RESET_ALL).strip()
        finally:
            from src.utils.animations import ocultar_cursor
            ocultar_cursor()
        if sel.lower() in ("q", "quit", "cancel", "back", ""):
            return None
        if sel.isdigit() and 1 <= int(sel) <= len(options):
            return int(sel) - 1
        return None

    selected = max(0, min(initial, len(options) - 1))
    try:
        _draw(title, options, selected, hint, header_fn)
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
            _draw(title, options, selected, hint, header_fn)
    finally:
        mostrar_cursor()
