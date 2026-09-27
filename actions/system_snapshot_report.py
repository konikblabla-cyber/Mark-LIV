"""Compact local system snapshot for JARVIS; deterministic and offline-capable."""
from __future__ import annotations

import json
import time

import psutil


def system_snapshot_report(parameters=None, **kwargs):
    """Return a compact JSON snapshot of CPU, memory, disk and uptime."""
    try:
        disk = psutil.disk_usage("/")
        result = {
            "cpu_percent": psutil.cpu_percent(interval=0.15),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
            "disk_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024 ** 3), 2),
            "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 2),
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"error": str(exc)[:160]}, ensure_ascii=False)


TOOL = {
    "name": "system_snapshot_report",
    "handler": system_snapshot_report,
    "description": "Get a compact local CPU, memory, disk and uptime snapshot without Gemini.",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}
