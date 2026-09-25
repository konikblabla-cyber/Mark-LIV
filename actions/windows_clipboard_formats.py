"""Windows clipboard format inspection without reading clipboard contents."""
import platform,ctypes
if platform.system()!="Windows":raise RuntimeError("Windows-only.")
def windows_clipboard_formats(parameters=None,**kwargs):
 u=ctypes.windll.user32; out=[]
 if not u.OpenClipboard(0):return "Clipboard is unavailable."
 try:
  f=0
  while True:
   f=u.EnumClipboardFormats(f)
   if not f:break
   out.append(str(f))
 finally:u.CloseClipboard()
 return "Formats present: "+(", ".join(out) if out else "none")
TOOL={"name":"windows_clipboard_formats","description":"Read-only Windows clipboard format inspection; reports formats only and never returns clipboard contents.","parameters":{"type":"OBJECT","properties":{}},"handler=windows_clipboard_formats}
