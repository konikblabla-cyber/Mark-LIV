"""Local semantic screen understanding without sending screenshots to Gemini.

Uses Windows UI Automation (UIA) when available. This gives JARVIS a cheap,
structured view of the active window: control names, roles, values and bounds.
It is intentionally read-only.
"""
from __future__ import annotations

import platform

_MAX_CONTROLS = 120


def screen_understanding(parameters=None, **kwargs):
    if platform.system() != "Windows":
        return "Local screen understanding is currently Windows-only."

    p = parameters or {}
    try:
        max_controls = max(10, min(int(p.get("max_controls", _MAX_CONTROLS)), _MAX_CONTROLS))
    except (TypeError, ValueError):
        max_controls = _MAX_CONTROLS

    try:
        from pywinauto import Desktop
    except ImportError:
        return "UI Automation unavailable: pywinauto is not installed."

    try:
        desktop = Desktop(backend="uia")
        window = desktop.get_active()
        if window is None:
            return "No active window found."

        info = window.element_info
        title = (window.window_text() or "").strip()
        control_type = getattr(info, "control_type", "") or "Window"
        lines = [
            f"ACTIVE WINDOW: {title or '(untitled)'}",
            f"TYPE: {control_type}",
        ]

        try:
            rect = window.rectangle()
            lines.append(f"BOUNDS: {rect.left},{rect.top},{rect.right},{rect.bottom}")
        except Exception:
            pass

        try:
            controls = window.descendants()
        except Exception:
            controls = []

        count = 0
        for ctrl in controls:
            if count >= max_controls:
                break
            try:
                ci = ctrl.element_info
                name = (ctrl.window_text() or getattr(ci, "name", "") or "").strip()
                ctype = (getattr(ci, "control_type", "") or "").strip()
                if not name and not ctype:
                    continue

                # Skip invisible/non-rendered elements when UIA exposes the flag.
                try:
                    if hasattr(ctrl, "is_visible") and not ctrl.is_visible():
                        continue
                except Exception:
                    pass

                value = ""
                try:
                    value = str(ctrl.get_value()).strip()
                except Exception:
                    pass

                bounds = ""
                try:
                    r = ctrl.rectangle()
                    bounds = f" [{r.left},{r.top},{r.right},{r.bottom}]"
                except Exception:
                    pass

                text = name or "(unnamed)"
                if value and value != name:
                    text += f" = {value[:180]}"
                lines.append(f"- {ctype or 'Control'}: {text[:240]}{bounds}")
                count += 1
            except Exception:
                continue

        if count == 0:
            lines.append("- No readable UI controls exposed by UI Automation.")
        else:
            lines.append(f"CONTROLS: {count}")

        return "\n".join(lines)[:18000]
    except Exception as exc:
        return f"Screen understanding failed: {type(exc).__name__}: {exc}"


TOOL = {
    "name": "screen_understanding",
    "description": (
        "Read-only Windows screen understanding using local UI Automation. "
        "Returns the active window and visible UI controls with names, roles, "
        "values and coordinates without sending a screenshot to Gemini. "
        "Use before screenshot vision when structured UI information is enough."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "max_controls": {
                "type": "INTEGER",
                "description": "Maximum UI controls to return (10-120)."
            }
        }
    },
    "handler": screen_understanding,
}
