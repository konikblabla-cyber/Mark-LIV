"""Cheap local learning of repeated JARVIS action preferences.

Only operational patterns are stored: action name and a bounded usage count.
No conversation text, secrets, or personal content is recorded.
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path

_LOCK = threading.Lock()
_PATH = Path(os.getenv("PROGRAMDATA", os.path.expanduser("~"))) / "Mark-LIV" / "jarvis_action_preferences.json"
_MAX_ACTIONS = 100


def record_action(action: str) -> None:
    name = str(action or "").strip().lower()
    if not name or len(name) > 80:
        return
    with _LOCK:
        try:
            _PATH.parent.mkdir(parents=True, exist_ok=True)
            try:
                data = json.loads(_PATH.read_text(encoding="utf-8"))
            except Exception:
                data = {}
            if not isinstance(data, dict):
                data = {}
            data[name] = int(data.get(name, 0) or 0) + 1
            if len(data) > _MAX_ACTIONS:
                keep = sorted(data.items(), key=lambda item: item[1], reverse=True)[:_MAX_ACTIONS]
                data = dict(keep)
            _PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass


def preferred_action(action: str, min_uses: int = 3) -> bool:
    """Return whether an action has become a stable repeated preference."""
    name = str(action or "").strip().lower()
    if not name:
        return False
    return any(item_name == name and count >= max(2, int(min_uses or 3))
               for item_name, count in top_actions(20))


def top_actions(limit: int = 10) -> list[tuple[str, int]]:
    with _LOCK:
        try:
            data = json.loads(_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
    if not isinstance(data, dict):
        return []
    return sorted(
        ((str(k), int(v)) for k, v in data.items()),
        key=lambda item: item[1],
        reverse=True,
    )[:max(1, min(int(limit or 10), 20))]


TOOL = {
    "name": "learned_preferences",
    "description": "Show locally learned repeated JARVIS action patterns. No Gemini or conversation text is stored.",
    "parameters": {"type": "OBJECT", "properties": {}},
    "handler": lambda parameters=None, **kwargs: "\n".join(
        f"{name}: {count} uses" for name, count in top_actions()
    ) or "No learned action preferences yet.",
}
