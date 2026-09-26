"""Safety guardrails for autonomous planning."""
from __future__ import annotations

import os
from typing import Any

from core.permissions import PROTECTED_PROCESSES, needs_confirmation

PROTECTED_PATHS = {
    os.path.normcase(os.path.abspath(os.environ.get("WINDIR", r"C:\Windows"))),
    os.path.normcase(os.path.abspath(os.environ.get("PROGRAMFILES", r"C:\Program Files"))),
    os.path.normcase(os.path.abspath(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"))),
}
DESTRUCTIVE_PATH_ACTIONS = {"delete_file", "delete_folder", "format_drive"}
PROCESS_ACTIONS = {"kill_process", "terminate_process", "close_active", "close_process"}


def _protected_path(path: str) -> bool:
    try:
        expanded = os.path.expandvars(path)
        normalized = os.path.normcase(os.path.abspath(expanded))
        real = os.path.normcase(os.path.realpath(expanded))
    except Exception:
        return False

    for protected in PROTECTED_PATHS:
        if (
            normalized == protected
            or normalized.startswith(protected + os.sep)
            or real == protected
            or real.startswith(protected + os.sep)
        ):
            return True
    return False


def validate_step(action: str, parameters: dict[str, Any]) -> tuple[bool, str]:
    action = str(action or "").strip()
    if not action:
        return False, "empty action"
    if not isinstance(parameters, dict):
        return False, "invalid parameters"

    # Autonomous planning can request risky actions, but it can never
    # smuggle human approval through parameters.
    if needs_confirmation(action):
        for key in ("confirmed", "confirm", "approved", "force_confirm"):
            if key in parameters:
                return False, f"autonomous planner cannot set approval parameter '{key}'"

    process = str(parameters.get("process") or parameters.get("name") or "").strip()
    protected = {str(p).lower() for p in PROTECTED_PROCESSES}
    if process.lower() in protected and action in PROCESS_ACTIONS:
        return False, f"protected process: {process}"

    for key in ("path", "file", "folder", "target"):
        value = parameters.get(key)
        if not isinstance(value, str) or not value.strip():
            continue
        if action in DESTRUCTIVE_PATH_ACTIONS and _protected_path(value):
            return False, f"protected system path: {value}"

    if action == "format_drive":
        value = str(parameters.get("path") or parameters.get("drive") or "").strip()
        if not value:
            return False, "format_drive requires an explicit drive/path"

    return True, "allowed"
