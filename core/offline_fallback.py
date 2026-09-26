"""Deterministic offline command fallback for essential JARVIS functions."""
from __future__ import annotations

import re


def handle(text: str):
    q = " ".join(str(text or "").strip().lower().split())
    if not q:
        return None

    if any(x in q for x in (
        "status komputera", "stan komputera", "system status", "pc status",
        "jak działa komputer", "jak dziala komputer",
    )):
        from actions.pc_status import pc_status
        return pc_status({})

    if q in {"zadania", "moje zadania", "lista zadań", "lista zadan", "daily tasks"}:
        from actions.daily_planner import daily_planner
        return daily_planner({"action": "list"})

    if q in {"następne zadanie", "nastepne zadanie", "next task"}:
        from actions.daily_planner import daily_planner
        return daily_planner({"action": "next"})

    m = re.match(r"^(?:dodaj|add) (?:zadanie|task)[: ]+(.+)$", q)
    if m:
        title = m.group(1).strip()
        if len(title) > 200:
            title = title[:200].rstrip()
        if title:
            from actions.daily_planner import daily_planner
            return daily_planner({"action": "add", "title": title})

    if q in {"self test", "autotest", "test jarvisa", "test jarvis"}:
        from actions.autonomous_tasks import jarvis_self_test
        return jarvis_self_test({})

    if q in {"status jarvisa", "stan jarvisa", "jarvis status"}:
        from actions.autonomous_tasks import jarvis_status
        return jarvis_status({})

    if q in {"optymalizuj komputer", "optymalizuj pc", "safe optimization", "pc optimization"}:
        from actions.autonomous_pc_audit import safe_pc_optimization
        return safe_pc_optimization({})

    if q in {"sprawdź ochronę", "sprawdz ochrone", "ochrona komputera", "protection check"}:
        from actions.jarvis_self_repair import jarvis_protection_check
        return jarvis_protection_check({})

    return None
