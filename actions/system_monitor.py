"""Windows-only system monitoring and alert generation."""
import ctypes, platform, time
import psutil
if platform.system()!="Windows": raise RuntimeError("Mark-LIV is Windows-only.")

DEFAULT_THRESHOLDS={"cpu":90.0,"ram":90.0,"temp":85.0,"gpu":95.0}
_COOLDOWN=300
_CPU_STREAK=3
_nvml_lib=None
_nvml_ok=None
_pynvml_ok=None

def _nvml_gpu():
    global _nvml_lib,_nvml_ok
    if _nvml_ok is False:return -1.0
    try:
        class Util(ctypes.Structure):
            _fields_=[("gpu",ctypes.c_uint),("memory",ctypes.c_uint)]
        if _nvml_lib is None:
            for name in ("nvml.dll",r"C:\Windows\System32\nvml.dll"):
                try:
                    lib=ctypes.WinDLL(name);lib.nvmlInit_v2();_nvml_lib=lib;break
                except Exception: pass
        if _nvml_lib is None:_nvml_ok=False;return -1.0
        dev=ctypes.c_void_p();u=Util()
        if _nvml_lib.nvmlDeviceGetHandleByIndex_v2(0,ctypes.byref(dev))!=0:return -1.0
        if _nvml_lib.nvmlDeviceGetUtilizationRates(dev,ctypes.byref(u))!=0:return -1.0
        _nvml_ok=True;return float(u.gpu)
    except Exception:
        _nvml_ok=False;return -1.0

def _get_gpu_usage():
    global _pynvml_ok
    if _pynvml_ok is not False:
        try:
            import pynvml
            if _pynvml_ok is None:pynvml.nvmlInit();_pynvml_ok=True
            h=pynvml.nvmlDeviceGetHandleByIndex(0)
            return float(pynvml.nvmlDeviceGetUtilizationRates(h).gpu)
        except Exception:
            _pynvml_ok=False
    return _nvml_gpu()

def _get_cpu_temp():
    try:
        import wmi
        zones=wmi.WMI(namespace="root/wmi").MSAcpi_ThermalZoneTemperature()
        if zones:return (zones[0].CurrentTemperature/10.0)-273.15
    except Exception:pass
    try:
        temps=psutil.sensors_temperatures()
        for entries in temps.values():
            for entry in entries:
                if getattr(entry,"current",None) is not None:return float(entry.current)
    except Exception:pass
    return -1.0

def get_system_status():
    cpu=psutil.cpu_percent(interval=0.2)
    ram=psutil.virtual_memory()
    temp=_get_cpu_temp();gpu=_get_gpu_usage()
    uptime=max(0,time.time()-psutil.boot_time())
    return {"cpu_percent":round(cpu,1),"ram_percent":round(ram.percent,1),
            "ram_used_gb":round(ram.used/1024**3,1),"ram_total_gb":round(ram.total/1024**3,1),
            "cpu_temp_c":round(temp,1) if temp>=0 else None,
            "gpu_percent":round(gpu,1) if gpu>=0 else None,
            "uptime":f"{int(uptime//3600)}h {int(uptime%3600//60)}m",
            "process_count":len(psutil.pids())}

class SystemMonitor:
    def __init__(self,thresholds=None):
        self.thresholds={**DEFAULT_THRESHOLDS,**(thresholds or {})}
        self._last_alert={};self._cpu_streak=0
    def _can_alert(self,key):return time.monotonic()-self._last_alert.get(key,0)>_COOLDOWN
    def _record(self,key):self._last_alert[key]=time.monotonic()
    def check(self):
        try:
            cpu=psutil.cpu_percent(interval=None);ram=psutil.virtual_memory().percent
            temp=_get_cpu_temp();gpu=_get_gpu_usage()
        except Exception:return None
        alerts=[]
        if cpu>=self.thresholds["cpu"]:
            self._cpu_streak+=1
            if self._cpu_streak>=_CPU_STREAK and self._can_alert("cpu"):
                alerts.append(f"[SYSTEM_ALERT] CPU usage is {cpu:.0f}% for several checks.");self._record("cpu");self._cpu_streak=0
        else:self._cpu_streak=0
        if ram>=self.thresholds["ram"] and self._can_alert("ram"):
            alerts.append(f"[SYSTEM_ALERT] RAM is at {ram:.0f}%.");self._record("ram")
        if temp>=self.thresholds["temp"] and self._can_alert("temp"):
            alerts.append(f"[SYSTEM_ALERT] CPU temperature is {temp:.0f}°C.");self._record("temp")
        if gpu>=self.thresholds["gpu"] and self._can_alert("gpu"):
            alerts.append(f"[SYSTEM_ALERT] GPU load is {gpu:.0f}%.");self._record("gpu")
        return " ".join(alerts) if alerts else None

def system_monitor_action(parameters=None,**kwargs):
    action=str((parameters or {}).get("action","status")).strip().lower()
    if action in {"status","system_status"}:return str(get_system_status())
    if action in {"processes","process_list","top_processes"}:
        rows=[]
        for p in psutil.process_iter(["pid","name","memory_info"]):
            try:
                info=p.info;mem=info["memory_info"].rss/1024**2 if info["memory_info"] else 0
                rows.append((mem,info["pid"],info["name"] or "?"))
            except (psutil.NoSuchProcess,psutil.AccessDenied):pass
        rows.sort(reverse=True)
        return "\n".join(f"PID {pid}: {name} | RAM {mem:.0f} MB" for mem,pid,name in rows[:30]) or "No processes found."
    if action in {"disks","disk_status"}:
        out=[]
        for d in psutil.disk_partitions(all=False):
            try:
                u=psutil.disk_usage(d.mountpoint);out.append(f"{d.device}: {u.percent:.1f}% used, {u.free/1024**3:.1f} GB free")
            except (OSError,PermissionError):pass
        return "\n".join(out) or "No disk data."
    return "Unsupported monitoring action."

TOOL={"name":"system_monitor","description":"Windows-only read-only system status, process memory ranking and disk usage.","parameters":{"type":"OBJECT","properties":{"action":{"type":"STRING","description":"status | processes | disks"}}},"handler":system_monitor_action}
