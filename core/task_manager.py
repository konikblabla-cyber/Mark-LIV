"""Persistent state for long-running JARVIS autonomous tasks."""
from __future__ import annotations
import json
import os
import threading
import uuid
from datetime import datetime, timezone
from typing import Any

_LOCK = threading.Lock()
_PATH = os.path.join(os.getenv("PROGRAMDATA", os.path.expanduser("~")), "Mark-LIV", "jarvis_tasks.json")

class TaskManager:
    def __init__(self, path: str = _PATH):
        self.path = path
        self._ensure()

    def _ensure(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            self._write({})

    def _read(self) -> dict:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _write(self, data: dict):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    def create(self, goal: str) -> str:
        task_id = uuid.uuid4().hex[:12]
        now = datetime.now(timezone.utc).isoformat()
        with _LOCK:
            data = self._read()
            data[task_id] = {"id": task_id, "goal": goal, "status": "running",
                             "created_at": now, "updated_at": now, "history": [],
                             "next_step": 0}
            self._write(data)
        return task_id

    def update(self, task_id: str, **fields):
        # Keep task metadata bounded so repeated recovery errors cannot grow
        # the persistent state indefinitely.
        if "failure" in fields:
            fields["failure"] = str(fields["failure"] or "")[:800]
        if "goal" in fields:
            fields["goal"] = str(fields["goal"] or "")[:500]
        with _LOCK:
            data = self._read()
            if task_id not in data:
                return
            data[task_id].update(fields)
            data[task_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._write(data)

    def step(self, task_id: str, action: str, result: Any, verified: bool):
        with _LOCK:
            data = self._read()
            task = data.get(task_id)
            if not task:
                return
            task["history"].append({"action": action, "result": str(result)[:4000],
                                    "verified": verified,
                                    "at": datetime.now(timezone.utc).isoformat()})
            task["next_step"] = int(task.get("next_step", 0)) + 1
            task["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._write(data)

    def get(self, task_id: str):
        with _LOCK:
            return self._read().get(task_id)

    def recoverable(self):
        with _LOCK:
            return [v for v in self._read().values()
                    if v.get("status") in {"running", "waiting_confirmation", "paused"}]

    def prune_finished(self, max_items: int = 100) -> int:
        """Bound completed task history so the local state file cannot grow forever."""
        limit = max(10, min(int(max_items or 100), 500))
        with _LOCK:
            data = self._read()
            finished = [
                (str(v.get("updated_at") or ""), key)
                for key, v in data.items()
                if v.get("status") == "completed"
            ]
            if len(finished) <= limit:
                return 0
            finished.sort()
            remove = finished[:-limit]
            for _, key in remove:
                data.pop(key, None)
            self._write(data)
            return len(remove)
