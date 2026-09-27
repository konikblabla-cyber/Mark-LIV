"""Local JARVIS incident report; deterministic and offline-capable."""
from __future__ import annotations

import json
import time


def jarvis_incident_report(parameters=None, **kwargs):
    """Return a compact report of recent JARVIS issues, fixes and recoverable tasks."""
    result = {"generated_at": time.time()}
    try:
        from core.status_center import snapshot
        s = snapshot(12)
        result["health"] = s.get("health", "OK")
        result["warnings"] = s.get("warnings", 0)
        result["errors"] = s.get("errors", 0)
        result["last_issue"] = str((s.get("last_issue") or {}).get("message", ""))[:300]
        result["last_fix"] = str((s.get("last_fix") or {}).get("message", ""))[:300]
    except Exception as exc:
        result["status_error"] = str(exc)[:160]
    try:
        from core.task_manager import TaskManager
        result["recoverable_tasks"] = [
            {"id": str(t.get("id", ""))[:24], "status": str(t.get("status", ""))[:24],
             "goal": str(t.get("goal", ""))[:120]}
            for t in TaskManager().recoverable()[:5]
        ]
    except Exception as exc:
        result["tasks_error"] = str(exc)[:160]
    return json.dumps(result, ensure_ascii=False)


TOOL = {
    "name": "jarvis_incident_report",
    "handler": jarvis_incident_report,
    "description": "Create a compact local report of recent JARVIS issues, fixes and recoverable tasks without Gemini.",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}
