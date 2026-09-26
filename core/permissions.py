"""Central JARVIS permission policy for risky operations."""
from __future__ import annotations

import ntpath

REQUIRE_CONFIRMATION = {
    "shutdown", "restart", "toggle_wifi", "close_all_apps", "close_active",
    "launch", "open_file",
    "delete_file", "delete_folder", "kill_process", "terminate_process",
    "close_process", "storage_cleanup_confirmed",
    "format_drive", "change_firewall", "change_security_setting",
    "install_software", "uninstall_software", "run_as_admin",
    "execute_admin_command",
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


def needs_confirmation(action: str, *, admin: bool = False) -> bool:
    name = str(action or "").strip().lower()
    if admin or name in REQUIRE_CONFIRMATION or name in REQUIRE_ADMIN_CONFIRMATION:
        return True
    risky_markers = (
        "delete", "remove", "uninstall", "format", "shutdown", "restart",
        "kill", "terminate", "firewall", "security", "admin",
    )
    return any(marker in name for marker in risky_markers)


def is_protected_process(name: str) -> bool:
    raw = str(name or "").strip().lower()
    if not raw:
        return False
    # Accept executable paths as well as bare process names, preventing a
    # protected process from being disguised as e.g. C:\Windows\System32\lsass.exe.
    basename = ntpath.basename(raw.rstrip("\/"))
    protected = {p.lower() for p in PROTECTED_PROCESSES}
    return raw in protected or basename in protected
