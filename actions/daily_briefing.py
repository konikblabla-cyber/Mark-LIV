"""Local JARVIS daily briefing; deterministic and offline-capable."""
from __future__ import annotations

from datetime import datetime
import json


def daily_briefing(parameters=None, **kwargs):
    """Build a compact morning/status briefing without Gemini."""
    parts = [f"JARVIS briefing — {datetime.now():%Y-%m-%d %H:%M}"]

    try:
        from actions.daily_planner import summarize_due_tasks
        tasks = summarize_due_tasks(24 * 60)
        if tasks:
            parts.append("Tasks: " + "; ".join(
                f"{t.get('title', 'unnamed')} ({t.get('due', 'no due time')})"
                for t in tasks[:5]
            ))
        else:
            parts.append("Tasks: nothing due or overdue in the next 24h.")
    except Exception:
        parts.append("Tasks: unavailable.")

    try:
        from actions.autonomous_tasks import jarvis_status
        status = str(jarvis_status({}))
        lines = [line.strip() for line in status.splitlines() if line.strip()]
        if lines:
            parts.append("System: " + " | ".join(lines[:4]))
    except Exception:
        pass

    try:
        from actions.pc_status import pc_status
        info = json.loads(str(pc_status({})))
        parts.append("PC: " + " | ".join([
            f"CPU {info.get("cpu_percent", "?")}%",
            f"RAM {info.get("ram_percent", "?")}%",
            f"uptime {info.get("uptime_hours", "?")}h",
        ]))
    except Exception:
        parts.append("PC: unavailable.")

    return "\n".join(parts)[:2500]


TOOL = {
    "name": "daily_briefing",
    "handler": daily_briefing,
    "description": "Give a compact local JARVIS morning/status briefing with tasks and PC state; no Gemini call.",
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}
