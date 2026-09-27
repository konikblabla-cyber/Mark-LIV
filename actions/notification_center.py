"""Local notification center for JARVIS; deterministic and offline-capable."""
from __future__ import annotations

import json
import os
import time

_STATE = os.path.join(
    os.getenv("PROGRAMDATA", os.path.expanduser("~")),
    "Mark-LIV",
    "jarvis_notifications.json",
)
_MAX = 50


def notification_center(parameters=None, **kwargs):
    """Add, list, acknowledge or clear compact local JARVIS notifications."""
    p = parameters or {}
    action = str(p.get("action") or "list").strip().lower()
    os.makedirs(os.path.dirname(_STATE), exist_ok=True)
    data = []
    try:
        with open(_STATE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, list):
                data = loaded[-_MAX:]
    except Exception:
        pass

    if action in {"add", "notify", "push"}:
        message = str(p.get("message") or "").strip()[:500]
        if not message:
            return json.dumps({"ok": False, "error": "message_required"}, ensure_ascii=False)
        item = {
            "id": str(int(time.time() * 1000)),
            "message": message,
            "level": str(p.get("level") or "info")[:20],
            "created_at": time.time(),
            "acknowledged": False,
        }
        data.append(item)
        data = data[-_MAX:]
    elif action in {"ack", "acknowledge"}:
        target = str(p.get("id") or "").strip()
        for item in data:
            if str(item.get("id")) == target:
                item["acknowledged"] = True
    elif action in {"clear", "clear_acknowledged"}:
        data = [x for x in data if not x.get("acknowledged")]
    elif action not in {"list", "status"}:
        return json.dumps({"ok": False, "error": "unknown_action"}, ensure_ascii=False)

    with open(_STATE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return json.dumps({"ok": True, "notifications": data[-20:]}, ensure_ascii=False)


TOOL = {
    "name": "notification_center",
    "handler": notification_center,
    "description": "Manage JARVIS local notifications: add, list, acknowledge or clear them without Gemini.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {"type": "STRING", "enum": ["add", "list", "ack", "clear"]},
            "message": {"type": "STRING"},
            "level": {"type": "STRING", "enum": ["info", "warning", "error"]},
            "id": {"type": "STRING"},
        },
        "required": [],
    },
}
