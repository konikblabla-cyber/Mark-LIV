"""High-level autonomous PC audit for Mark-LIV.
This is a decision layer: it gathers evidence, filters noise, and produces
actionable recommendations instead of dumping raw telemetry.
"""
from __future__ import annotations
import os
import platform
import shutil
import time
from pathlib import Path
import psutil

PROTECTED = {"System", "Registry", "smss.exe", "csrss.exe", "wininit.exe",
             "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe",
             "dwm.exe", "explorer.exe"}

def _top_processes(limit=8):
    rows=[]
    for p in psutil.process_iter(["pid","name","memory_percent","cpu_percent"]):
        try:
            info=p.info
            name=info.get("name") or "?"
            if name in PROTECTED: continue
            rows.append((float(info.get("memory_percent") or 0), float(info.get("cpu_percent") or 0),
                         int(info.get("pid") or 0), name))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(rows, reverse=True)[:limit]

def autonomous_pc_audit(parameters=None, **kwargs):
    p=parameters or {}
    threshold=max(50,min(int(p.get("disk_threshold",80)),99))
    disks=[]
    for part in psutil.disk_partitions(all=False):
        try:
            u=psutil.disk_usage(part.mountpoint)
            disks.append((part.mountpoint,u.percent,u.free,u.total))
        except (OSError,PermissionError):
            pass
    vm=psutil.virtual_memory()
    boot=time.time()-psutil.boot_time()
    rec=[]
    for mount,pct,free,total in disks:
        if pct>=threshold:
            rec.append(f"HIGH: {mount} ma {pct:.1f}% zajętości — uruchom analizę storage_cleanup_advisor.")
    if vm.percent>=85:
        rec.append(f"HIGH: RAM {vm.percent:.1f}% — sprawdź procesy obciążające pamięć.")
    if not rec:
        rec.append("Brak krytycznych problemów wykrytych w podstawowym audycie.")
    lines=[
        "JARVIS AUTONOMOUS PC AUDIT",
        f"System: {platform.platform()}",
        f"Uptime: {boot/86400:.1f} dni",
        f"RAM: {vm.percent:.1f}% ({vm.available/1073741824:.1f} GB dostępne)",
        "Dyski:"
    ]
    lines += [f"- {m}: {pct:.1f}% zajęte, {free/1073741824:.1f} GB wolne" for m,pct,free,total in disks]
    lines.append("Priorytety:")
    lines += [f"- {x}" for x in rec]
    lines.append("Procesy wymagające uwagi:")
    lines += [f"- PID {pid} {name}: RAM {mem:.1f}%, CPU {cpu:.1f}%" for mem,cpu,pid,name in _top_processes()]
    return "\n".join(lines)

TOOL={
    "name":"autonomous_pc_audit",
    "description":"Wysokopoziomowy audyt komputera: zbiera dane, odrzuca chronione procesy i wyznacza priorytety zamiast zwracać surowy spam diagnostyczny.",
    "parameters":{"type":"OBJECT","properties":{"disk_threshold":{"type":"INTEGER","description":"Próg zajętości dysku dla rekomendacji, domyślnie 80."}}},
    "handler":autonomous_pc_audit,
}
