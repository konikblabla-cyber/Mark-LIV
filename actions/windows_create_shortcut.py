"""Create a Windows shortcut."""
import os
import platform
import subprocess

def windows_create_shortcut(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "windows_create_shortcut is Windows-only."
    p = parameters or {}
    target = str(p.get("target", "")).strip()
    link = str(p.get("shortcut", "")).strip()
    if not target or not link:
        return "Missing target or shortcut."
    if not os.path.exists(target):
        return f"Target not found: {target}"
    try:
        safe_target = target.replace("'", "''")
        safe_link = link.replace("'", "''")
        ps = (
            "$s=(New-Object -ComObject WScript.Shell).CreateShortcut("
            f"'{safe_link}');"
            f"$s.TargetPath='{safe_target}';$s.Save()"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
            check=True, capture_output=True, text=True, timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return f"Created shortcut: {link}"
    except (subprocess.SubprocessError, OSError) as e:
        return f"Failed to create shortcut: {e}"

TOOL = {
    "name": "windows_create_shortcut",
    "description": "Create a Windows .lnk shortcut to an existing target.",
    "parameters": {
        "type": "OBJECT",
        "properties": {"target": {"type": "STRING"}, "shortcut": {"type": "STRING"}},
        "required": ["target", "shortcut"],
    },
    "handler": windows_create_shortcut,
}
