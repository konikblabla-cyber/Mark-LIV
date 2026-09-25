"""Risk-aware policy for autonomous JARVIS decisions."""
from __future__ import annotations
from dataclasses import dataclass
from core.permissions import needs_confirmation

@dataclass(frozen=True)
class Risk:
    level: str
    reason: str

READ_ONLY = {"inspect","read","list","search","status","audit","calculate","get"}

def classify(action: str, parameters: dict) -> Risk:
    if needs_confirmation(action):
        return Risk("high", "destructive or externally consequential action")
    name = action.lower()
    if any(x in name for x in ("delete","remove","uninstall","format","shutdown","restart","kill","terminate","admin")):
        return Risk("high", "action name indicates an irreversible or privileged change")
    if any(x in name for x in ("write","edit","move","copy","rename","install","service","registry","firewall")):
        return Risk("medium", "action changes system or user state")
    return Risk("low", "read-only or low-impact operation")

def can_autonomously_chain(action: str, parameters: dict) -> bool:
    return classify(action, parameters).level != "high"
