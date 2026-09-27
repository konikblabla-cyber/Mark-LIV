"""Central JARVIS permission policy for Windows operations.

Access levels:
READ      -> read-only/inspection actions
NORMAL    -> normal local changes; risky actions require confirmation
ELEVATED  -> privileged/admin actions may be requested, but confirmation remains required
CRITICAL  -> unrestricted normal control; hard-dangerous actions still require confirmation
"""
from __future__ import annotations

import ntpath
import os
import re

CONTROL_LEVELS = ("READ", "NORMAL", "ELEVATED", "CRITICAL")
DEFAULT_CONTROL_LEVEL = "NORMAL"

FULL_CONTROL = os.environ.get("JARVIS_FULL_CONTROL", "0").strip().lower() in {"1", "true", "yes", "on"}

HARD_CONFIRM_ACTIONS = {
    "format_drive", "change_security_setting", "execute_admin_command",
    "run_as_admin", "change_firewall",
}

REQUIRE_CONFIRMATION = {
    "shutdown", "restart", "toggle_wifi", "close_all_apps", "close_active",
    "launch", "open_file", "delete_file", "delete_folder", "kill_process",
    "terminate_process", "close_process", "storage_cleanup_confirmed",
    "format_drive", "change_firewall", "change_security_setting",
    "install_software", "uninstall_software", "run_as_admin",
    "execute_admin_command", "autostart_enable", "autostart_disable",
}

REQUIRE_ADMIN_CONFIRMATION = {
    "run_as_admin", "execute_admin_command", "change_firewall",
    "change_security_setting", "format_drive",
}

PROTECTED_PROCESSES = {
    "System", "Registry", "smss.exe", "csrss.exe", "wininit.exe",
    "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe",
    "dwm.exe", "explorer.exe",
}

_READ_MARKERS = (
    "get_", "list", "read", "inspect", "search", "status", "show",
    "info", "find", "query", "check", "calculate", "monitor", "snapshot", "screenshot",
)
_WRITE_MARKERS = (
    "open", "launch", "close", "move", "resize", "minimize", "maximize",
    "restore", "focus", "click", "type", "press", "write", "create",
    "edit", "copy", "rename", "install", "toggle", "set_", "save",
    "download", "upload", "send", "volume", "audio", "wifi", "route",
    "arp", "dns", "service", "registry", "lock", "close_camera",
)
_HIGH_MARKERS = (
    "delete", "remove", "uninstall", "format", "shutdown", "restart",
    "kill", "terminate", "firewall", "security", "admin",
)


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
    if name in HARD_CONFIRM_ACTIONS or name in REQUIRE_CONFIRMATION:
        return "high"
    if any(marker in name for marker in _HIGH_MARKERS):
        return "high"
    if any(marker in name for marker in _WRITE_MARKERS):
        return "medium"
    if any(name.startswith(marker) for marker in _READ_MARKERS):
        return "low"
    # Unknown actions are conservative: they may have side effects even when
    # their name does not match a known read/write marker.
    return "high"


def permission_decision(action: str, parameters: dict | None = None) -> tuple[str, str]:
    """Return ('allow'|'confirm'|'deny', reason)."""
    name = str(action or "").strip().lower()
    params = parameters if isinstance(parameters, dict) else {}
    level = get_control_level()
    risk = _risk(name)

    admin_requested = bool(params.get("admin") or params.get("elevated"))
    command = params.get("command")
    if isinstance(command, str) and command_needs_admin(command):
        admin_requested = True
    if admin_requested:
        if level not in {"ELEVATED", "CRITICAL"}:
            return "deny", "ELEVATED or CRITICAL access is required for privileged operations"
        return "confirm", f"{level}: explicit privileged operation requires confirmation"

    if risk == "low":
        return "allow", f"{level}: read-only operation"

    if level == "READ":
        return "deny", "READ level allows only read/inspection operations"

    if name in HARD_CONFIRM_ACTIONS or risk == "high":
        return "confirm", f"{level}: confirmation required for consequential operation"

    return "allow", f"{level}: normal operation"


def needs_confirmation(action: str, *, admin: bool = False) -> bool:
    """Return whether execution must pass through a confirmation boundary.

    An explicit admin request always requires confirmation, even when the
    current access level would ultimately deny the operation.  This keeps the
    confirmation predicate faithful to the requested privilege while
    permission_decision remains the final execution gate.
    """
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
    if executable in {"bcdedit", "dism", "diskpart", "takeown", "manage-bde"}:
        return True
    if executable == "sc":
        return bool(re.search(r"\b(create|config|delete|start|stop|failure|sdset|sdshow)\b", normalized))
    if executable == "reg":
        return bool(re.search(r"\b(add|delete|import|load|unload)\b", normalized))
    if executable == "netsh":
        return bool(re.search(r"\b(advfirewall|firewall|wlan|interface portproxy|winsock)\b", normalized))
    if executable == "net":
        return bool(re.search(r"\b(user|localgroup|share|session|start|stop)\b", normalized))
    if executable in {"wevtutil", "auditpol"}:
        return True
    return False


def admin_requirement_reason(command: str = "", output: str = "") -> str | None:
    """Return a short reason when an operation needs Windows elevation."""
    if command_needs_admin(command):
        return "This Windows operation requires administrator privileges."
    if is_admin_failure(output):
        return "Windows reported that administrator privileges are required."
    return None


def is_admin_failure(output: str) -> bool:
    text = str(output or "").lower()
    markers = (
        "access is denied", "access denied", "requested operation requires elevation",
        "requires elevation", "requires administrator", "elevation required",
        "error: 5", "error 5",
    )
    return any(marker in text for marker in markers)


def is_protected_process(name: str) -> bool:
    raw = str(name or "").strip().lower()
    if not raw:
        return False
    basename = ntpath.basename(raw.rstrip("\\/"))
    protected = {p.lower() for p in PROTECTED_PROCESSES}
    return raw in protected or basename in protected
