"""Windows-only direct system controls for Mark-LIV."""
import os, platform, shutil, subprocess, tempfile
from core import confirm
try:
    from core.permissions import needs_confirmation
except Exception:
    def needs_confirmation(action: str, *, admin: bool=False): return admin
WIN=platform.system()=="Windows"
HIDE={"creationflags":subprocess.CREATE_NO_WINDOW} if WIN else {}
def ps(cmd,timeout=20):
    return subprocess.run(["powershell","-NoProfile","-NonInteractive","-Command",cmd],capture_output=True,text=True,timeout=timeout,**HIDE)
def _reset():
    subprocess.run(["ipconfig","/flushdns"],capture_output=True,**HIDE)
    subprocess.run(["netsh","winsock","reset"],capture_output=True,**HIDE)
    return "Network reset completed; restart Windows if required."
def _service(cmd,name):
    safe=name.replace("'","''")
    r=ps(f"{cmd} -Name '{safe}' -ErrorAction Stop")
    return r.stdout.strip() or f"{cmd} completed for {name}."
def system_control(parameters=None,**kwargs):
    if not WIN:return "This action is Windows-only."
    p=parameters or {}; a=str(p.get("action","status")).lower().strip(); v=str(p.get("value","")).strip()
    if a=="status":
        r=ps("Get-CimInstance Win32_OperatingSystem | Select Caption,Version,LastBootUpTime | Format-List")
        return r.stdout.strip() or "Windows status unavailable."
    if a=="power_plan":
        plans={"balanced":"381b4222-f694-41f0-9685-ff5bb260df2e","high_performance":"8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c","power_saver":"a1841308-3541-4fab-bc81-f71556f20b4a"}
        k=v.lower() or "balanced"; g=plans.get(k)
        if not g:return "Use balanced, high_performance or power_saver."
        subprocess.run(["powercfg","/setactive",g],capture_output=True,**HIDE); return f"Power plan set to {k}."
    if a in ("sleep_timeout","display_timeout"):
        try:m=max(0,int(v or ("30" if a=="sleep_timeout" else "15")))
        except ValueError:return "Value must be minutes."
        cmd="standby-timeout-ac" if a=="sleep_timeout" else "monitor-timeout-ac"
        subprocess.run(["powercfg","/change",cmd,str(m)],capture_output=True,**HIDE)
        return f"{a} set to {m} minutes."
    if a=="temp_cleanup":
        root=tempfile.gettempdir(); n=0
        for x in os.listdir(root):
            q=os.path.join(root,x)
            try:
                shutil.rmtree(q,ignore_errors=True) if os.path.isdir(q) else os.remove(q); n+=1
            except Exception:pass
        return f"Temporary cleanup processed {n} items."
    if a=="dns_flush":
        r=subprocess.run(["ipconfig","/flushdns"],capture_output=True,text=True,**HIDE); return r.stdout.strip() or r.stderr.strip() or "DNS flush completed."
    if a=="network_reset":
        if confirm.pending_title():return "There is already a confirmation waiting."
        return confirm.request(key="system_control:network_reset",title="Allow network reset?",detail="Network connectivity may be interrupted.",run=_reset)
    if a=="startup_list":
        r=ps("Get-CimInstance Win32_StartupCommand | Select Name,Command,Location | Format-Table -AutoSize | Out-String"); return r.stdout.strip() or "No startup entries."
    if a=="services_list":
        r=ps("Get-Service | Sort Status,DisplayName | Select Status,Name,DisplayName | Format-Table -AutoSize | Out-String"); return r.stdout.strip() or "No services."
    if a in ("service_start","service_stop","service_restart"):
        if not v:return "Service name required."
        cmd={"service_start":"Start-Service","service_stop":"Stop-Service","service_restart":"Restart-Service"}[a]
        if confirm.pending_title():return "There is already a confirmation waiting."
        return confirm.request(key=f"system_control:{a}",title="Allow Windows service change?",detail=f"{a}: {v}",run=lambda:_service(cmd,v))
    if a in ("wifi_on","wifi_off"):
        cmd="Enable-NetAdapter" if a=="wifi_on" else "Disable-NetAdapter"
        ps(f"Get-NetAdapter -Physical | Where-Object {{$_.Name -match 'Wi-Fi|Wireless'}} | {cmd} -Confirm:$false")
        return f"Wi-Fi {a[4:]} requested."
    if a=="bluetooth":
        on=v.lower() in ("on","1","true","enable","enabled")
        cmd="Enable-PnpDevice" if on else "Disable-PnpDevice"
        ps(f"Get-PnpDevice -Class Bluetooth | {cmd} -Confirm:$false")
        return "Bluetooth state change requested."
    return "Use status, power_plan, sleep_timeout, display_timeout, temp_cleanup, dns_flush, network_reset, startup_list, services_list, service_start, service_stop, service_restart, wifi_on, wifi_off or bluetooth."
TOOL={"name":"system_control","description":"Windows-only direct system controls: power, timeouts, temp cleanup, DNS/network reset, startup/services, Wi-Fi and Bluetooth.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","description":"status | power_plan | sleep_timeout | display_timeout | temp_cleanup | dns_flush | network_reset | startup_list | services_list | service_start | service_stop | service_restart | wifi_on | wifi_off | bluetooth"},"value":{"type":"STRING","description":"Minutes, power plan, service name, or Bluetooth on/off."}},"required":["action"]},"handler":system_control}
