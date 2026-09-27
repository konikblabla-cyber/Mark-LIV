"""Local Windows power status for JARVIS; deterministic and offline-capable."""
from __future__ import annotations

import json
import subprocess


def power_status(parameters=None, **kwargs):
    """Return compact Windows AC/battery power information."""
    result = {"battery_percent": None, "charging": None, "ac_line": None}
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery is not None:
            result["battery_percent"] = round(float(battery.percent), 1)
            result["charging"] = bool(battery.power_plugged)
            result["ac_line"] = "online" if battery.power_plugged else "offline"
            return json.dumps(result, ensure_ascii=False)
    except Exception as exc:
        result["error"] = str(exc)[:160]

    if __import__("os").name == "nt":
        try:
            proc = subprocess.run(
                ["powercfg", "/getactivescheme"],
                capture_output=True,
                text=True,
                timeout=3,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            result["active_scheme"] = (proc.stdout or proc.stderr).strip()[:240]
        except Exception as exc:
            result["powercfg_error"] = str(exc)[:160]
    return json.dumps(result, ensure_ascii=False)


TOOL = {
    "name": "power_status",
    "handler": power_status,
    "description": "Get local battery, charging and active Windows power information without Gemini.",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}
