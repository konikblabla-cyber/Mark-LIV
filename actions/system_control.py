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
    extra = _system_control_extra(a, v, bool(p.get("needs_confirmation", False)))\n    if extra is not None: return extra\n    extra = windows_extra_controls(a, v, bool(p.get("needs_confirmation", False)))\n    if extra is not None: return extra\n    desknet = windows_desktop_network_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if desknet is not None: return desknet\n    printassoc = windows_print_assoc_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if printassoc is not None: return printassoc\n    netres = windows_network_resource_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if netres is not None: return netres\n    ident = windows_identity_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if ident is not None: return ident\n    admin = windows_admin_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if admin is not None: return admin\n    acct = windows_account_device_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if acct is not None: return acct\n    policy = windows_policy_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if policy is not None: return policy\n    acl = windows_acl_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if acl is not None: return acl\n    priv = windows_privilege_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if priv is not None: return priv\n    extra2 = windows_extra_actions(a, v, bool(p.get("needs_confirmation", False)))\n    if extra2 is not None: return extra2\n    perf = windows_performance_info(a, v)\n    if perf is not None: return perf\n    return "Unknown system_control action."
TOOL={"name":"system_control","description":"Windows-only direct system controls: power, timeouts, temp cleanup, DNS/network reset, startup/services, Wi-Fi and Bluetooth.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","description":"status, power_plan, sleep_timeout, display_timeout, temp_cleanup, dns_flush, network_reset, startup_list, services_list, service_start, service_stop, service_restart, wifi_on, wifi_off, bluetooth, installed_apps, exe_inventory, analyze_exe, process_tree, scheduled_tasks, event_log, installed_drivers, environment_vars, gpu_status, disk_health, defender_status, windows_updates, network_adapters, wifi_networks, ip_config, firewall_status, bitlocker_status, battery_status, windows_service_info, proxy_status, hosts_read, timezone_set, dns_servers_set, proxy_set, user_accounts, local_groups, installed_software_paths, recycle_bin_size, restore_point_create, optional_features, startup_registry_list, startup_disable, startup_enable, feature_enable, feature_disable, large_files, process_details, service_dependencies, listening_ports, disk_cleanup_preview, disk_cleanup_execute, process_command_lines, network_connections, usb_devices, bluetooth_devices, file_hash, digital_signature, scheduled_task_enable, scheduled_task_disable, service_enable, service_disable, process_kill_tree, memory_pressure, pagefile_status, reboot_required, defrag_status, disk_space_by_folder", service_status, scheduled_task_run, environment_set, environment_delete, admin_status, access_check, run_elevated, token_privileges, admin_group_members, acl_read, acl_grant, firewall_rule_list, firewall_rule_add, firewall_rule_remove, registry_read, mapped_drives, local_user_disable, local_group_add, device_disable, local_user_enable, local_group_remove, device_enable, registry_write, local_user_create, local_user_delete, local_group_create, local_group_delete, mapped_drives_disconnect, network_drive_map, printer_list, default_printer_set, printer_pause, printer_cancel_all, file_association, timezone_list, clipboard_get, clipboard_set, hosts_write, proxy_disable, default_app_set, dns_servers_set, proxy_enable, timezone_get"},"value":{"type":"STRING","description":"Minutes, power plan, service name, or Bluetooth on/off."}},"required":["action"]},"handler":system_control}

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


def windows_task_and_startup(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    if action == "scheduled_tasks":
        out=subprocess.run(["powershell","-NoProfile","-Command","Get-ScheduledTask | Select-Object TaskName,TaskPath,State | ConvertTo-Json -Compress"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action in ("startup_disable","startup_enable"):
        if not value or not needs_confirmation: return "An exact startup entry name and confirmation are required."
        # Only operate on the user's startup folder shortcut, not arbitrary registry entries.
        p=os.path.join(os.environ.get("APPDATA",""),r"Microsoft\Windows\Start Menu\Programs\Startup")
        matches=[os.path.join(p,x) for x in os.listdir(p)] if os.path.isdir(p) else []
        target=next((x for x in matches if os.path.basename(x).lower()==str(value).lower()),None)
        if not target: return "Startup shortcut not found in the user Startup folder."
        if action=="startup_disable":
            disabled=target+".disabled"
            os.rename(target,disabled); return f"Disabled startup item: {value}"
        if target.endswith(".disabled"):
            os.rename(target,target[:-9]); return f"Enabled startup item: {value}"
        return "Startup item is already enabled."
    return None


def windows_maintenance_extra(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    if action == "windows_update_search":
        cmd='Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 30 HotFixID,InstalledOn,Description | ConvertTo-Json -Compress'
        out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "No update history returned."
    if action in ("feature_enable","feature_disable"):
        if not value or not needs_confirmation: return "An exact Windows feature name and confirmation are required."
        state="Enabled" if action=="feature_enable" else "Disabled"
        cmd=f'Dism /Online /Enable-Feature /FeatureName:"{value}" /NoRestart' if state=="Enabled" else f'Dism /Online /Disable-Feature /FeatureName:"{value}" /NoRestart'
        out=subprocess.run(["cmd","/c",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "large_files":
        root=str(value or os.environ.get("USERPROFILE",r"C:\Users"))
        if not os.path.isdir(root): return "Directory not found."
        rows=[]
        for base,dirs,files in os.walk(root):
            dirs[:]=[d for d in dirs if d.lower() not in {"appdata","windows","program files","program files (x86)"}]
            for f in files:
                try:
                    p=os.path.join(base,f); s=os.path.getsize(p)
                    if s>=500*1024*1024: rows.append((s,p))
                except OSError: pass
        rows.sort(reverse=True)
        return json.dumps([{"path":p,"size_mb":round(s/1048576,1)} for s,p in rows[:100]],ensure_ascii=False)
    return None


def windows_resource_tools(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    commands={
      "process_details": 'Get-Process | Select-Object Id,ProcessName,CPU,WS,Path | Sort-Object WS -Descending | ConvertTo-Json -Compress',
      "service_dependencies": 'Get-Service | Select-Object Name,Status,DependentServices,ServicesDependedOn | ConvertTo-Json -Compress',
      "listening_ports": 'Get-NetTCPConnection -State Listen | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess | Sort-Object LocalPort | ConvertTo-Json -Compress'
    }
    if action in commands:
        out=subprocess.run(["powershell","-NoProfile","-Command",commands[action]],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "No data returned."
    if action == "disk_cleanup_preview":
        temp=os.environ.get("TEMP",""); rows=[]
        if temp and os.path.isdir(temp):
            for base,dirs,files in os.walk(temp):
                for f in files:
                    try:
                        p=os.path.join(base,f); rows.append((os.path.getsize(p),p))
                    except OSError: pass
        rows.sort(reverse=True)
        return json.dumps([{"path":p,"size_mb":round(s/1048576,1)} for s,p in rows[:100]],ensure_ascii=False)
    if action == "disk_cleanup_execute":
        if not needs_confirmation: return "Disk cleanup requires confirmation."
        temp=os.environ.get("TEMP",""); removed=0
        if temp and os.path.isdir(temp):
            for base,dirs,files in os.walk(temp,topdown=False):
                for f in files:
                    try: os.remove(os.path.join(base,f)); removed+=1
                    except OSError: pass
        return f"Removed {removed} temporary files."
    return None


def windows_security_inventory(action, value=None):
    if platform.system() != "Windows": return "This action is Windows-only."
    commands={
      "process_command_lines": 'Get-CimInstance Win32_Process | Select-Object ProcessId,Name,CommandLine,ExecutablePath | ConvertTo-Json -Compress',
      "network_connections": 'Get-NetTCPConnection | Select-Object State,LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess | ConvertTo-Json -Compress',
      "usb_devices": 'Get-PnpDevice -PresentOnly | Where-Object InstanceId -like "USB*" | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json -Compress',
      "bluetooth_devices": 'Get-PnpDevice -PresentOnly | Where-Object Class -eq "Bluetooth" | Select-Object Status,FriendlyName,InstanceId | ConvertTo-Json -Compress'
    }
    if action in commands:
        out=subprocess.run(["powershell","-NoProfile","-Command",commands[action]],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "No data returned."
    if action == "file_hash":
        p=str(value or "")
        if not p or not os.path.isfile(p): return "File not found."
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Get-FileHash -LiteralPath "{p.replace(chr(34),chr(96)+chr(34)+chr(96))}" -Algorithm SHA256 | ConvertTo-Json -Compress'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "digital_signature":
        p=str(value or "")
        if not p or not os.path.isfile(p): return "File not found."
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Get-AuthenticodeSignature -LiteralPath "{p.replace(chr(34),chr(96)+chr(34)+chr(96))}" | Select-Object Status,StatusMessage,SignerCertificate | ConvertTo-Json -Compress'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None


def windows_control_extra(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    if action == "startup_registry_list":
        cmd='Get-ItemProperty HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run,HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run | Select-Object * | ConvertTo-Json -Compress'
        out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "No registry startup entries found."
    if action in ("scheduled_task_enable","scheduled_task_disable"):
        if not value or not needs_confirmation: return "An exact task name and confirmation are required."
        verb="Enable-ScheduledTask" if action.endswith("enable") else "Disable-ScheduledTask"
        cmd=f'{verb} -TaskName "{str(value).replace(chr(34),chr(96)+chr(34)+chr(96))}" -ErrorAction Stop'
        out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Task command completed."
    if action in ("service_enable","service_disable"):
        if not value or not needs_confirmation: return "An exact service name and confirmation are required."
        mode="Automatic" if action.endswith("enable") else "Disabled"
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Set-Service -Name "{value}" -StartupType {mode} -ErrorAction Stop'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Service startup mode changed."
    if action == "process_kill_tree":
        if not value or not needs_confirmation: return "A PID and confirmation are required."
        try: pid=int(value)
        except ValueError: return "PID must be an integer."
        out=subprocess.run(["taskkill","/PID",str(pid),"/T","/F"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None













def windows_extra_controls(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "default_app_set":
        parts=value.split("|",1)
        if len(parts)!=2 or not all(parts): return "Use EXTENSION|PROGID, e.g. .txt|txtfile."
        if not needs_confirmation: return "Confirmation is required before changing a default app association."
        ext, progid=parts
        cmd=f"cmd /c assoc {ext}={progid}"
        out=subprocess.run(cmd,capture_output=True,text=True,shell=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Default association updated."
    if action == "dns_servers_set":
        parts=value.split("|")
        if len(parts)!=2 or not all(parts): return "Use ADAPTER|DNS1,DNS2."
        if not needs_confirmation: return "Confirmation is required before changing DNS servers."
        adapter,dns=parts
        servers=[x.strip() for x in dns.split(",") if x.strip()]
        if not servers:return "No DNS server supplied."
        cmd=["powershell","-NoProfile","-Command",f"Set-DnsClientServerAddress -InterfaceAlias '{adapter.replace(chr(39),chr(39)*2)}' -ServerAddresses @({','.join(chr(39)+x.replace(chr(39),chr(39)*2)+chr(39) for x in servers)})"]
        out=subprocess.run(cmd,capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "DNS servers updated."
    if action == "proxy_enable":
        if not needs_confirmation:return "Confirmation is required before enabling a proxy."
        parts=value.split("|")
        if len(parts)!=2:return "Use HOST|PORT."
        out=subprocess.run(["netsh","winhttp","set","proxy",f"{parts[0]}:{parts[1]}"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "timezone_get":
        out=subprocess.run(["powershell","-NoProfile","-Command","Get-TimeZone | Select-Object Id,DisplayName,BaseUtcOffset | Format-List"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_desktop_network_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "clipboard_get":
        out=subprocess.run(["powershell","-NoProfile","-Command","Get-Clipboard"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.rstrip() or out.stderr.strip()
    if action == "clipboard_set":
        if not needs_confirmation:return "Confirmation is required before replacing the clipboard."
        safe=value.replace("'","''")
        subprocess.run(["powershell","-NoProfile","-Command",f'Set-Clipboard -Value \'{safe}\''],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return "Clipboard updated."
    if action == "hosts_write":
        parts=value.split("|",1)
        if len(parts)!=2 or not all(parts):return "Use IP|HOSTNAME."
        if not needs_confirmation:return "Confirmation is required before changing the hosts file."
        line=f"{parts[0]} {parts[1]}"
        safe=line.replace("'","''")
        cmd=f"Add-Content -Path $env:SystemRoot\\System32\\drivers\\etc\\hosts -Value '{safe}'"
        out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Hosts entry added."
    if action == "proxy_disable":
        if not needs_confirmation:return "Confirmation is required before disabling the user proxy."
        out=subprocess.run(["netsh","winhttp","reset","proxy"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_print_assoc_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "printer_pause":
        if not value or not needs_confirmation:return "Printer name and confirmation are required."
        safe=value.replace("'","''")
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Suspend-PrintJob -PrinterName \'{safe}\' -JobId * -ErrorAction SilentlyContinue'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Printer jobs pause requested."
    if action == "printer_cancel_all":
        if not value or not needs_confirmation:return "Printer name and confirmation are required."
        safe=value.replace("'","''")
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Get-PrintJob -PrinterName \'{safe}\' -ErrorAction SilentlyContinue | Remove-PrintJob -Confirm:$false'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Printer jobs cancelled."
    if action == "file_association":
        if not value:return "File extension required, e.g. .pdf."
        ext=value if value.startswith(".") else "."+value
        out=subprocess.run(["cmd","/c","assoc",ext],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "timezone_list":
        out=subprocess.run(["tzutil","/l"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_network_resource_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "mapped_drives_disconnect":
        if not value or not needs_confirmation:return "Drive letter or network path and confirmation are required."
        out=subprocess.run(["net","use",value,"/delete","/y"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "network_drive_map":
        parts=value.split("|",1)
        if len(parts)!=2 or not all(parts):return "Use DRIVE|\\\\server\\share."
        if not needs_confirmation:return "Confirmation is required before mapping a network drive."
        out=subprocess.run(["net","use",parts[0],parts[1],"/persistent:yes"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "printer_list":
        out=subprocess.run(["powershell","-NoProfile","-Command","Get-Printer | Select Name,DriverName,PortName,Shared,Default | ConvertTo-Json -Compress"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "default_printer_set":
        if not value or not needs_confirmation:return "Printer name and confirmation are required."
        safe=value.replace("'","''")
        out=subprocess.run(["powershell","-NoProfile","-Command",f'(New-Object -ComObject WScript.Network).SetDefaultPrinter(\'{safe}\')'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Default printer changed."
    return None

def windows_identity_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "local_user_create":
        parts=value.split("|",1)
        if len(parts)!=2 or not all(parts):return "Use USERNAME|PASSWORD."
        if not needs_confirmation:return "Confirmation is required before creating a local account."
        out=subprocess.run(["net","user",parts[0],parts[1],"/add"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "local_user_delete":
        if not value or not needs_confirmation:return "Username and confirmation are required."
        out=subprocess.run(["net","user",value,"/delete"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "local_group_create":
        if not value or not needs_confirmation:return "Group name and confirmation are required."
        out=subprocess.run(["net","localgroup",value,"/add"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "local_group_delete":
        if not value or not needs_confirmation:return "Group name and confirmation are required."
        out=subprocess.run(["net","localgroup",value,"/delete"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_admin_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "local_user_enable":
        if not value or not needs_confirmation:return "Username and confirmation are required."
        out=subprocess.run(["net","user",value,"/active:yes"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "local_group_remove":
        parts=value.split("|",1)
        if len(parts)!=2 or not all(parts):return "Use GROUP|USERNAME."
        if not needs_confirmation:return "Confirmation is required before changing local group membership."
        out=subprocess.run(["net","localgroup",parts[0],parts[1],"/delete"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "device_enable":
        if not value or not needs_confirmation:return "Device instance ID and confirmation are required."
        safe=value.replace("'","''")
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Enable-PnpDevice -InstanceId \'{safe}\' -Confirm:$false'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "registry_write":
        parts=value.split("|",3)
        if len(parts)!=4 or not all(parts):return "Use PATH|NAME|TYPE|DATA."
        path,name,typ,data=parts
        if not needs_confirmation:return "Confirmation is required before changing the registry."
        out=subprocess.run(["reg","add",path,"/v",name,"/t",typ,"/d",data,"/f"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_account_device_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "mapped_drives":
        out=subprocess.run(["net","use"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "local_user_disable":
        if not value or not needs_confirmation:return "Username and confirmation are required."
        out=subprocess.run(["net","user",value,"/active:no"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "local_group_add":
        parts=value.split("|",1)
        if len(parts)!=2 or not all(parts):return "Use GROUP|USERNAME."
        if not needs_confirmation:return "Confirmation is required before changing local group membership."
        out=subprocess.run(["net","localgroup",parts[0],parts[1],"/add"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "device_disable":
        if not value or not needs_confirmation:return "Device instance ID and confirmation are required."
        safe=value.replace("'","''")
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Disable-PnpDevice -InstanceId \'{safe}\' -Confirm:$false'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_policy_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "firewall_rule_list":
        out=subprocess.run(["powershell","-NoProfile","-Command","Get-NetFirewallRule | Select DisplayName,Enabled,Direction,Action,Profile | ConvertTo-Json -Compress"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "firewall_rule_add":
        parts=value.split("|",3)
        if len(parts)!=4 or not all(parts): return "Use NAME|DIRECTION|PROTOCOL|LOCALPORT."
        name,direction,protocol,port=parts
        if not needs_confirmation:return "Confirmation is required before changing firewall rules."
        out=subprocess.run(["powershell","-NoProfile","-Command",f'New-NetFirewallRule -DisplayName "{name}" -Direction {direction} -Protocol {protocol} -LocalPort "{port}" -Action Allow'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Firewall rule added."
    if action == "firewall_rule_remove":
        if not value or not needs_confirmation:return "Rule name and confirmation are required."
        out=subprocess.run(["powershell","-NoProfile","-Command",f'Remove-NetFirewallRule -DisplayName "{value}"'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip() or "Firewall rule removed."
    if action == "registry_read":
        if not value:return "Registry path required."
        out=subprocess.run(["reg","query",value],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_acl_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "token_privileges":
        cmd='whoami /priv'
        out=subprocess.run(cmd,capture_output=True,text=True,shell=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "admin_group_members":
        out=subprocess.run(["net","localgroup","Administrators"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "acl_read":
        if not value:return "Path required."
        out=subprocess.run(["icacls",value],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "acl_grant":
        parts=value.split("|",2)
        if len(parts)!=3 or not all(parts): return "Use PATH|ACCOUNT|PERMISSION (for example PATH|user|M)."
        path,account,perm=parts
        if not needs_confirmation:return "Confirmation is required before changing ACL permissions."
        out=subprocess.run(["icacls",path,"/grant",f"{account}:{perm}"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    return None

def windows_privilege_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    if action in ("admin_status","elevated_status"):
        out=subprocess.run(["powershell","-NoProfile","-Command",'$p=New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent()); $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)'],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return "Administrator: " + out.stdout.strip()
    if action == "access_check":
        if not value: return "Path required."
        try:
            p=os.path.abspath(value); exists=os.path.exists(p)
            return json.dumps({"path":p,"exists":exists,"readable":os.access(p,os.R_OK),"writable":os.access(p,os.W_OK)},ensure_ascii=False)
        except Exception as e: return f"Access check failed: {e}"
    if action in ("run_elevated","open_elevated"):
        if not value or not needs_confirmation: return "Command/application and confirmation are required."
        safe=value.replace("'","''")
        ps(f"Start-Process -FilePath 'powershell.exe' -Verb RunAs -ArgumentList '-NoProfile','-Command','& {{ {safe} }}'")
        return "Elevation requested; Windows UAC will ask for approval."
    return None

def windows_extra_actions(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value = str(value or "").strip()
    if action == "service_status":
        if not value: return "Service name required."
        return subprocess.run(["powershell","-NoProfile","-Command",f'Get-Service -Name "{value}" -ErrorAction Stop | Select Status,Name,DisplayName,StartType | Format-List'],capture_output=True,text=True,creationflags=_WIN_HIDE).stdout.strip()
    if action == "scheduled_task_run":
        if not value or not needs_confirmation: return "Task name and confirmation are required."
        out=subprocess.run(["schtasks","/Run","/TN",value],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return out.stdout.strip() or out.stderr.strip()
    if action == "environment_set":
        if "=" not in value: return "Use NAME=VALUE."
        name,val=value.split("=",1)
        if not name.strip(): return "Variable name required."
        subprocess.run(["setx",name.strip(),val],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return f"User environment variable {name.strip()} updated for new processes."
    if action == "environment_delete":
        if not value or not needs_confirmation: return "Variable name and confirmation are required."
        subprocess.run(["reg","delete",r"HKCU\\Environment","/v",value,"/f"],capture_output=True,text=True,creationflags=_WIN_HIDE)
        return f"User environment variable {value} deleted."
    return None

def windows_performance_info(action, value=None):
    if platform.system() != "Windows": return "This action is Windows-only."
    commands={
      "memory_pressure": 'Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory,TotalVirtualMemorySize,FreeVirtualMemory | ConvertTo-Json -Compress',
      "pagefile_status": 'Get-CimInstance Win32_PageFileUsage | Select-Object Name,AllocatedBaseSize,CurrentUsage,PeakUsage | ConvertTo-Json -Compress',
      "reboot_required": 'Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Component Based Servicing\\RebootPending"',
      "defrag_status": 'Get-Volume | Where-Object DriveLetter | Select-Object DriveLetter,FileSystem,SizeRemaining,Size | ConvertTo-Json -Compress',
      "disk_space_by_folder": 'Get-ChildItem $env:USERPROFILE -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object { $s=(Get-ChildItem $_.FullName -File -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum; [pscustomobject]@{Folder=$_.FullName;SizeGB=[math]::Round($s/1GB,2)} } | Sort-Object SizeGB -Descending | ConvertTo-Json -Compress'
    }
    cmd=commands.get(action)
    if not cmd: return None
    out=subprocess.run(["powershell","-NoProfile","-Command",cmd],capture_output=True,text=True,creationflags=_WIN_HIDE)
    return out.stdout.strip() or out.stderr.strip() or "No data returned."


def windows_device_audio_controls(action, value=None, needs_confirmation=False):
    if platform.system() != "Windows": return "This action is Windows-only."
    value=str(value or "").strip()
    if action == "audio_devices":
        return _ps("Get-CimInstance Win32_SoundDevice | Select Name,Status,PNPDeviceID | Format-Table -AutoSize")
    if action == "camera_devices":
        return _ps("Get-PnpDevice -Class Camera -ErrorAction SilentlyContinue | Select Status,Class,FriendlyName,InstanceId | Format-Table -AutoSize")
    if action == "network_adapter_enable":
        if not value or not needs_confirmation:return "Adapter name and confirmation are required."
        return _ps(f"Enable-NetAdapter -Name '{value.replace(chr(39),chr(39)*2)}' -Confirm:$false; 'Network adapter enabled.'")
    if action == "network_adapter_disable":
        if not value or not needs_confirmation:return "Adapter name and confirmation are required."
        return _ps(f"Disable-NetAdapter -Name '{value.replace(chr(39),chr(39)*2)}' -Confirm:$false; 'Network adapter disabled.'")
    return None
