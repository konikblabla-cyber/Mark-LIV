"""Save a screenshot to the user's Desktop on demand."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import mss
import mss.tools

def quick_screenshot(parameters=None, **kwargs):
    p = parameters or {}
    try:
        monitor = int(p.get("monitor", 1))
    except (TypeError, ValueError):
        monitor = 1
    with mss.mss() as sct:
        monitors = sct.monitors
        if monitor < 1 or monitor >= len(monitors):
            monitor = 1 if len(monitors) > 1 else 0
        shot = sct.grab(monitors[monitor])
        desktop = Path.home() / "Desktop"
        desktop.mkdir(parents=True, exist_ok=True)
        path = desktop / f"JARVIS_Screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        mss.tools.to_png(shot.rgb, shot.size, output=str(path))
    return f"Screenshot saved to {path}"

TOOL = {
    "name": "quick_screenshot",
    "description": "Take a screenshot of a selected monitor and save it to the user's Desktop.",
    "parameters": {"type":"OBJECT","properties":{"monitor":{"type":"INTEGER","description":"Monitor number starting at 1; omit for the primary monitor."}},"required":[]},
    "handler": quick_screenshot,
}
