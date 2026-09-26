"""Local daily planner for JARVIS; no Gemini/API calls required."""
from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

_LOCK = threading.Lock()
_PATH = Path(os.getenv("PROGRAMDATA", str(Path.home()))) / "Mark-LIV" / "jarvis_daily_tasks.json"
_MAX_TASKS = 200


def _read():
    try:
        data = json.loads(_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _write(tasks):
    _PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = _PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(tasks[-_MAX_TASKS:], ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, _PATH)


def _clean(text, limit=240):
    return " ".join(str(text or "").replace("\n", " ").split())[:limit]


def check_overdue_tasks():
    now = datetime.now()
    found = []
    with _LOCK:
        tasks = _read()
        changed = False
        for task in tasks:
            if task.get("status") != "open" or task.get("overdue_notified_at"):
                continue
            try:
                when = datetime.strptime(str(task.get("due") or ""), "%Y-%m-%d %H:%M")
            except ValueError:
                continue
            if when < now:
                task["overdue_notified_at"] = datetime.now(timezone.utc).isoformat()
                found.append({"id": task.get("id"), "title": task.get("title"), "due": task.get("due")})
                changed = True
        if changed:
            _write(tasks)
    return found

def daily_planner(parameters=None, **kwargs):
    """Add/list/complete/postpone local daily tasks. Deterministic and offline-capable."""
    p = parameters or {}
    action = str(p.get("action", "list")).strip().lower()

    with _LOCK:
        tasks = _read()

        if action == "add":
            title = _clean(p.get("title"))
            if not title:
                return "Task title is required."
            task = {
                "id": uuid.uuid4().hex[:10],
                "title": title,
                "priority": max(1, min(3, int(p.get("priority", 2) or 2))),
                "due": _clean(p.get("due"), 32),
                "status": "open",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            tasks.append(task)
            _write(tasks)

            # Valid YYYY-MM-DD HH:MM due times automatically get a local
            # Windows reminder. Free-form due text remains a normal task.
            due = task["due"]
            reminder_result = ""
            if due:
                try:
                    from datetime import datetime as _dt
                    _dt.strptime(due, "%Y-%m-%d %H:%M")
                    from actions.reminder import reminder
                    reminder_result = " " + reminder({
                        "date": due[:10],
                        "time": due[11:16],
                        "message": f"JARVIS task: {title}",
                    })
                except Exception:
                    pass
            return f"Task added: {title} [{task['id']}].{reminder_result}"

        if action in {"complete", "done"}:
            task_id = _clean(p.get("id"), 20)
            for task in tasks:
                if task.get("id") == task_id and task.get("status") == "open":
                    task["status"] = "done"
                    task["completed_at"] = datetime.now(timezone.utc).isoformat()
                    _write(tasks)
                    return f"Task completed: {task.get('title')}."
            return "Open task not found."

        if action == "postpone":
            task_id = _clean(p.get("id"), 20)
            due = _clean(p.get("due"), 32)
            for task in tasks:
                if task.get("id") == task_id and task.get("status") == "open":
                    task["due"] = due
                    task["updated_at"] = datetime.now(timezone.utc).isoformat()
                    _write(tasks)
                    return f"Task postponed: {task.get('title')}."
            return "Open task not found."
        if action == "upcoming":
            now = datetime.now()
            soon = []
            for task in tasks:
                if task.get("status") != "open":
                    continue
                try:
                    when = datetime.strptime(str(task.get("due") or ""), "%Y-%m-%d %H:%M")
                except ValueError:
                    continue
                delta = (when - now).total_seconds()
                if 0 <= delta <= 3600:
                    soon.append(task)
            soon.sort(key=lambda t: t.get("due") or "")
            if not soon:
                return "No tasks due within the next hour."
            return "\n".join(
                f"{t['id']} | {t['title']} | due {t['due']}" for t in soon[:20]
            )
        if action == "overdue":
            now = datetime.now()
            overdue = []
            for task in tasks:
                if task.get("status") != "open":
                    continue
                due = str(task.get("due") or "")
                try:
                    when = datetime.strptime(due, "%Y-%m-%d %H:%M")
                except ValueError:
                    continue
                if when < now:
                    overdue.append(task)
            overdue.sort(key=lambda t: t.get("due") or "")
            if not overdue:
                return "No overdue daily tasks."
            lines = [f"{t['id']} | {t['title']} | overdue {t['due']}" for t in overdue[:20]]
            try:
                from core.status_center import record
                record("planner", f"{len(overdue)} overdue task(s) detected", level="warning")
            except Exception:
                pass
            return "\n".join(lines)
        if action == "list":
            open_tasks = [t for t in tasks if t.get("status") == "open"]
            open_tasks.sort(key=lambda t: (int(t.get("priority", 2)), t.get("due") or "9999-99-99"))
            if not open_tasks:
                return "No open daily tasks."
            lines = [f"{t['id']} | P{t.get('priority', 2)} | {t['title']}" +
                     (f" | due {t['due']}" if t.get("due") else "") for t in open_tasks[:20]]
            return "\n".join(lines)

        if action == "next":
            open_tasks = [t for t in tasks if t.get("status") == "open"]
            open_tasks.sort(key=lambda t: (int(t.get("priority", 2)), t.get("due") or "9999-99-99"))
            if not open_tasks:
                return "No open daily tasks."
            t = open_tasks[0]
            return f"Next task: {t['title']} (id {t['id']}, priority {t.get('priority', 2)}" + (f", due {t['due']}" if t.get("due") else "") + ")."

        return "Use action=add, list, next, or complete."


TOOL = {
    "name": "daily_planner",
    "description": "Manage JARVIS's persistent personal daily task list locally without Gemini.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {"type": "STRING", "description": "add, list, next, complete, postpone, overdue, or upcoming."},
            "title": {"type": "STRING", "description": "Task title for add."},
            "id": {"type": "STRING", "description": "Task id for complete."},
            "priority": {"type": "INTEGER", "description": "1 highest, 2 normal, 3 low."},
            "due": {"type": "STRING", "description": "Optional due date/time text."},
        },
        "required": ["action"],
    },
}
