"""High-level local PC status snapshot for JARVIS."""
from __future__ import annotations
import json
import platform
import shutil
import subprocess
import time

try:
    import psutil
except Exception:
    psutil = None


def _windows_foreground():
    if platform.system() != "Windows":
        return {}
    try:
        import ctypes
        import psutil as _psutil
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        p = _psutil.Process(pid.value)
        return {"pid": p.pid, "process": p.name(), "path": p.exe()}
    except Exception:
        return {}


def _gpu():
    try:
        import pynvml
        pynvml.nvmlInit()
        rows = []
        for i in range(pynvml.nvmlDeviceGetCount()):
            h = pynvml.nvmlDeviceGetHandleByIndex(i)
            mem = pynvml.nvmlDeviceGetMemoryInfo(h)
            rows.append({
                "name": pynvml.nvmlDeviceGetName(h),
                "utilization_percent": pynvml.nvmlDeviceGetUtilizationRates(h).gpu,
                "memory_used_mb": round(mem.used / 1048576),
                "memory_total_mb": round(mem.total / 1048576),
                "temperature_c": pynvml.nvmlDeviceGetTemperature(h, pynvml.NVML_TEMPERATURE_GPU),
            })
        pynvml.nvmlShutdown()
        return rows
    except Exception:
        return []


def pc_status(parameters=None, **kwargs):
    if psutil is None:
        return "psutil is required for pc_status."
    interval = 0.15
    try:
        psutil.cpu_percent(interval=interval)
        boot = psutil.boot_time()
        disks = []
        for part in psutil.disk_partitions(all=False):
            try:
                u = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "mount": part.mountpoint,
                    "total_gb": round(u.total / 1e9, 1),
                    "used_gb": round(u.used / 1e9, 1),
                    "free_gb": round(u.free / 1e9, 1),
                    "used_percent": u.percent,
                })
            except (PermissionError, OSError):
                pass
        battery = psutil.sensors_battery()
        result = {
            "os": platform.platform(),
            "cpu_percent": psutil.cpu_percent(interval=0.15),
            "ram_percent": psutil.virtual_memory().percent,
            "ram_available_gb": round(psutil.virtual_memory().available / 1e9, 1),
            "disk": disks,
            "battery": None if battery is None else {
                "percent": battery.percent,
                "plugged": battery.power_plugged,
            },
            "uptime_hours": round((time.time() - boot) / 3600, 1),
            "foreground": _windows_foreground(),
            "gpu": _gpu(),
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return f"PC status failed: {e}"


TOOL = {
    "name": "pc_status",
    "description": "Return one compact read-only snapshot of CPU, RAM, disks, battery, uptime, foreground app and NVIDIA GPU usage.",
    "parameters": {"type": "OBJECT", "properties": {}},
    "handler": pc_status,
}
