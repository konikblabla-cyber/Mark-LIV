"""Single central JARVIS permission policy.

All action modules should ask this module before executing a controlled
operation.  CRITICAL enables autonomous normal computer control; Windows UAC
and OS-level security boundaries are still respected.
"""
from __future__ import annotations
import ntpath
import os
import re

CONTROL_LEVELS = ("READ", "NORMAL", "ELEVATED", "CRITICAL")
DEFAULT_CONTROL_LEVEL = "NORMAL"
FULL_CONTROL = os.environ.get("JARVIS_FULL_CONTROL", "0").strip().lower() in {"1", "true", "yes", "on"}

PROTECTED_PROCESSES = {"System", "Registry", "smss.exe", "csrss.exe", "wininit.exe", "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe", "dwm.exe", "explorer.exe"}
READ_MARKERS = ("get_", "list", "read", "inspect", "search", "status", "show", "info", "find", "query", "check", "calculate", "monitor", "snapshot", "screenshot")
WRITE_MARKERS = ("open", "launch", "close", "move", "resize", "minimize", "maximize", "restore", "focus", "click", "type", "press", "write", "create", "edit", "copy", "rename", "install", "toggle", "set_", "save", "download", "upload", "send", "volume", "audio", "wifi", "route", "arp", "dns", "service", "registry", "lock", "close_camera")
HIGH_MARKERS = ("delete", "remove", "uninstall", "format", "shutdown", "restart", "kill", "terminate", "firewall", "security", "admin")


def get_control_level() -> str:
    try:
        from memory.config_manager import get_control_level as _get
        value = str(_get() or DEFAULT_CONTROL_LEVEL).strip().upper()
    except Exception:
        value = DEFAULT_CONTROL_LEVEL
    if FULL_CONTROL:
        return "CRITICAL"
    return value if value in CONTROL_LEVELS else DEFAULT_CONTROL_LEVEL


def save_control_level(level: str) -> str:
    value = str(level or DEFAULT_CONTROL_LEVEL).strip().upper()
    if value not in CONTROL_LEVELS:
        value = DEFAULT_CONTROL_LEVEL
    try:
        from memory.config_manager import save_control_level as _save
        _save(value)
    except Exception:
        pass
    return value


def full_control_enabled() -> bool:
    return get_control_level() == "CRITICAL"


def _risk(action: str) -> str:
    name = str(action or "").strip().lower()
    if not name:
        return "high"
    if any(marker in name for marker in HIGH_MARKERS):
        return "high"
    if any(marker in name for marker in WRITE_MARKERS):
        return "medium"
    if any(name.startswith(marker) for marker in READ_MARKERS):
        return "low"
    return "high"


def permission_decision(action: str, parameters: dict | None = None) -> tuple[str, str]:
    """Central decision point: allow, confirm, or deny."""
    name = str(action or "").strip().lower()
    params = parameters if isinstance(parameters, dict) else {}
    level = get_control_level()

    # CRITICAL is the user's explicit autonomous-control mode. It removes
    # JARVIS confirmation prompts for normal computer operations.
    if level == "CRITICAL":
        return "allow", "CRITICAL: autonomous control"

    command = params.get("command")
    admin_requested = bool(params.get("admin") or params.get("elevated"))
    if isinstance(command, str) and command_needs_admin(command):
        admin_requested = True
    if admin_requested and level not in {"ELEVATED", "CRITICAL"}:
        return "deny", "ELEVATED or CRITICAL access is required"
    if admin_requested:
        return "confirm", f"{level}: privileged operation"

    risk = _risk(name)
    if risk == "low":
        return "allow", f"{level}: read-only operation"
    if level == "READ":
        return "deny", "READ level allows only inspection operations"
    if risk == "high":
        return "confirm", f"{level}: consequential operation"
    return "allow", f"{level}: normal operation"


def needs_confirmation(action: str, *, admin: bool = False) -> bool:
    if get_control_level() == "CRITICAL":
        return False
    if admin:
        return True
    decision, _ = permission_decision(action)
    return decision == "confirm"


def is_admin() -> bool:
    if os.name != "nt":
        return False
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError, ImportError):
        return False


def command_needs_admin(command: str) -> bool:
    raw = str(command or "").strip()
    if not raw or os.name != "nt":
        return False
    normalized = re.sub(r"\s+", " ", raw.lower()).strip()
    first = normalized.lstrip(' "').split(" ", 1)[0]
    executable = ntpath.basename(first)
    if executable.endswith(".exe"):
        executable = executable[:-4]
    if executable in {"bcdedit", "dism", "diskpart", "takeown", "manage-bde", "wevtutil", "auditpol"}:
        return True
    if executable == "sc":
        return bool(re.search(r"\b(create|config|delete|start|stop|failure|sdset|sdshow)\b", normalized))
    if executable == "reg":
        return bool(re.search(r"\b(add|delete|import|load|unload)\b", normalized))
    if executable == "netsh":
        return bool(re.search(r"\b(advfirewall|firewall|wlan|interface portproxy|winsock)\b", normalized))
    if executable == "net":
        return bool(re.search(r"\b(user|localgroup|share|session|start|stop)\b", normalized))
    return False


def admin_requirement_reason(command: str = "", output: str = "") -> str | None:
    if command_needs_admin(command):
        return "This Windows operation requires administrator privileges."
    if is_admin_failure(output):
        return "Windows reported that administrator privileges are required."
    return None


def is_admin_failure(output: str) -> bool:
    text = str(output or "").lower()
    return any(x in text for x in ("access is denied", "access denied", "requires elevation", "requires administrator", "elevation required", "error: 5", "error 5"))


def is_protected_process(name: str) -> bool:
    raw = str(name or "").strip().lower()
    basename = ntpath.basename(raw.rstrip("\\/"))
    protected = {p.lower() for p in PROTECTED_PROCESSES}
    return raw in protected or basename in protected
