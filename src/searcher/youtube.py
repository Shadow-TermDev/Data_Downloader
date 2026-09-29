#!/usr/bin/env python3
"""
YouTube search prototype (yt-dlp ytsearch).

Flow (player/TokenHub-style):
  1. Ask for a query.
  2. Fetch top N results with yt-dlp (no download).
  3. Show a numbered selection box.
  4. Return the chosen video URL (or "" if cancelled).

Author: Shadow-TermDev
"""

from typing import List, Dict
from colorama import Fore, Style

from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.boxes import print_info_box, print_error_box, print_selection_box


def search_youtube(query: str, limit: int = 8) -> List[Dict]:
    """Search YouTube and return [{title, url, duration, uploader}].

    Args:
        query: Search text.
        limit: Max results (1-15).

    Returns:
        List of result dicts (empty on error).
    """
    import yt_dlp

    limit = max(1, min(int(limit), 15))
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "nocheckcertificate": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            entries = info.get("entries", []) or []
            results = []
            for e in entries:
                if not e:
                    continue
                vid = e.get("id", "")
                title = (e.get("title") or "Unknown title")[:60]
                duration = e.get("duration") or 0
                uploader = (e.get("uploader") or e.get("channel") or "?")[:25]
                url = e.get("webpage_url") or (f"https://www.youtube.com/watch?v={vid}" if vid else "")
                if not url:
                    continue
                results.append({
                    "title": title,
                    "url": url,
                    "duration": duration,
                    "uploader": uploader,
                })
            return results
    except Exception as e:
        print(Fore.RED + f"\n❌ Search failed: {str(e)[:80]}")
        return []


def format_duration(seconds: int) -> str:
    """Format seconds as m:ss."""
    try:
        seconds = int(seconds or 0)
        return f"{seconds // 60}:{seconds % 60:02d}"
    except Exception:
        return "--:--"


def pick_result(results: List[Dict]) -> Dict | None:
    """Show results in a selection box, return chosen dict or None."""
    if not results:
        print_error_box("❌ NO RESULTS", ["No videos found. Try another query."])
        return None

    lines, colors = [], []
    for i, r in enumerate(results):
        marker = "▶ " if i == 0 else "  "
        color = Fore.GREEN if i == 0 else Fore.WHITE
        lines.append(f"{marker}{i + 1}. {r['title'][:45]}")
        colors.append(color)
        lines.append(f"     ⏱ {format_duration(r['duration'])}  │  👤 {r['uploader']}")
        colors.append(Fore.CYAN)

    print_selection_box("🔎 SEARCH RESULTS", lines, colors)
    print(Fore.CYAN + "   ℹ️  Option 1 is the top result (0 = cancel)")

    while True:
        mostrar_cursor()
        sel = input(Fore.YELLOW + "\n➜ " + Fore.CYAN + f"Pick video [0-{len(results)}]: " + Style.RESET_ALL).strip()
        ocultar_cursor()
        if sel == "0" or sel.lower() in ("q", "cancel", "back"):
            return None
        if sel.isdigit() and 1 <= int(sel) <= len(results):
            chosen = results[int(sel) - 1]
            print(Fore.GREEN + f"   ✓ Selected: {chosen['title'][:50]}")
            return chosen
        print(Fore.RED + "   ❌ Invalid option")


def search_and_pick() -> str:
    """Interactive prototype: query -> results -> URL ("" if cancelled).

    Returns:
        Video URL or empty string.
    """
    ocultar_cursor()
    try:
        print_info_box("🔎 YOUTUBE SEARCH (prototype)")
        mostrar_cursor()
        query = input(Fore.YELLOW + "\n🔎 Search YouTube: " + Style.RESET_ALL).strip()
        ocultar_cursor()
        if not query:
            print(Fore.RED + "❌ Empty query.")
            return ""
        print(Fore.CYAN + f"\n⏳ Searching for '{query[:40]}'...")
        results = search_youtube(query, limit=8)
        chosen = pick_result(results)
        return chosen["url"] if chosen else ""
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Search cancelled")
        return ""
