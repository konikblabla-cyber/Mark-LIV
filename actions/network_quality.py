"""Local network quality probe for JARVIS; deterministic and offline-capable."""
from __future__ import annotations

import json
import socket
import time
import urllib.request


def network_quality(parameters=None, **kwargs):
    """Measure basic DNS and HTTPS reachability/latency without Gemini."""
    result = {"internet": False, "dns_ms": None, "https_ms": None}
    try:
        started = time.perf_counter()
        socket.getaddrinfo("example.com", 443, type=socket.SOCK_STREAM)
        result["dns_ms"] = round((time.perf_counter() - started) * 1000, 1)
    except OSError as exc:
        result["dns_error"] = str(exc)[:160]

    try:
        started = time.perf_counter()
        req = urllib.request.Request("https://example.com/", method="HEAD")
        with urllib.request.urlopen(req, timeout=3) as response:
            result["https_status"] = int(getattr(response, "status", 200))
        result["https_ms"] = round((time.perf_counter() - started) * 1000, 1)
        result["internet"] = True
    except Exception as exc:
        result["https_error"] = str(exc)[:160]

    return json.dumps(result, ensure_ascii=False)


TOOL = {
    "name": "network_quality",
    "handler": network_quality,
    "description": "Measure basic DNS and HTTPS connectivity latency locally without Gemini.",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}
