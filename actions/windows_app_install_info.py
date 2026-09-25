"""Read-only Windows application installation inventory."""
import platform,winreg
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
ROOTS=[(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),(winreg.HKEY_CURRENT_USER,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")]
def windows_app_install_info(parameters=None,**kwargs):
 out=[]
 for root,path in ROOTS:
  try:k=winreg.OpenKey(root,path)
  except OSError:continue
  try:
   for i in range(winreg.QueryInfoKey(k)[0]):
    try:
     s=winreg.OpenKey(k,winreg.EnumKey(k,i)); name=winreg.QueryValueEx(s,"DisplayName")[0]
     ver=winreg.QueryValueEx(s,"DisplayVersion")[0] if _has(s,"DisplayVersion") else ""
     if name: out.append(f"{name} | {ver}")
    except OSError: pass
  finally:winreg.CloseKey(k)
 return "\n".join(sorted(set(out),key=str.lower)[:500]) or "No installed application entries found."
def _has(k,n):
 try:winreg.QueryValueEx(k,n);return True
 except OSError:return False
TOOL={"name":"windows_app_install_info","description":"Read-only inventory of Windows installed applications and versions from uninstall registry entries.","parameters":{"type":"OBJECT","properties":{}},"handler":windows_app_install_info}
