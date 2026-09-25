"""Windows utility actions for Mark-LIV. No UI changes; capability-only module."""
import platform
import subprocess

_WIN_HIDE = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def _ps(command):
    p = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True, creationflags=_WIN_HIDE)
    return p.stdout.strip() or p.stderr.strip() or "No output."


def windows_utilities_action(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows":
        return "This action is Windows-only."
    action = str(action or "").strip().lower()
    value = str(value or "").strip()
    if action == "windows_version":
        return _ps("Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsBuildNumber,OsArchitecture | Format-List")
    if action == "system_uptime":
        return _ps("$os=Get-CimInstance Win32_OperatingSystem; $u=(Get-Date)-$os.LastBootUpTime; [pscustomobject]@{LastBoot=$os.LastBootUpTime;Uptime=(''{0}d {1}h {2}m'' -f $u.Days,$u.Hours,$u.Minutes)} | Format-List")
    if action == "windows_locale":
        return _ps("Get-Culture | Select-Object Name,DisplayName,DateTimeFormat | Format-List")
    if action == "windows_notification":
        if not value:
            return "Notification text required."
        safe=value.replace("'","''")
        return _ps("[Windows.UI.Notifications.ToastNotificationManager,Windows.UI.Notifications,ContentType=WindowsRuntime] > $null; [Windows.Data.Xml.Dom.XmlDocument,Windows.Data.Xml.Dom,ContentType=WindowsRuntime] > $null; $xml=New-Object Windows.Data.Xml.Dom.XmlDocument; $xml.LoadXml('<toast><visual><binding template=\"ToastText02\"><text>Mark-LIV</text><text>"+safe+"</text></binding></visual></toast>'); $t=[Windows.UI.Notifications.ToastNotification]::new($xml); [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Mark-LIV').Show($t); 'Notification sent.'")
    return None


TOOL = {
    "name": "windows_utilities",
    "description": "Windows-only utility actions: inspect Windows version, system uptime, locale, and send a local desktop notification.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["windows_version", "system_uptime", "windows_locale", "windows_notification"]},
            "value": {"type": "string"},
            "needs_confirmation": {"type": "boolean"}
        },
        "required": ["action"]
    },
    "handler": windows_utilities_action
}
