"""
JARVIS Autonomy Core.

Turns a high-level user goal into a validated plan, executes one step at a time,
verifies tool results, and replans after failures. Destructive actions never get
their own confirmation mechanism here: they are delegated to the normal action
layer, whose core.confirm gate remains the security boundary.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from core.gemini import as_json, SMART
from core.autonomy_verifier import verify_text, verify_state, recovery_hint
from core import confirm
from core.task_manager import TaskManager
from core.autonomy_guard import audit_plan
from core.autonomy_policy import classify


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

    def __init__(self, registry, ctx=None, logger=print, task_manager=None, task_id=None):
        self.registry = registry
        self._catalog_cache = None
        self.ctx = ctx or {}
        self.logger = logger
        self.tasks = task_manager or TaskManager()
        self.task_id = task_id

    def _catalog(self) -> str:
        if self._catalog_cache is not None:
            return self._catalog_cache
        rows = []
        for name in sorted(self.registry.names()):
            rec = self.registry._actions.get(name)
            if not rec:
                continue
            rows.append(f"{name}: {rec.description[:240]}")
        self._catalog_cache = "\n".join(rows)
        return self._catalog_cache

    def _plan(self, goal: str, failure: str = "") -> Plan | None:
        prompt = f"""Local Windows JARVIS planner. Make the shortest safe plan for:
{goal}

ACTIONS:
{self._catalog()}

Rules: use only listed actions; inspect before changes; destructive actions use their normal confirmation gate; never invent confirmation/approval; max {self.MAX_STEPS} steps; on failure change strategy. Return ONLY JSON with summary and steps (action, parameters, reason, verify). Failure: {failure or "none"}"""
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
        steps = steps[:self.MAX_STEPS]
        problems = audit_plan(steps)
        if problems:
            self.logger("[Autonomy] Plan rejected by safety guard: " + "; ".join(problems))
            return None
        return Plan(goal=goal, steps=steps,
                    summary=str(data.get("summary") or ""))

    def _result_ok(self, result: Any, expectation: str = "") -> bool:
        return verify_text(result, expectation)

    def _failure(self, action: str, result: Any, expectation: str = "") -> str:
        return recovery_hint(action, result) + (
            f" Expected verification: {expectation}" if expectation else ""
        )

    def _execute_steps(self, plan: Plan, start: int, goal: str, history: list, replan_count: int = 0) -> str:
        """Execute remaining steps; a human confirmation resumes at the next step."""
        for index in range(start, len(plan.steps)):
            step = plan.steps[index]
            risk = classify(step.action, step.parameters)
            self.logger(f"[Autonomy] Risk={risk.level}: {step.action} — {risk.reason}")
            if risk.level == "high":
                self.logger(f"[Autonomy] Confirmation-gated step: {step.action}")

            def resume(_result: str, next_index=index + 1, current_plan=plan):
                self._execute_steps(current_plan, next_index, goal, history)

            confirm.set_continuation(resume)
            started = time.monotonic()
            result = self.registry.run(step.action, step.parameters, self.ctx)
            elapsed = time.monotonic() - started
            history.append((step.action, result))
            verified = self._result_ok(result, step.verify) and verify_state(step.action, step.parameters, result)
            if self.task_id:
                self.tasks.step(self.task_id, step.action, result, verified)
                if "[CONFIRMATION_PENDING]" in str(result):
                    self.tasks.update(self.task_id, status="waiting_confirmation", next_step=index)

            if verified:
                self.logger(
                    f"[Autonomy] Step {index + 1}/{len(plan.steps)} VERIFIED: "
                    f"{step.action} ({elapsed:.1f}s)"
                )
                if "[CONFIRMATION_PENDING]" in str(result):
                    return str(result)
                continue

            failure = self._failure(step.action, result, step.verify)
            if self.task_id:
                self.tasks.update(self.task_id, status="recovering", failure=failure)
            self.logger(f"[Autonomy] Recovery required: {failure}")
            if replan_count >= self.MAX_REPLANS:
                if self.task_id:
                    self.tasks.update(self.task_id, status="failed", failure=failure)
                return "Recovery limit reached: " + failure
            recovery = self._plan(goal, failure=failure)
            if recovery and recovery.steps:
                self.logger(f"[Autonomy] Recovery plan: {recovery.summary}")
                return self._execute_steps(recovery, 0, goal, history, replan_count + 1)
            if self.task_id:
                self.tasks.update(self.task_id, status="failed", failure=failure)
            return "Recovery failed: " + failure

        last = history[-1][1] if history else "Done."
        if self.task_id:
            self.tasks.update(self.task_id, status="completed", next_step=len(plan.steps))
        return (
            f"{plan.summary or 'Goal completed.'}\n"
            f"Executed {len(history)} step(s).\n"
            f"Final result: {last}"
        )

    def run(self, goal: str) -> str:
        goal = str(goal or "").strip()
        if not goal:
            return "I need a goal to execute."

        history = []
        failure = ""
        task_id = self.tasks.create(goal)
        self.task_id = task_id
        for attempt in range(self.MAX_REPLANS + 1):
            plan = self._plan(goal, failure=failure)
            if not plan or not plan.steps:
                if self.task_id:
                    self.tasks.update(self.task_id, status="failed",
                                      failure="No safe executable plan could be created.")
                return (
                    "I could not build a safe executable plan for that goal "
                    "with the actions currently available."
                )

            self.logger(f"[Autonomy] Plan {attempt + 1}: {plan.summary}")
            result = self._execute_steps(plan, 0, goal, history)
            if self.task_id and "[CONFIRMATION_PENDING]" not in result and not result.startswith("Recovery failed"):
                self.tasks.update(self.task_id, status="completed")
            return result

        return "I could not complete the goal safely."
