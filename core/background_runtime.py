"""Windows background/autostart support for Mark-LIV.

The UI is optional: the JARVIS process can remain alive in the tray and can
start automatically with the current Windows user.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

APP_NAME = "Mark-LIV JARVIS"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "Mark-LIV JARVIS"


def _startup_command() -> str:
    if getattr(sys, "frozen", False):
        return f'"{Path(sys.executable).resolve()}" --background'
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    interpreter = pythonw if pythonw.exists() else Path(sys.executable)
    return f'"{interpreter.resolve()}" "{Path(__file__).resolve().parents[1] / "main.py"}" --background'


def enable_autostart() -> bool:
    if os.name != "nt":
        return False
    try:
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_SZ, _startup_command())
        return True
    except Exception as exc:
        print(f"[Background] Autostart unavailable: {exc}")
        return False


def disable_autostart() -> bool:
    if os.name != "nt":
        return False
    try:
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE
        ) as key:
            try:
                winreg.DeleteValue(key, VALUE_NAME)
            except FileNotFoundError:
                pass
        return True
    except Exception as exc:
        print(f"[Background] Autostart removal failed: {exc}")
        return False


def autostart_enabled() -> bool:
    if os.name != "nt":
        return False
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, VALUE_NAME)
            return bool(value)
    except Exception:
        return False
