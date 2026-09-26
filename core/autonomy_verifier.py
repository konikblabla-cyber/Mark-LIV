"""Verification and recovery primitives for JARVIS autonomy."""
from __future__ import annotations

import ntpath
from pathlib import Path
from typing import Any

import psutil


def result_success(result: Any) -> bool:
    if isinstance(result, dict):
        return bool(result.get("ok", False))
    text = str(result or "").strip().lower()
    if "[confirmation_pending]" in text:
        return True
    bad = (
        "failed", "error:", "not available", "unknown tool",
        "permission denied", "exception", "traceback",
    )
    return not any(x in text for x in bad)


def verify_text(result: Any, expectation: str) -> bool:
    """Conservative semantic verification using deterministic text checks."""
    if not result_success(result):
        return False
    if not expectation:
        return True
    haystack = str(result or "").lower()
    wanted = [x.strip().lower() for x in expectation.split("|") if x.strip()]
    return not wanted or any(x in haystack for x in wanted)


def _process_name_matches(actual: str, requested: str) -> bool:
    actual_name = ntpath.basename(str(actual or "").strip().rstrip("\/")).lower()
    requested_name = ntpath.basename(str(requested or "").strip().rstrip("\/")).lower()
    return bool(requested_name) and actual_name == requested_name


def verify_state(
    action: str,
    parameters: dict | None = None,
    result: Any = None,
) -> bool:
    """Verify common high-impact actions against actual local state when possible."""
    p = parameters or {}
    if "[confirmation_pending]" in str(result or "").lower():
        return True
    try:
        if action in {"delete_file", "delete_folder"}:
            path = p.get("path") or p.get("file_path") or p.get("folder_path")
            return bool(path) and not Path(str(path)).exists()

        if action in {"kill_process", "terminate_process"}:
            pid = p.get("pid")
            return bool(pid) and not psutil.pid_exists(int(pid))

        if action == "move_file":
            src = p.get("source") or p.get("src")
            dst = p.get("destination") or p.get("dst")
            return bool(src and dst) and not Path(str(src)).exists() and Path(str(dst)).exists()

        if action == "copy_file":
            src = p.get("source") or p.get("src")
            dst = p.get("destination") or p.get("dst")
            return bool(src and dst) and Path(str(src)).exists() and Path(str(dst)).exists()

        if action in {"create_file", "write_file"}:
            path = p.get("path") or p.get("file_path") or p.get("destination")
            return bool(path) and Path(str(path)).exists()

        if action == "rename_file":
            src = p.get("source") or p.get("src")
            dst = p.get("destination") or p.get("dst")
            return bool(src and dst) and not Path(str(src)).exists() and Path(str(dst)).exists()

        if action in {"close_process", "close_active"}:
            pid = p.get("pid")
            if pid is not None:
                return not psutil.pid_exists(int(pid))
            name = str(
                p.get("name")
                or p.get("process")
                or p.get("process_name")
                or ""
            ).strip()
            if name:
                return not any(
                    _process_name_matches(proc.info.get("name"), name)
                    for proc in psutil.process_iter(["name"])
                )
            return result_success(result)

        return result_success(result)
    except (OSError, ValueError, TypeError):
        return False


def recovery_hint(action: str, result: Any) -> str:
    return (
        f"The action '{action}' did not satisfy its expected result. "
        f"Inspect the current state and choose a different available action; "
        f"do not blindly repeat it. Previous result: {str(result)[:1000]}"
    )
