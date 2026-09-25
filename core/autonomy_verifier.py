"""Verification and recovery primitives for JARVIS autonomy."""
from __future__ import annotations

from typing import Any


def result_success(result: Any) -> bool:
    if isinstance(result, dict):
        return bool(result.get("ok", False))
    text = str(result or "").strip().lower()
    if "[confirmation_pending]" in text:
        return True
    bad = ("failed", "error:", "not available", "unknown tool",
           "permission denied", "exception", "traceback")
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


def recovery_hint(action: str, result: Any) -> str:
    return (
        f"The action '{action}' did not satisfy its expected result. "
        f"Inspect the current state and choose a different available action; "
        f"do not blindly repeat it. Previous result: {str(result)[:1000]}"
    )
