"""Windows toast notification action."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def windows_notification_action(parameters=None,**kwargs):
 p=parameters or {}; title=str(p.get("title","Mark-LIV")).strip()[:120]; message=str(p.get("message","")).strip()[:500]
 if not message:return "Message is required."
 t=title.replace("'","''");m=message.replace("'","''")
 ps=f'''[Windows.UI.Notifications.ToastNotificationManager,Windows.UI.Notifications,ContentType=WindowsRuntime] > $null; $xml=[Windows.Data.Xml.Dom.XmlDocument,Windows.Data.Xml.Dom.XmlDocument,ContentType=WindowsRuntime]::new();$xml.LoadXml('<toast><visual><binding template="ToastGeneric"><text>{t}</text><text>{m}</text></binding></visual></toast>');$toast=[Windows.UI.Notifications.ToastNotification]::new($xml);[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Mark-LIV').Show($toast)'''
 r=subprocess.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",ps],capture_output=True,text=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
 return "Notification sent." if r.returncode==0 else (r.stderr or "Notification failed.")
TOOL={"name":"windows_notification_action","description":"Show a local Windows toast notification from Mark-LIV.","parameters":{"type":"OBJECT","properties":{"title":{"type":"STRING"},"message":{"type":"STRING"}},"required":["message"]},"handler":windows_notification_action}
