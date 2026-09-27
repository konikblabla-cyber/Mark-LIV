"""Local focus mode controller for JARVIS; no Gemini calls."""
from __future__ import annotations

import json
import os
import subprocess
import time

_STATE = os.path.join(os.getenv("PROGRAMDATA", os.path.expanduser("~")), "Mark-LIV", "jarvis_focus.json")


def focus_mode(parameters=None, **kwargs):
    """Enable, disable or inspect a lightweight Windows focus mode."""
    p = parameters or {}
    action = str(p.get("action") or "status").strip().lower()
    state = {"enabled": False, "started_at": None}
    try:
        with open(_STATE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, dict):
                state.update(loaded)
    except Exception:
        pass

    if action in {"on", "enable", "start"}:
        state["enabled"] = True
        state["started_at"] = time.time()
        os.makedirs(os.path.dirname(_STATE), exist_ok=True)
        with open(_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f)
        return json.dumps({"ok": True, "enabled": True, "mode": "local_focus"}, ensure_ascii=False)

    if action in {"off", "disable", "stop"}:
        state["enabled"] = False
        state["started_at"] = None
        os.makedirs(os.path.dirname(_STATE), exist_ok=True)
        with open(_STATE, "w", encoding="utf-8") as f:
            json.dump(state, f)
        return json.dumps({"ok": True, "enabled": False, "mode": "local_focus"}, ensure_ascii=False)

    return json.dumps({
        "ok": True,
        "enabled": bool(state.get("enabled")),
        "started_at": state.get("started_at"),
        "mode": "local_focus",
    }, ensure_ascii=False)


TOOL = {
    "name": "focus_mode",
    "handler": focus_mode,
    "description": "Enable, disable or inspect JARVIS local focus mode state without Gemini.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {"type": "STRING", "enum": ["on", "off", "status"]},
        },
        "required": [],
    },
}
