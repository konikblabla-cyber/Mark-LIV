"""Windows package management through the official winget client."""
import platform,subprocess
if platform.system()!="Windows": raise RuntimeError("Windows-only.")
def _run(args,timeout=120):
 r=subprocess.run(["winget.exe",*args],capture_output=True,text=True,timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
 return (r.stdout or r.stderr or f"winget exit code {r.returncode}")[:8000]
def windows_package_manager(parameters=None,**kwargs):
 p=parameters or {}; a=str(p.get("action","search")).lower().strip(); q=str(p.get("query") or p.get("id") or "").strip()
 if a not in ("search","list","install","upgrade","uninstall"): return "Action must be search, list, install, upgrade, or uninstall."
 if a=="list": return _run(["list"])
 if not q and a!="upgrade": return "Package name or ID required."
 if a=="search": return _run(["search","--query",q])
 if a=="install": return _run(["install","--id",q,"--exact","--accept-source-agreements","--accept-package-agreements"])
 if a=="uninstall": return _run(["uninstall","--id",q,"--exact"])
 if a=="upgrade": return _run(["upgrade","--id",q,"--exact"] if q else ["upgrade","--all"])
TOOL={"name":"windows_package_manager","description":"Windows software package management via winget: search/list/install/upgrade/uninstall. Install, upgrade and uninstall are system-changing operations and should use the normal Mark-LIV confirmation policy.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING"},"query":{"type":"STRING"},"id":{"type":"STRING"}},"required":["action"]},"handler":windows_package_manager}
