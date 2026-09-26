"""Safety guardrails for autonomous planning."""
from __future__ import annotations
import os
from typing import Any
from core.permissions import needs_confirmation, PROTECTED_PROCESSES

PROTECTED_PATHS = {
    os.path.normcase(os.environ.get("WINDIR", r"C:\Windows")),
    os.path.normcase(os.environ.get("PROGRAMFILES", r"C:\Program Files")),
    os.path.normcase(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")),
}

def validate_step(action: str, parameters: dict[str, Any]) -> tuple[bool, str]:
    if not action:
        return False, "empty action"
    if not isinstance(parameters, dict):
        return False, "invalid parameters"

    # Autonomous planning can request destructive actions, but can never
    # smuggle human approval through parameters.
    if needs_confirmation(action):
        for key in ("confirmed", "confirm", "approved", "force_confirm"):
            if key in parameters:
                return False, f"autonomous planner cannot set approval parameter '{key}'"

    process = str(parameters.get("process") or parameters.get("name") or "")
    protected = {p.lower() for p in PROTECTED_PROCESSES}
    if process.lower() in protected:
        if action in {"kill_process", "terminate_process", "close_active"}:
            return False, f"protected process: {process}"

    for key in ("path", "file", "folder", "target"):
        value = parameters.get(key)
        if not isinstance(value, str) or not value:
            continue
        try:
            normalized = os.path.normcase(os.path.abspath(os.path.expandvars(value)))
        except Exception:
            continue
        for protected in PROTECTED_PATHS:
            if normalized == protected or normalized.startswith(protected + os.sep):
                if action in {"delete_file", "delete_folder", "format_drive"}:
                    return False, f"protected system path: {value}"

    if action == "format_drive":
        drive = str(parameters.get("drive") or parameters.get("path") or parameters.get("target") or "")
        if not drive:
            return False, "format_drive requires an explicit drive/path"
    return True, ""

def audit_plan(steps) -> list[str]:
    problems = []
    for i, step in enumerate(steps, 1):
        ok, reason = validate_step(step.action, step.parameters)
        if not ok:
            problems.append(f"step {i} ({step.action}): {reason}")
    return problems
