"""Resolve executable names through Windows PATH."""
import platform,subprocess
def windows_app_aliases(parameters=None,**kwargs):
 names=(parameters or {}).get("names",[])
 if isinstance(names,str):names=[names]
 names=[str(x).strip() for x in names[:30] if str(x).strip()]
 if not names:return "Missing executable names."
 out=[]
 for n in names:
  try:
   r=subprocess.run(["where",n],capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=10,creationflags=0x08000000)
  except (subprocess.TimeoutExpired,OSError) as e:
   out.append(f"{n}: lookup failed: {e}"); continue
  out.append(f"{n}: {r.stdout.strip() or 'not found'}")
 return "\n".join(out)
TOOL={"name":"windows_app_aliases","description":"Resolve multiple executable names through the Windows PATH.","parameters":{"type":"OBJECT","properties":{"names":{"type":"ARRAY","items":{"type":"STRING"}}},"required":["names"]},"handler":windows_app_aliases}
