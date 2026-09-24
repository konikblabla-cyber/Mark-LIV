import subprocess
import platform
from core import confirm

_OS = platform.system()

_PROTECTED = {
    "explorer.exe", "dwm.exe", "csrss.exe", "winlogon.exe",
    "services.exe", "lsass.exe", "smss.exe", "System", "Registry"
}

def _close_all_windows():
    if _OS != "Windows":
        return "This action currently supports Windows only."

    # Ask Windows to close normal foreground applications gracefully.
    ps = r'''
$ErrorActionPreference = "SilentlyContinue"
$protected = @("explorer","dwm","csrss","winlogon","services","lsass","smss","System","Registry","svchost")
Get-Process | Where-Object {
    $_.MainWindowHandle -ne 0 -and
    $protected -notcontains $_.ProcessName
} | ForEach-Object {
    $_.CloseMainWindow() | Out-Null
}
'''
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        capture_output=True, text=True, timeout=15,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    return "Requested graceful close for all normal application windows."

def close_all_apps(parameters=None, response=None, player=None, session_memory=None):
    if _OS != "Windows":
        return "Close-all-apps is currently implemented for Windows only."

    if confirm.pending_title():
        return "There is already a confirmation waiting on screen. Ask the user to answer it first."

    return confirm.request(
        key="close_all_apps",
        title="Close all open applications?",
        detail="JARVIS will ask normal Windows applications to close. Unsaved work may prompt inside those apps.",
        run=_close_all_windows,
    )

TOOL = {
    "name": "close_all_apps",
    "description": "Close all normal user applications on Windows. Requires an explicit human confirmation button before anything is closed. Does not target protected Windows system processes.",
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": []
    },
    "handler": close_all_apps,
}
