"""List and cancel persistent JARVIS timers created through Windows Task Scheduler."""
from __future__ import annotations
import csv
import io
import platform
import subprocess
from pathlib import Path


PREFIX = "JARVISTimer_"
ROOT = Path.home() / ".jarvis" / "timers"


def _run(args):
    return subprocess.run(
        args, capture_output=True, text=True, timeout=30,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def _list():
    r = _run(["schtasks.exe", "/Query", "/FO", "CSV", "/NH"])
    if r.returncode:
        return "No active JARVIS timers."
    rows = []
    try:
        for row in csv.reader(io.StringIO(r.stdout)):
            if row and row[0].startswith(PREFIX):
                rows.append(row)
    except Exception:
        return "Could not read Windows timers."
    if not rows:
        return "No active JARVIS timers."
    return "\n".join(
        f"{row[0]} | {row[1] if len(row) > 1 else ''} | {row[2] if len(row) > 2 else ''}"
        for row in rows
    )


def _cancel(name):
    name = str(name or "").strip()
    if not name:
        return "Timer name is required."
    if not name.startswith(PREFIX) or any(c in name for c in "\\/:"):
        return "Invalid JARVIS timer name."
    r = _run(["schtasks.exe", "/Delete", "/TN", name, "/F"])
    if r.returncode:
        return (r.stderr or r.stdout or "Timer cancellation failed.").strip()
    ROOT.mkdir(parents=True, exist_ok=True)
    for path in ROOT.glob(name + ".*"):
        try:
            path.unlink()
        except OSError:
            pass
    return f"Timer {name} cancelled."


def timer_manager(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."
    p = parameters or {}
    action = str(p.get("action", "list")).lower().strip()
    if action == "list":
        return _list()
    if action == "cancel":
        return _cancel(p.get("name"))
    return "Use action=list or action=cancel."


TOOL = {
    "name": "timer_manager",
    "description": "List active JARVIS timers or cancel a specific JARVIS timer.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {"type": "STRING", "description": "list or cancel."},
            "name": {"type": "STRING", "description": "Exact JARVISTimer task name when cancelling."},
        },
        "required": ["action"],
    },
    "handler": timer_manager,
}
