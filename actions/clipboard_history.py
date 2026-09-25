"""Windows-only local clipboard history for Mark-LIV."""
import platform,ctypes,time
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
_hist=[]
def _get():
 u=ctypes.windll.user32
 if not u.OpenClipboard(0): return ""
 h=u.GetClipboardData(13)
 if not h:return ""
 p=ctypes.windll.kernel32.GlobalLock(h)
 try:return ctypes.wstring_at(p) if p else ""
 finally:
  if p:ctypes.windll.kernel32.GlobalUnlock(h)
def clipboard_history(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","list")).lower().strip()
 if a=="capture":
  v=_get()
  if v and (not _hist or _hist[-1]!=v): _hist.append(v); del _hist[:-20]
  return f"Captured {len(v)} characters." if v else "Clipboard has no text."
 if a=="clear": _hist.clear(); return "Clipboard history cleared."
 if a=="list": return "\n\n".join(f"{i+1}. {v[:500]}" for i,v in enumerate(reversed(_hist))) or "Clipboard history is empty."
 return "Unknown clipboard_history action."
TOOL={"name":"clipboard_history","description":"Windows-only local text clipboard history: capture current clipboard, list up to 20 recent entries, or clear local history. Values are not sent anywhere by this action.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"}},"required":["action"]},"handler":clipboard_history}
