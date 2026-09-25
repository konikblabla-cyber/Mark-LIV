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

def _installed_apps():
    cmd = 'Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Where-Object DisplayName | Select-Object DisplayName,DisplayVersion,UninstallString | Sort-Object DisplayName | ConvertTo-Json -Compress'
    out = subprocess.run(["powershell","-NoProfile","-Command",cmd], capture_output=True, text=True, creationflags=_WIN_HIDE)
    return out.stdout.strip() or "[]"

def _exe_inventory():
    roots = [os.environ.get("ProgramFiles", ""), os.environ.get("ProgramFiles(x86)", ""), os.environ.get("LOCALAPPDATA", "")]
    found=[]
    for root in roots:
        if not root or not os.path.isdir(root): continue
        try:
            for base, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d.lower() not in {"windowsapps","packages","cache","temp"}]
                for f in files:
                    if f.lower().endswith(".exe"):
                        found.append(os.path.join(base,f))
        except (PermissionError,OSError): pass
    return found

def _system_control_extra(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    if action == "installed_apps": return _installed_apps()
    if action == "exe_inventory": return json.dumps(_exe_inventory(), ensure_ascii=False)
    if action == "app_uninstall":
        if not needs_confirmation: return "Uninstall requires confirmation."
        target = str(value or "").strip()
        if not target: return "Provide the exact installed app name."
        apps=json.loads(_installed_apps() or "[]")
        apps = apps if isinstance(apps,list) else [apps]
        match=next((a for a in apps if str(a.get("DisplayName","")).lower()==target.lower()),None)
        if not match: return "App not found. Use installed_apps first."
        cmd=match.get("UninstallString")
        if not cmd: return "No uninstall command is registered for this app."
        subprocess.Popen(["cmd","/c",cmd], creationflags=_WIN_HIDE)
        return f"Started uninstall for {match.get('DisplayName')}."
    return None



def analyze_exe_inventory():
    """Return metadata useful for deciding whether an EXE is likely unnecessary; never deletes anything."""
    rows=[]
    for p in _exe_inventory():
        try:
            st=os.stat(p)
            rows.append({"path":p,"size_mb":round(st.st_size/1048576,2),"modified":int(st.st_mtime)})
        except OSError: pass
    return rows

def analyze_exe(action):
    if action != "analyze_exe": return None
    rows=analyze_exe_inventory()
    return json.dumps({"count":len(rows),"executables":rows},ensure_ascii=False)

def process_tree():
    if platform.system() != "Windows": return "This action is Windows-only."
    cmd='Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,ExecutablePath | ConvertTo-Json -Compress'
    out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
    return out.stdout.strip() or "[]"


def windows_diagnostics(action):
    """Read-only Windows diagnostics; no settings are changed."""
    if platform.system() != "Windows": return "This action is Windows-only."
    commands={
      "scheduled_tasks": 'Get-ScheduledTask | Select-Object TaskName,TaskPath,State | ConvertTo-Json -Compress',
      "event_log": 'Get-WinEvent -LogName System -MaxEvents 30 | Select-Object TimeCreated,Id,LevelDisplayName,ProviderName,Message | ConvertTo-Json -Compress',
      "installed_drivers": 'Get-CimInstance Win32_PnPSignedDriver | Select-Object DeviceName,DriverVersion,Manufacturer,DriverDate | ConvertTo-Json -Compress',
      "environment_vars": 'Get-ChildItem Env: | Select-Object Name,Value | Sort-Object Name | ConvertTo-Json -Compress',
      "gpu_status": 'Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion,AdapterRAM,Status | ConvertTo-Json -Compress',
      "disk_health": 'Get-PhysicalDisk | Select-Object FriendlyName,MediaType,HealthStatus,OperationalStatus,Size | ConvertTo-Json -Compress',
      "defender_status": 'Get-MpComputerStatus | Select-Object AMServiceEnabled,AntivirusEnabled,RealTimeProtectionEnabled,AntispywareEnabled | ConvertTo-Json -Compress',
      "windows_updates": '(Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 30 HotFixID,InstalledOn,Description) | ConvertTo-Json -Compress'
    }
    cmd=commands.get(action)
    if not cmd: return None
    out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
    return out.stdout.strip() or out.stderr.strip() or "No data returned."


def windows_system_info(action):
    if platform.system() != "Windows": return "This action is Windows-only."
    commands={
      "network_adapters": 'Get-NetAdapter | Select-Object Name,InterfaceDescription,Status,LinkSpeed,MacAddress | ConvertTo-Json -Compress',
      "wifi_networks": 'netsh wlan show networks mode=bssid',
      "ip_config": 'Get-NetIPConfiguration | Select-Object InterfaceAlias,IPv4Address,IPv6Address,DNSServer | ConvertTo-Json -Compress',
      "firewall_status": 'Get-NetFirewallProfile | Select-Object Name,Enabled,DefaultInboundAction,DefaultOutboundAction | ConvertTo-Json -Compress',
      "bitlocker_status": 'Get-BitLockerVolume | Select-Object MountPoint,VolumeStatus,ProtectionStatus,EncryptionPercentage | ConvertTo-Json -Compress',
      "battery_status": 'Get-CimInstance Win32_Battery | Select-Object Name,EstimatedChargeRemaining,BatteryStatus | ConvertTo-Json -Compress',
      "windows_service_info": 'Get-Service | Select-Object Name,DisplayName,Status,StartType | Sort-Object Name | ConvertTo-Json -Compress'
    }
    cmd=commands.get(action)
    if not cmd: return None
    out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
    return out.stdout.strip() or out.stderr.strip() or "No data returned."


def windows_network_tools(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    if action == "proxy_status":
        return subprocess.run(["netsh","winhttp","show","proxy"],capture_output=True,text=True,creationflags=_WIN_HIDE).stdout.strip()
    if action == "hosts_read":
        p=os.path.join(os.environ.get("SystemRoot",r"C:\\Windows"),"System32","drivers","etc","hosts")
        try: return open(p,encoding="utf-8",errors="replace").read()
        except OSError as e: return str(e)
    if action == "timezone_set":
        if not value or not needs_confirmation: return "A timezone and confirmation are required."
        out=subprocess.run(["tzutil","/s",str(value)],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return "Timezone changed." if out.returncode==0 else out.stderr.strip()
    if action == "dns_servers_set":
        if not value or not needs_confirmation: return "A DNS configuration and confirmation are required."
        return "DNS changes require an explicit adapter-specific implementation; no change was made."
    if action == "proxy_set":
        if not value or not needs_confirmation: return "A proxy configuration and confirmation are required."
        out=subprocess.run(["netsh","winhttp","set","proxy",str(value)],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None


def windows_maintenance(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    commands={
      "user_accounts": 'Get-LocalUser | Select-Object Name,Enabled,LastLogon,Description | ConvertTo-Json -Compress',
      "local_groups": 'Get-LocalGroup | Select-Object Name,Description | ConvertTo-Json -Compress',
      "installed_software_paths": 'Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Where-Object DisplayName | Select-Object DisplayName,InstallLocation | ConvertTo-Json -Compress',
      "recycle_bin_size": '(Get-ChildItem -LiteralPath "$env:SystemDrive\\$Recycle.Bin" -Force -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum'
    }
    if action in commands:
        out=subprocess.run(["powershell","-NoProfile","-Command",commands[action]],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "No data returned."
    if action == "restore_point_create":
        if not needs_confirmation: return "Creating a restore point requires confirmation."
        out=subprocess.run(["powershell","-NoProfile","-Command","Checkpoint-Computer -Description 'Mark-LIV restore point' -RestorePointType MODIFY_SETTINGS"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Restore point command completed."
    if action == "optional_features":
        out=subprocess.run(["powershell","-NoProfile","-Command","Get-WindowsOptionalFeature -Online | Select-Object FeatureName,State | ConvertTo-Json -Compress"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "No data returned."
    return None
