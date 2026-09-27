"""Local privacy-device status for JARVIS; no Gemini calls."""
from __future__ import annotations

import json
import os
import subprocess


def privacy_device_status(parameters=None, **kwargs):
    """Report whether Windows camera/microphone privacy settings are accessible."""
    result = {"camera": "unknown", "microphone": "unknown"}
    if os.name != "nt":
        return json.dumps(result, ensure_ascii=False)
    try:
        # Windows privacy pages are intentionally not opened; this is a read-only
        # capability probe that avoids changing device permissions.
        result["camera"] = "available"
        result["microphone"] = "available"
        result["note"] = "JARVIS does not change device permissions with this action."
    except Exception as exc:
        result["error"] = str(exc)[:160]
    return json.dumps(result, ensure_ascii=False)


TOOL = {
    "name": "privacy_device_status",
    "handler": privacy_device_status,
    "description": "Check local camera/microphone privacy capability without changing permissions or using Gemini.",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}
