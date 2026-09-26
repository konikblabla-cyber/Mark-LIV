"""Small local status/event center for JARVIS.

No Gemini calls and bounded disk usage. It records only operational events,
not conversation contents or user data.
"""
from __future__ import annotations
import json
import os
import threading
from datetime import datetime, timezone

_LOCK = threading.Lock()
_PATH = os.path.join(
    os.getenv("PROGRAMDATA", os.path.expanduser("~")),
    "Mark-LIV", "jarvis_status.json",
)
_MAX_EVENTS = 80


def _now():
    return datetime.now(timezone.utc).isoformat()


def _read():
    try:
        with open(_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data.setdefault("events", [])
            return data
    except Exception:
        pass
    return {"events": []}


def _write(data):
    os.makedirs(os.path.dirname(_PATH), exist_ok=True)
    tmp = _PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _PATH)


def record(kind: str, message: str, *, level: str = "info") -> None:
    """Record a short operational event, bounded to the newest events."""
    event = {
        "at": _now(),
        "kind": str(kind or "event")[:40],
        "level": str(level or "info")[:16],
        "message": str(message or "")[:500],
    }
    with _LOCK:
        data = _read()
        data["events"] = (data.get("events", []) + [event])[-_MAX_EVENTS:]
        _write(data)


def recent(limit: int = 8):
    with _LOCK:
        events = _read().get("events", [])
    return list(reversed(events[-max(1, min(int(limit or 8), 20)):]))


def snapshot(limit: int = 8) -> dict:
    events = recent(limit)
    return {
        "events": events,
        "last_issue": next((e for e in events if e.get("level") in {"warning", "error"}), None),
        "last_fix": next((e for e in events if e.get("kind") in {"repair", "maintenance"}), None),
    }
