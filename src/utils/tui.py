#!/usr/bin/env python3
"""
Zero-dependency navigable TUI in the style of TokenHub
(InquirerPy: green `?` prompt + `❯` pointer).

Flicker-free by design:
  - ONE full clear when the menu opens (banner + list painted once).
  - Arrow keys only repaint the option block IN PLACE: the cursor
    moves up exactly the block's row count and the block is
    reprinted with `ESC[K` (clear-to-end-of-line) per row.
  - No `clear` per keypress (that fork + full repaint was the blink).
  - Every printed line is truncated to the terminal width, so a
    logical line is ALWAYS exactly one physical row — the row math
    can't drift, even with wide chars or pinch-zoom.
  - If the terminal is resized mid-navigation, we resync once
    (full clear + header + block) and keep going.

Usage:
    from src.utils.tui import select_index

    idx = select_index(
        "What would you like to do?",
        ["Download content", "Convert files", "Exit"],
        header_fn=lambda: print("BANNER..."),
    )
    # idx -> int | None (None = cancelled with q/Esc)

Controls:
    up/k  move up        down/j  move down
    Enter select         q/Esc cancel
    1-9  quick pick      Ctrl+C cancel

Non-TTY fallback: numbered input prompt.
"""

import shutil
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
    """Read one key (incl. arrows) on Unix. Returns: up/down/enter/esc/q/char.

    NOTE: reads with os.read() on the raw fd, NOT sys.stdin.read().
    sys.stdin is a buffered TextIOWrapper: read(1) slurps the whole
    escape sequence (ESC [ A) into its internal buffer, so a later
    select() on the fd sees nothing and arrows were misread as Esc
    (which cancelled the menu). os.read() bypasses that buffer.
    """
    import os
    import select
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        def _read(timeout=None):
            if timeout is not None:
                r, _, _ = select.select([fd], [], [], timeout)
                if not r:
                    return ""
            try:
                data = os.read(fd, 1)
            except OSError:
                return ""
            if not data:
                return ""
            return data.decode("utf-8", errors="ignore")

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


# ---------------------------------------------------------------
# Width-aware, wrap-free rendering (one logical line == one row)
# ---------------------------------------------------------------

def _term_cols(default: int = 80) -> int:
    try:
        return max(20, shutil.get_terminal_size().columns)
    except Exception:
        return default


def _char_w(ch: str) -> int:
    try:
        from wcwidth import wcwidth
        w = wcwidth(ch)
        return w if w and w > 0 else 0
    except Exception:
        import unicodedata
        return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


def _vwidth(text: str) -> int:
    return sum(_char_w(c) for c in text)


def _truncate(text: str, max_w: int) -> str:
    """Cut plain text to max_w columns (ellipsis if cut)."""
    if _vwidth(text) <= max_w:
        return text
    out, w = [], 0
    for ch in text:
        cw = _char_w(ch)
        if w + cw > max_w - 1:  # reserve 1 col for "…"
            break
        out.append(ch)
        w += cw
    return "".join(out) + "…"


def _ansi_clear() -> None:
    """Single full clear (ANSI only, no fork) for menu open / resync."""
    sys.stdout.write("\033[2J\033[3J\033[H")
    sys.stdout.flush()


def _block_rows(title: str, options: list, hint: str) -> int:
    """Row count of the managed block (all lines wrap-free, so exact)."""
    rows = 1 + 1  # question line + blank
    for opt in options:
        rows += 1 + str(opt).count("\n")
    rows += 1  # blank
    if hint:
        rows += 1
    return rows


def _print_block(title: str, options: list, selected: int,
                 hint: str, cols: int) -> int:
    """Print the managed block; every line fits cols (no wrap)."""
    from src.utils.animations import ocultar_cursor
    ocultar_cursor()

    def _line(color: str, plain: str):
        sys.stdout.write(color + _truncate(plain, cols) + Style.RESET_ALL + "\033[K\n")

    # InquirerPy-style question (two-tone, width-safe)
    sys.stdout.write(Fore.GREEN + Style.BRIGHT + f"{PROMPT_SYMBOL} " + Style.RESET_ALL)
    _line(Fore.WHITE + Style.BRIGHT, title)
    _line("", "")
    for i, opt in enumerate(options):
        parts = str(opt).split("\n")
        marker = f"{POINTER} {i + 1}." if i == selected else f"  {i + 1}."
        if i == selected:
            _line(Fore.CYAN + Style.BRIGHT, f"{marker} {parts[0]}")
            for cont in parts[1:]:
                _line(Fore.CYAN, f"     {cont}")
        else:
            _line(Fore.WHITE, f"{marker} {parts[0]}")
            for cont in parts[1:]:
                _line(Fore.LIGHTBLACK_EX, f"     {cont}")
    _line("", "")
    if hint:
        _line(Fore.LIGHTBLACK_EX, hint)
    sys.stdout.flush()
    return _block_rows(title, options, hint)


def select_index(title: str, options: list, initial: int = 0,
                 header_fn=None, hint: str = None) -> int | None:
    """Interactive arrow-key picker (TokenHub-style, flicker-free).

    Args:
        title: Question shown InquirerPy-style (`? title`).
        options: Display strings (may contain newlines for subtitles).
        initial: Initially highlighted index.
        header_fn: Optional callable painted once above the list
            (banner, etc). Repainted only on resize resync.
        hint: Footer hint (default mentions arrows/Enter/quick-pick).

    Returns:
        Selected index or None if cancelled.
    """
    from src.utils.animations import mostrar_cursor, ocultar_cursor

    if not options:
        return None

    if hint is None:
        if len(options) <= 9:
            hint = "up/down navigate • Enter select • 1-{} jump • q back".format(len(options))
        else:
            hint = "up/down navigate • Enter select • q back"

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
        cols = _term_cols()
        _ansi_clear()
        if header_fn is not None:
            try:
                header_fn()
            except Exception:
                pass
        rows = _print_block(title, options, selected, hint, cols)
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
            new_cols = _term_cols()
            if new_cols != cols:
                # Resize/zoom mid-navigation: resync layout once.
                cols = new_cols
                _ansi_clear()
                if header_fn is not None:
                    try:
                        header_fn()
                    except Exception:
                        pass
                rows = _print_block(title, options, selected, hint, cols)
            else:
                sys.stdout.write(f"\033[{rows}A")
                rows = _print_block(title, options, selected, hint, cols)
    finally:
        mostrar_cursor()
        print()
