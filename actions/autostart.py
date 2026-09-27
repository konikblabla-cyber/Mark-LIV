"""Permission-gated JARVIS Windows autostart controls."""
from __future__ import annotations

from core.background_runtime import enable_autostart, disable_autostart, autostart_enabled

TOOL = [
    {"name":"autostart_enable","description":"Enable JARVIS automatic startup for the current Windows user.","parameters":{"type":"OBJECT","properties":{}},"handler":lambda parameters=None, **kwargs: enable_autostart()},
    {"name":"autostart_disable","description":"Disable JARVIS automatic startup for the current Windows user.","parameters":{"type":"OBJECT","properties":{}},"handler":lambda parameters=None, **kwargs: disable_autostart()},
    {"name":"autostart_status","description":"Check whether JARVIS automatic startup is enabled.","parameters":{"type":"OBJECT","properties":{}},"handler":lambda parameters=None, **kwargs: "Autostart enabled." if autostart_enabled() else "Autostart disabled."},
]
