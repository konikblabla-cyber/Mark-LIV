"""Read-only Windows file association lookup."""
import platform,winreg
def windows_file_association_info(parameters=None,**kwargs):
 if platform.system()!="Windows": return "Windows-only action."
 ext=str((parameters or {}).get("extension") or "").strip().lower()
 if not ext:return "Missing extension, e.g. .pdf"
 if not ext.startswith("."):ext="."+ext
 try:
  with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,ext) as k: prog=winreg.QueryValueEx(k,"")[0]
  return f"{ext} -> {prog}"
 except OSError:return f"No association found for {ext}."
TOOL={"name":"windows_file_association_info","description":"Read-only lookup of the Windows file association for an extension.","parameters":{"type":"OBJECT","properties":{"extension":{"type":"STRING"}},"required":["extension"]},"handler":windows_file_association_info}
