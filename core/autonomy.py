"""
JARVIS Autonomy Core.

Turns a high-level user goal into a validated plan, executes one step at a time,
verifies tool results, and replans after failures. Destructive actions never get
their own confirmation mechanism here: they are delegated to the normal action
layer, whose core.confirm gate remains the security boundary.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any

from core.gemini import as_json, FAST, SMART
from core.permissions import needs_confirmation


@dataclass
class PlanStep:
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    verify: str = ""


@dataclass
class Plan:
    goal: str
    steps: list[PlanStep]
    summary: str = ""


class AutonomyEngine:
    """Goal -> plan -> execute -> verify -> recover/replan."""

    MAX_STEPS = 12
    MAX_REPLANS = 2

    def __init__(self, registry, ctx=None, logger=print):
        self.registry = registry
        self.ctx = ctx or {}
        self.logger = logger

    def _catalog(self) -> str:
        rows = []
        for name in sorted(self.registry.names()):
            rec = self.registry._actions.get(name)
            if not rec:
                continue
            rows.append(f"{name}: {rec.description[:240]}")
        return "\n".join(rows)

    def _plan(self, goal: str, failure: str = "") -> Plan | None:
        prompt = f"""
You are the planning brain of a local Windows JARVIS.
Create a concrete, minimal execution plan for this goal:

GOAL:
{goal}

AVAILABLE ACTIONS:
{self._catalog()}

Rules:
- Only use action names from AVAILABLE ACTIONS.
- Never invent a tool.
- Prefer inspection/read-only actions before modification.
- For destructive changes, select the existing destructive action; NEVER add
  confirmation parameters and NEVER claim approval.
- Each step must have parameters that match the action's schema as closely as
  possible.
- Maximum {self.MAX_STEPS} steps.
- If the goal cannot be completed with these actions, return an empty steps list.
- If a previous attempt failed, change strategy instead of repeating the exact
  same failed step.

Return ONLY JSON:
{{
  "summary": "short plan summary",
  "steps": [
    {{"action":"...", "parameters":{{}}, "reason":"...", "verify":"..."}}
  ]
}}
Previous failure:
{failure or "none"}
"""
        data = as_json(prompt, tier=SMART, timeout_ms=15000, default=None)
        if not isinstance(data, dict):
            return None
        steps = []
        for raw in data.get("steps", []):
            if not isinstance(raw, dict):
                continue
            action = str(raw.get("action") or "").strip()
            if not action or not self.registry.has(action):
                continue
            params = raw.get("parameters")
            if not isinstance(params, dict):
                params = {}
            steps.append(PlanStep(
                action=action,
                parameters=params,
                reason=str(raw.get("reason") or ""),
                verify=str(raw.get("verify") or ""),
            ))
        return Plan(goal=goal, steps=steps[:self.MAX_STEPS],
                    summary=str(data.get("summary") or ""))

    def _result_ok(self, result: Any) -> bool:
        text = str(result or "").lower()
        if "[confirmation_pending]" in text:
            return True
        if isinstance(result, dict):
            return bool(result.get("ok", False))
        bad = ("failed", "error:", "not available", "unknown tool", "permission denied")
        return not any(x in text for x in bad)

    def run(self, goal: str) -> str:
        goal = str(goal or "").strip()
        if not goal:
            return "I need a goal to execute."

        history = []
        failure = ""
        for attempt in range(self.MAX_REPLANS + 1):
            plan = self._plan(goal, failure=failure)
            if not plan or not plan.steps:
                return ("I could not build a safe executable plan for that goal "
                        "with the actions currently available.")

            self.logger(f"[Autonomy] Plan {attempt + 1}: {plan.summary}")
            for index, step in enumerate(plan.steps, 1):
                # A model-produced action can never bypass the normal permission
                # layer. This is deliberately informational; confirmation is
                # enforced by the action implementation itself.
                if needs_confirmation(step.action):
                    self.logger(f"[Autonomy] Confirmation-gated step: {step.action}")

                started = time.monotonic()
                result = self.registry.run(step.action, step.parameters, self.ctx)
                elapsed = time.monotonic() - started
                history.append((step.action, result))

                if self._result_ok(result):
                    self.logger(f"[Autonomy] Step {index}/{len(plan.steps)} OK: "
                                 f"{step.action} ({elapsed:.1f}s)")
                    if "[CONFIRMATION_PENDING]" in str(result):
                        return str(result)
                    continue

                failure = f"Action {step.action} failed: {result}"
                self.logger(f"[Autonomy] {failure}")
                break
            else:
                last = history[-1][1] if history else "Done."
                return (
                    f"{plan.summary or 'Goal completed.'}\n"
                    f"Executed {len(plan.steps)} step(s).\n"
                    f"Final result: {last}"
                )

        return ("I attempted the goal, verified the failed step, and replanned "
                "but could not complete it safely. Last failure: " + failure)
