"""
core/permissions.py — central JARVIS permission policy.

Keep permission decisions in this one file so actions do not each invent their
own security rules. Normal reversible actions run immediately; risky,
destructive, privacy-sensitive, or administrator-level actions require the
human confirmation UI in core.confirm.

This is a policy/configuration module, not an OpenAI-security bypass.
"""

# Actions that must wait for an explicit human click in the JARVIS HUD.
# Add a new action here instead of scattering permission checks across actions.
REQUIRE_CONFIRMATION = {
    "shutdown",
    "restart",
    "toggle_wifi",
    "close_all_apps",
    "delete_file",
    "delete_folder",
    "kill_process",
    "terminate_process",
    "format_drive",
    "change_firewall",
    "change_security_setting",
    "install_software",
    "uninstall_software",
    "run_as_admin",
    "execute_admin_command",
}

# Operations that should be treated as administrator-level even if an action
# forgets to classify them explicitly.
REQUIRE_ADMIN_CONFIRMATION = {
    "run_as_admin",
    "execute_admin_command",
    "change_firewall",
    "change_security_setting",
    "format_drive",
}

# Never silently allow these through a generic "close/kill everything" action.
PROTECTED_PROCESSES = {
    "System",
    "Registry",
    "smss.exe",
    "csrss.exe",
    "wininit.exe",
    "winlogon.exe",
    "services.exe",
    "lsass.exe",
    "svchost.exe",
    "dwm.exe",
    "explorer.exe",
}

def needs_confirmation(action: str, *, admin: bool = False) -> bool:
    name = str(action or "").strip().lower()
    return admin or name in REQUIRE_CONFIRMATION or name in REQUIRE_ADMIN_CONFIRMATION

def is_protected_process(name: str) -> bool:
    return str(name or "").strip().lower() in {
        p.lower() for p in PROTECTED_PROCESSES
    }
