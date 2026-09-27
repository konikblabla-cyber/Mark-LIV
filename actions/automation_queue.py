"""Persistent local automation queue for JARVIS; deterministic and offline-capable."""
from __future__ import annotations

import json
import os
import time
import uuid

_STATE = os.path.join(os.getenv("PROGRAMDATA", os.path.expanduser("~")), "Mark-LIV", "jarvis_automation_queue.json")
_MAX = 100


def claim_due(limit=1):
    """Atomically claim due queued goals for the runtime scheduler."""
    os.makedirs(os.path.dirname(_STATE), exist_ok=True)
    items = []
    try:
        with open(_STATE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, list):
                items = loaded[-_MAX:]
    except Exception:
        return []
    now = time.time()
    claimed = []
    for item in items:
        if len(claimed) >= max(1, int(limit)):
            break
        if item.get("status") != "queued":
            continue
        try:
            run_after = float(item.get("run_after") or 0)
        except (TypeError, ValueError):
            run_after = 0
        if run_after > now:
            continue
        item["status"] = "running"
        item["started_at"] = now
        claimed.append(dict(item))
    if claimed:
        tmp = _STATE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(items[-_MAX:], f, ensure_ascii=False)
        os.replace(tmp, _STATE)
    return claimed


def finish_claimed(item_id, result, success):
    """Persist the result of a scheduler claim."""
    os.makedirs(os.path.dirname(_STATE), exist_ok=True)
    items = []
    try:
        with open(_STATE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, list):
                items = loaded[-_MAX:]
    except Exception:
        return False
    for item in items:
        if str(item.get("id")) == str(item_id):
            item["updated_at"] = time.time()
            item["result"] = str(result or "")[:1800]
            repeat = float(item.get("repeat_seconds") or 0)
            if success and repeat > 0:
                item["status"] = "queued"
                item["run_after"] = time.time() + min(repeat, 365 * 24 * 3600)
            else:
                item["status"] = "completed" if success else "failed"
            break
    tmp = _STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items[-_MAX:], f, ensure_ascii=False)
    os.replace(tmp, _STATE)
    return True


def automation_queue(parameters=None, **kwargs):
    """Queue, list, cancel or complete deferred JARVIS goals."""
    p = parameters or {}
    action = str(p.get("action") or "list").strip().lower()
    os.makedirs(os.path.dirname(_STATE), exist_ok=True)
    items = []
    try:
        with open(_STATE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            if isinstance(loaded, list):
                items = loaded[-_MAX:]
    except Exception:
        pass

    if action in {"add", "queue"}:
        goal = str(p.get("goal") or "").strip()[:500]
        if not goal:
            return json.dumps({"ok": False, "error": "goal_required"}, ensure_ascii=False)
        item = {
            "id": uuid.uuid4().hex[:16],
            "goal": goal,
            "created_at": time.time(),
            "run_after": float(p.get("run_after") or time.time()),
            "status": "queued",
            "repeat_seconds": max(0, float(p.get("repeat_seconds") or 0)),
        }
        items.append(item)
    elif action in {"cancel", "complete"}:
        target = str(p.get("id") or "").strip()
        new_status = "cancelled" if action == "cancel" else "completed"
        for item in items:
            if str(item.get("id")) == target:
                item["status"] = new_status
                item["updated_at"] = time.time()
    elif action not in {"list", "status"}:
        return json.dumps({"ok": False, "error": "unknown_action"}, ensure_ascii=False)

    with open(_STATE, "w", encoding="utf-8") as f:
        json.dump(items[-_MAX:], f, ensure_ascii=False)
    return json.dumps({"ok": True, "queue": items[-20:]}, ensure_ascii=False)


TOOL = {
    "name": "automation_queue",
    "handler": automation_queue,
    "description": "Persist and manage deferred JARVIS goals locally so planned work can survive restarts.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {"type": "STRING", "enum": ["add", "list", "cancel", "complete"]},
            "goal": {"type": "STRING"},
            "id": {"type": "STRING"},
            "run_after": {"type": "NUMBER"},
            "repeat_seconds": {"type": "NUMBER"},
        },
        "required": [],
    },
}
