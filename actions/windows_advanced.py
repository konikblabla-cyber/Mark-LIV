"""Additional Windows-only read-only system actions for Mark-LIV."""
import json
import os
import platform
import subprocess

WIN = platform.system() == "Windows"
HIDE = {"creationflags": subprocess.CREATE_NO_WINDOW} if WIN else {}


def _ps(command, timeout=30):
    if not WIN:
        return "This action is Windows-only."
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True, text=True, timeout=timeout, **HIDE
        )
        return r.stdout.strip() or r.stderr.strip() or "No data returned."
    except Exception as exc:
        return f"Windows query failed: {exc}"


def windows_advanced_action(parameters=None, **kwargs):
    if not WIN:
        return "This action is Windows-only."
    p = parameters or {}
    action = str(p.get("action", "")).strip().lower()

    if action == "windows_share_list":
        return _ps(
            "Get-SmbShare | Select-Object Name,Path,Description,ScopeName,Special,EncryptData,FolderEnumerationMode "
            "| Sort-Object Name | ConvertTo-Json -Compress"
        )

    if action == "windows_share_sessions":
        return _ps(
            "$s=Get-SmbSession | Select-Object ClientComputerName,ClientUserName,NumOpens,SecondsIdle,SecondsExists,SessionId;"
            "$o=Get-SmbOpenFile | Select-Object ClientComputerName,ClientUserName,Path,ShareRelativePath,SessionId;"
            "[pscustomobject]@{Sessions=$s;OpenFiles=$o} | ConvertTo-Json -Compress"
        )

    if action == "windows_user_profile_info":
        return _ps(
            "$u=$env:USERNAME;"
            "$p=$env:USERPROFILE;"
            "$q=Get-CimInstance Win32_UserProfile | Where-Object LocalPath -eq $p | "
            "Select-Object LocalPath,Loaded,RoamingConfigured,Status;"
            "[pscustomobject]@{UserName=$u;UserProfile=$p;Profile=$q} | ConvertTo-Json -Compress"
        )

    if action == "windows_boot_recovery_status":
        return _ps(
            "$re=Get-ComputerInfo -Property WindowsBootDevice,WindowsSystemDevice,BiosFirmwareType,OsName,OsVersion;"
            "$b=Get-CimInstance Win32_ComputerSystem | Select-Object BootupState,SystemType;"
            "[pscustomobject]@{Computer=$re;Boot=$b} | ConvertTo-Json -Compress"
        )

    return None


TOOL = {
    "name": "windows_advanced",
    "description": (
        "Windows-only read-only system inspection. Actions: "
        "windows_share_list (SMB shares), windows_share_sessions (SMB sessions/open files), "
        "windows_user_profile_info (current Windows profile), "
        "windows_boot_recovery_status (boot/firmware/system boot status). "
        "These actions inspect the system and do not change settings."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "windows_share_list, windows_share_sessions, "
                    "windows_user_profile_info, windows_boot_recovery_status"
                ),
            }
        },
        "required": ["action"],
    },
    "handler": windows_advanced_action,
}
