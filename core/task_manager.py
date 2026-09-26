"""Persistent state for long-running JARVIS autonomous tasks."""
from __future__ import annotations

import json
import os
import tempfile
import threading
import uuid
from datetime import datetime, timezone
from typing import Any

_LOCK = threading.Lock()
_PATH = os.path.join(
    os.getenv("PROGRAMDATA", os.path.expanduser("~")),
    "Mark-LIV",
    "jarvis_tasks.json",
)
_ALLOWED_FIELDS = frozenset({
    "status", "goal", "failure", "next_step", "plan", "waiting_for",
})


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
        directory = os.path.dirname(self.path)
        os.makedirs(directory, exist_ok=True)
        fd, tmp = tempfile.mkstemp(
            prefix=f".{os.path.basename(self.path)}.",
            suffix=".tmp",
            dir=directory,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self.path)
        finally:
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass

    def create(self, goal: str) -> str:
        task_id = uuid.uuid4().hex[:12]
        now = datetime.now(timezone.utc).isoformat()
        with _LOCK:
            data = self._read()
            data[task_id] = {
                "id": task_id,
                "goal": str(goal or "")[:500],
                "status": "running",
                "created_at": now,
                "updated_at": now,
                "history": [],
                "next_step": 0,
            }
            self._write(data)
        return task_id

    def update(self, task_id: str, **fields):
        safe_fields = {
            key: value for key, value in fields.items()
            if key in _ALLOWED_FIELDS
        }
        if "failure" in safe_fields:
            safe_fields["failure"] = str(safe_fields["failure"] or "")[:800]
        if "goal" in safe_fields:
            safe_fields["goal"] = str(safe_fields["goal"] or "")[:500]
        if "status" in safe_fields:
            status = str(safe_fields["status"] or "").strip().lower()
            if status not in {"running", "waiting_confirmation", "paused", "completed", "failed"}:
                return
            safe_fields["status"] = status
        if "next_step" in safe_fields:
            try:
                safe_fields["next_step"] = max(0, min(int(safe_fields["next_step"]), 10000))
            except (TypeError, ValueError):
                return
        with _LOCK:
            data = self._read()
            task = data.get(task_id)
            if not isinstance(task, dict):
                return
            task.update(safe_fields)
            task["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._write(data)

    def step(self, task_id: str, action: str, result: Any, verified: bool):
        with _LOCK:
            data = self._read()
            task = data.get(task_id)
            if not isinstance(task, dict):
                return
            history = task.get("history")
            if not isinstance(history, list):
                history = []
                task["history"] = history
            history.append({
                "action": str(action)[:120],
                "result": str(result)[:1200],
                "verified": bool(verified),
                "at": datetime.now(timezone.utc).isoformat(),
            })
            if len(history) > 50:
                task["history"] = history[-50:]
            try:
                current_step = max(0, min(int(task.get("next_step", 0)), 10000))
            except (TypeError, ValueError):
                current_step = 0
            task["next_step"] = current_step + 1
            task["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._write(data)

    def get(self, task_id: str):
        with _LOCK:
            return self._read().get(task_id)

    def recoverable(self):
        with _LOCK:
            data = self._read()
            return [
                v for v in data.values()
                if isinstance(v, dict)
                and v.get("status") in {"running", "waiting_confirmation", "paused"}
            ]

    def prune_finished(self, max_items: int = 100) -> int:
        try:
            limit = max(10, min(int(max_items or 100), 500))
        except (TypeError, ValueError):
            limit = 100
        with _LOCK:
            data = self._read()
            finished = [
                (str(v.get("updated_at") or ""), key)
                for key, v in data.items()
                if isinstance(v, dict) and v.get("status") == "completed"
            ]
            if len(finished) <= limit:
                return 0
            finished.sort()
            remove = finished[:-limit]
            for _, key in remove:
                data.pop(key, None)
            self._write(data)
            return len(remove)
