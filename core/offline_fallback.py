"""Deterministic offline command fallback for essential JARVIS functions."""
from __future__ import annotations

import re


def handle(text: str):
    q = " ".join(str(text or "").strip().lower().split())
    if not q:
        return None

    if any(x in q for x in ("status komputera", "stan komputera", "system status", "pc status")):
        from actions.pc_status import pc_status
        return pc_status({})

    if q in {"zadania", "moje zadania", "lista zadań", "lista zadan", "daily tasks"}:
        from actions.daily_planner import daily_planner
        return daily_planner({"action": "list"})

    if any(x in q for x in ("następne zadanie", "nastepne zadanie", "next task")):
        from actions.daily_planner import daily_planner
        return daily_planner({"action": "next"})

    m = re.match(r"^(?:dodaj|add) (?:zadanie|task)[: ]+(.+)$", q)
    if m:
        from actions.daily_planner import daily_planner
        return daily_planner({"action": "add", "title": m.group(1)})

    if q in {"self test", "autotest", "test jarvisa", "test jarvis"}:
        from actions.autonomous_tasks import jarvis_self_test
        return jarvis_self_test({})

    if q in {"status jarvisa", "stan jarvisa", "jarvis status"}:
        from actions.autonomous_tasks import jarvis_status
        return jarvis_status({})

    return None
