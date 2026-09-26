"""Cheap local learning of repeated JARVIS action preferences."""
from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path

_LOCK = threading.Lock()
_PATH = Path(os.getenv("PROGRAMDATA", os.path.expanduser("~"))) / "Mark-LIV" / "jarvis_action_preferences.json"
_MAX_ACTIONS = 100
_MAX_COUNT = 2_147_483_647


def _load() -> dict:
    try:
        data = json.loads(_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    clean = {}
    for key, value in data.items():
        name = str(key).strip().lower()
        try:
            count = max(0, min(int(value), _MAX_COUNT))
        except (TypeError, ValueError):
            continue
        if name and len(name) <= 80 and count:
            clean[name] = count
    return clean


def _save(data: dict) -> None:
    _PATH.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".prefs-", suffix=".tmp", dir=str(_PATH.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(data, ensure_ascii=False, indent=2))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, _PATH)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def record_action(action: str) -> None:
    name = str(action or "").strip().lower()
    if not name or len(name) > 80:
        return
    with _LOCK:
        try:
            data = _load()
            data[name] = min(_MAX_COUNT, data.get(name, 0) + 1)
            if len(data) > _MAX_ACTIONS:
                data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True)[:_MAX_ACTIONS])
            _save(data)
        except Exception:
            pass


def preferred_action(action: str, min_uses: int = 3) -> bool:
    name = str(action or "").strip().lower()
    if not name:
        return False
    try:
        threshold = max(2, int(min_uses or 3))
    except (TypeError, ValueError):
        threshold = 3
    return any(item_name == name and count >= threshold for item_name, count in top_actions(20))


def top_actions(limit: int = 10) -> list[tuple[str, int]]:
    with _LOCK:
        data = _load()
    try:
        size = max(1, min(int(limit or 10), 20))
    except (TypeError, ValueError):
        size = 10
    return sorted(data.items(), key=lambda item: (-item[1], item[0]))[:size]


TOOL = {
    "name": "learned_preferences",
    "description": "Show locally learned repeated JARVIS action patterns. No Gemini or conversation text is stored.",
    "parameters": {"type": "OBJECT", "properties": {}},
    "handler": lambda parameters=None, **kwargs: "\n".join(
        f"{name}: {count} uses" for name, count in top_actions()
    ) or "No learned action preferences yet.",
}
