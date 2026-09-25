"""Persistent one-shot countdown timer using Windows Task Scheduler."""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from xml.sax.saxutils import escape


def timer(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Windows-only action."

    p = parameters or {}
    try:
        seconds = int(p.get("seconds", 0))
    except (TypeError, ValueError):
        return "Timer duration must be an integer number of seconds."

    if not 1 <= seconds <= 7 * 24 * 3600:
        return "Timer must be between 1 second and 7 days."

    message = " ".join(str(p.get("message", "Timer finished")).split())[:300] or "Timer finished"
    target = datetime.now() + timedelta(seconds=seconds)
    name = f"JARVISTimer_{target.strftime('%Y%m%d_%H%M%S_%f')}"

    root = Path.home() / ".jarvis" / "timers"
    root.mkdir(parents=True, exist_ok=True)

    script = root / f"{name}.py"
    script_body = (
        "import json, pathlib, subprocess\n"
        f"message = {json.dumps(message, ensure_ascii=False)}\n"
        "try:\n"
        "    from win10toast import ToastNotifier\n"
        "    ToastNotifier().show_toast('J.A.R.V.I.S Timer', message, duration=15, threaded=False)\n"
        "except Exception:\n"
        "    subprocess.run(['msg', '*', '/TIME:30', message], check=False, "
        "creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))\n"
        "try:\n"
        "    import winsound\n"
        "    for frequency in (800, 1000, 1200):\n"
        "        winsound.Beep(frequency, 180)\n"
        "except Exception:\n"
        "    pass\n"
        "pathlib.Path(__file__).unlink(missing_ok=True)\n"
    )
    script.write_text(script_body, encoding="utf-8")

    exe = Path(sys.executable).parent / "pythonw.exe"
    if not exe.exists():
        exe = Path(sys.executable)

    xml = root / f"{name}.xml"
    xml.write_text(
        f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
<Triggers><TimeTrigger><StartBoundary>{target.strftime("%Y-%m-%dT%H:%M:%S")}</StartBoundary><Enabled>true</Enabled></TimeTrigger></Triggers>
<Actions Context="Author"><Exec><Command>{escape(str(exe))}</Command><Arguments>{escape(f'"{script}"')}</Arguments></Exec></Actions>
<Settings><StartWhenAvailable>true</StartWhenAvailable><ExecutionTimeLimit>PT5M</ExecutionTimeLimit></Settings>
<Principals><Principal id="Author"><LogonType>InteractiveToken</LogonType><RunLevel>LeastPrivilege</RunLevel></Principal></Principals>
</Task>''',
        encoding="utf-16",
    )

    try:
        result = subprocess.run(
            ["schtasks.exe", "/Create", "/TN", name, "/XML", str(xml), "/F"],
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    finally:
        xml.unlink(missing_ok=True)

    if result.returncode:
        script.unlink(missing_ok=True)
        return "Windows Task Scheduler could not create the timer."

    return f"Timer set for {seconds} seconds."


TOOL = {
    "name": "timer",
    "description": "Set a persistent one-shot countdown timer from 1 second up to 7 days.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "seconds": {
                "type": "INTEGER",
                "description": "Countdown duration in seconds.",
            },
            "message": {
                "type": "STRING",
                "description": "Notification text when the timer finishes.",
            },
        },
        "required": ["seconds"],
    },
    "handler": timer,
}
