"""Local network status for JARVIS; deterministic and offline-capable."""
from __future__ import annotations

import json
import platform
import socket
import subprocess


def network_status(parameters=None, **kwargs):
    """Return compact local connectivity and adapter information."""
    result = {"connected": False, "hostname": socket.gethostname(), "interfaces": []}
    try:
        if platform.system() == "Windows":
            proc = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
                timeout=4,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            text = proc.stdout or ""
            adapters = []
            current = None
            for raw in text.splitlines():
                line = raw.strip()
                if line and not line.startswith(("IPv4", "IPv6", "Subnet", "Default Gateway", "DNS")) and line.endswith(":"):
                    current = line.rstrip(":")
                    adapters.append(current)
            result["interfaces"] = adapters[:12]
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=1.5).close()
            result["connected"] = True
        except OSError:
            pass
    except Exception as exc:
        result["error"] = str(exc)[:160]
    return json.dumps(result, ensure_ascii=False)


TOOL = {
    "name": "network_status",
    "handler": network_status,
    "description": "Check local network connectivity and detected Windows network adapters without Gemini.",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}
