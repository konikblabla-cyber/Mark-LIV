"""Risk-aware policy for autonomous JARVIS decisions."""
from __future__ import annotations

from dataclasses import dataclass

from core.permissions import needs_confirmation

READ_ONLY = frozenset({
    "inspect", "read", "list", "search", "status", "audit", "calculate", "get",
})
_HIGH_MARKERS = (
    "delete", "remove", "uninstall", "format", "shutdown", "restart",
    "kill", "terminate", "admin", "firewall", "security",
)
_MEDIUM_MARKERS = (
    "write", "edit", "move", "copy", "rename", "install",
    "service", "registry", "permission",
)


@dataclass(frozen=True)
class Risk:
    level: str
    reason: str


def classify(action: str, parameters: dict | None = None) -> Risk:
    name = str(action or "").strip().lower()
    if not name:
        return Risk("high", "empty action is not safe to execute")
    if needs_confirmation(name):
        return Risk("high", "destructive or externally consequential action")
    if any(marker in name for marker in _HIGH_MARKERS):
        return Risk("high", "action name indicates an irreversible or privileged change")
    if any(marker in name for marker in _MEDIUM_MARKERS):
        return Risk("medium", "action changes system or user state")
    return Risk("low", "read-only or low-impact operation")


def can_autonomously_chain(action: str, parameters: dict | None = None) -> bool:
    return classify(action, parameters).level != "high"
