import re
from typing import Any, Iterable, List, Optional
from urllib.parse import parse_qs, urlparse

# Regex patterns harvested from aldale_yt_mcp
_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_PLAYLIST_ID_RE = re.compile(r"^(PL|UU|LL|FL|OL|RD|WL)[A-Za-z0-9_-]{10,200}$")
_ISO8601_DUR_RE = re.compile(
    r"^P"
    r"(?:(?P<days>\d+)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+)S)?"
    r")?$"
)

def extract_video_id(url_or_id: str) -> Optional[str]:
    """
    Extracts a YouTube video ID from a URL or string.
    """
    s = (url_or_id or "").strip()
    if _VIDEO_ID_RE.match(s):
        return s

    try:
        p = urlparse(s)
        host = (p.netloc or "").lower()
        path = p.path.strip("/")

        if "youtube.com" in host:
            qs = parse_qs(p.query)
            v = (qs.get("v") or [None])[0]
            if v and _VIDEO_ID_RE.match(v):
                return v

            parts = path.split("/")
            if len(parts) >= 2 and parts[0] in {"shorts", "embed", "v"}:
                cand = parts[1]
                if _VIDEO_ID_RE.match(cand):
                    return cand

        if "youtu.be" in host:
            cand = path.split("/")[0]
            if _VIDEO_ID_RE.match(cand):
                return cand
    except Exception:
        pass

    return None

def extract_playlist_id(url_or_id: str) -> Optional[str]:
    """
    Extracts a YouTube playlist ID from a URL or string.
    """
    s = (url_or_id or "").strip()

    if _PLAYLIST_ID_RE.match(s) and not _VIDEO_ID_RE.match(s):
        return s

    try:
        p = urlparse(s)
        qs = parse_qs(p.query)
        pl = (qs.get("list") or [None])[0]
        if pl and _PLAYLIST_ID_RE.match(pl):
            return pl
    except Exception:
        pass

    return None

def parse_iso8601_duration_to_seconds(dur: str) -> int:
    """
    Parses ISO8601 duration string (e.g., PT1H2M10S) to seconds.
    """
    m = _ISO8601_DUR_RE.match(dur or "")
    if not m:
        return 0
    days = int(m.group("days") or 0)
    hours = int(m.group("hours") or 0)
    minutes = int(m.group("minutes") or 0)
    seconds = int(m.group("seconds") or 0)
    return (((days * 24 + hours) * 60 + minutes) * 60) + seconds

def chunked(seq: List[Any], size: int) -> Iterable[List[Any]]:
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), size):
        yield seq[i : i + size]

def dedupe_preserve_order(items: Iterable[Any]) -> List[Any]:
    """Deduplicate items while preserving order."""
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def format_timestamp(seconds: float) -> str:
    """
    Convert float seconds to HH:MM:SS.mmm format.
    """
    seconds = max(0.0, seconds)
    ms = int((seconds - int(seconds)) * 1000)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"
