"""Recent Windows event log inspection."""
import platform
import subprocess

def eventlog_recent(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "eventlog_recent is Windows-only."

    p = parameters or {}
    log = str(p.get("log", "System")).strip()
    try:
        count = max(1, min(int(p.get("count", 20)), 100))
    except (TypeError, ValueError):
        count = 20

    safe = log if log in {"System", "Application", "Security"} else "System"
    cmd = (
        f"Get-WinEvent -LogName '{safe}' -MaxEvents {count} | "
        "Select TimeCreated,Id,LevelDisplayName,ProviderName,Message | Format-List"
    )
    try:
        kwargs = {"capture_output": True, "text": True, "timeout": 20}
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        r = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", cmd],
            **kwargs,
        )
        return (r.stdout or r.stderr or "No events.")[:16000]
    except subprocess.TimeoutExpired:
        return "Event log query timed out."
    except OSError as e:
        return f"Could not query event log: {e}"

TOOL = {
    "name": "eventlog_recent",
    "description": "Read-only Windows recent event inspection for System, Application or Security logs.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "log": {"type": "STRING"},
            "count": {"type": "INTEGER"},
        },
        "required": ["log"],
    },
    "handler": eventlog_recent,
}
