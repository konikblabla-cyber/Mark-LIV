"""One-command local diagnostic report for JARVIS; no Gemini calls."""
from __future__ import annotations

import json
import platform
import time

import psutil


def diagnostic_report(parameters=None, action_registry=None, **kwargs):
    """Aggregate core health, PC resources, tasks and recent operational events."""
    result = {"ok": True, "platform": platform.platform()[:180]}
    try:
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\") if platform.system() == "Windows" else psutil.disk_usage("/")
        result["resources"] = {
            "cpu_percent": psutil.cpu_percent(interval=0.15),
            "memory_percent": mem.percent,
            "disk_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024 ** 3), 2),
            "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 2),
        }
    except Exception as exc:
        result["resources_error"] = str(exc)[:160]

    try:
        from actions.autonomous_tasks import jarvis_self_test
        test = jarvis_self_test({}, action_registry=action_registry)
        result["self_test"] = str(test)[:2200]
        result["ok"] = result["ok"] and "attention needed" not in str(test).lower()
    except Exception as exc:
        result["self_test"] = "unavailable: " + str(exc)[:160]
        result["ok"] = False

    try:
        from core.status_center import snapshot
        status = snapshot(6)
        result["status_center"] = {
            "health": status.get("health", "OK"),
            "warnings": status.get("warnings", 0),
            "errors": status.get("errors", 0),
            "last_issue": (status.get("last_issue") or {}).get("message", "")[:220],
            "last_fix": (status.get("last_fix") or {}).get("message", "")[:220],
        }
        if status.get("errors", 0):
            result["ok"] = False
    except Exception as exc:
        result["status_center"] = {"error": str(exc)[:160]}

    try:
        from core.task_manager import TaskManager
        tasks = TaskManager().recoverable()
        result["recoverable_tasks"] = [
            {"id": str(t.get("id", ""))[:24], "status": str(t.get("status", ""))[:24],
             "goal": str(t.get("goal", ""))[:120]}
            for t in tasks[:5]
        ]
    except Exception as exc:
        result["tasks_error"] = str(exc)[:160]

    return json.dumps(result, ensure_ascii=False)


TOOL = {
    "name": "diagnostic_report",
    "handler": diagnostic_report,
    "description": "Create a compact local diagnostic report covering JARVIS health, PC resources, tasks and recent issues without Gemini.",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}
