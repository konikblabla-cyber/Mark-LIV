"""Optional central JARVIS permission policy.

If this file exists, actions use it to decide which operations need a human
confirmation. If it is removed, actions continue working without this layer.
"""

REQUIRE_CONFIRMATION = {
    "shutdown", "restart", "toggle_wifi", "close_all_apps", "close_active",
    "delete_file", "delete_folder", "kill_process", "terminate_process",
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
    return admin or name in REQUIRE_CONFIRMATION or name in REQUIRE_ADMIN_CONFIRMATION

def is_protected_process(name: str) -> bool:
    return str(name or "").strip().lower() in {p.lower() for p in PROTECTED_PROCESSES}
