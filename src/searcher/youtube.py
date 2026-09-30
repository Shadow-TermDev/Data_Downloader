#!/usr/bin/env python3
"""
YouTube search (yt-dlp ytsearch, fast flat mode).

Flow:
  1. Ask for a query.
  2. Fetch top N results with yt-dlp (flat, no per-video fetch).
  3. Show a navigable arrow-key list (title + duration + uploader).
  4. Return the chosen video URL (or "" if cancelled).

Author: Shadow-TermDev
"""

from typing import List, Dict
from colorama import Fore, Style

from src.utils.animations import ocultar_cursor, mostrar_cursor
from src.utils.boxes import print_info_box, print_error_box


def search_youtube(query: str, limit: int = 8) -> List[Dict]:
    """Search YouTube and return [{title, url, duration, uploader}].

    Uses flat extraction (fast: no per-video webpage fetch).

    Args:
        query: Search text.
        limit: Max results (1-15).

    Returns:
        List of result dicts (empty on error).
    """
    import time

    import yt_dlp

    limit = max(1, min(int(limit), 15))
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "socket_timeout": 20,
        "retries": 2,
        # NOTE: no custom http_headers here — a spoofed Android
        # User-Agent makes YouTube search return 0 entries.
    }
    # YouTube search API is flaky (empty pages / rate limits) — retry.
    last_error = ""
    for attempt in range(3):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                entries = info.get("entries", []) or []
                results = []
                for e in entries:
                    if not e or not isinstance(e, dict):
                        continue
                    # Flat entries expose `url`, full ones `webpage_url`
                    vid = (e.get("id") or "").strip()
                    url = (
                        e.get("webpage_url")
                        or e.get("url")
                        or (f"https://www.youtube.com/watch?v={vid}" if vid else "")
                    )
                    if not url:
                        continue
                    if "://" not in url and vid:
                        url = f"https://www.youtube.com/watch?v={vid}"
                    title = (e.get("title") or "Unknown title").strip()[:70]
                    try:
                        duration = int(e.get("duration") or 0)
                    except Exception:
                        duration = 0
                    uploader = (
                        e.get("uploader") or e.get("channel")
                        or e.get("uploader_id") or "?"
                    ).strip()[:30]
                    results.append({
                        "title": title,
                        "url": url,
                        "duration": duration,
                        "uploader": uploader,
                    })
            if results:
                return results
            last_error = "empty response"
        except Exception as exc:
            last_error = str(exc)[:120]
        if attempt < 2:
            time.sleep(1.5 * (attempt + 1))
    if last_error:
        print(Fore.RED + f"\n❌ Search failed after 3 tries: {last_error}")
    return []


def format_duration(seconds: int) -> str:
    """Format seconds as m:ss (or h:mm:ss)."""
    try:
        seconds = int(seconds or 0)
        if seconds <= 0:
            return "live/--:--"
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        if h:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"
    except Exception:
        return "--:--"


def pick_result(results: List[Dict], query: str = "") -> Dict | None:
    """Show results in a navigable arrow-key list, return chosen dict or None."""
    if not results:
        print_error_box("❌ NO RESULTS", ["No videos found. Try another query."])
        return None

    from src.utils.tui import select_index

    def _header():
        print_info_box(f"🔎 YOUTUBE SEARCH{(': ' + query[:30]) if query else ''}")

    options = [
        f"🎬 {r['title'][:55]}\n⏱ {format_duration(r['duration'])}  │  👤 {r['uploader']}"
        for r in results
    ]
    idx = select_index(
        f"{len(results)} results — pick a video to download",
        options,
        header_fn=_header,
        hint="↑/↓ navigate • Enter download • 1-8 jump • q cancel",
    )
    if idx is None:
        return None
    chosen = results[idx]
    print(Fore.GREEN + f"   ✓ Selected: {chosen['title'][:60]}")
    return chosen


def search_and_pick() -> str:
    """Interactive search: query -> navigable list -> URL ("" if cancelled).

    Returns:
        Video URL or empty string.
    """
    ocultar_cursor()
    try:
        print_info_box("🔎 YOUTUBE SEARCH")
        mostrar_cursor()
        query = input(Fore.YELLOW + "\n🔎 Search YouTube: " + Style.RESET_ALL).strip()
        ocultar_cursor()
        if not query:
            print(Fore.RED + "❌ Empty query.")
            return ""
        print(Fore.CYAN + f"\n⏳ Searching for '{query[:40]}'...")
        results = search_youtube(query, limit=8)
        chosen = pick_result(results, query=query)
        return chosen["url"] if chosen else ""
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Search cancelled")
        return ""
