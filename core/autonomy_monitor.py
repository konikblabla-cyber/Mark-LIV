"""Background trigger logic for autonomous PC observation."""
from __future__ import annotations

import threading
from typing import Callable


class AutonomyMonitor:
    def __init__(
        self,
        audit: Callable[[], object],
        on_issue: Callable[[object], None],
        interval: int = 300,
        logger=print,
    ):
        self.audit = audit
        self.on_issue = on_issue
        try:
            parsed_interval = int(interval)
        except (TypeError, ValueError):
            parsed_interval = 300
        self.interval = max(30, parsed_interval)
        self.logger = logger
        self._stop = threading.Event()
        self._thread = None
        self._last_fingerprint = None
        self._health_counter = 0
        self._issue_streak = 0
        self._last_protection_fingerprint = None
        self._protection_streak = 0

    def _fingerprint(self, result):
        # Fingerprint only actionable state, not volatile uptime/CPU telemetry.
        if isinstance(result, dict):
            return str(sorted((k, str(v)) for k, v in result.items()))
        text = str(result or "")
        priority = text.split("Priorytety:", 1)[-1].split(
            "Procesy wymagające uwagi:", 1
        )[0]
        return priority.strip()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="jarvis-autonomy-monitor",
        )
        self._thread.start()
        self.logger("[AutonomyMonitor] started")

    def stop(self):
        self._stop.set()

    def check_once(self):
        try:
            result = self.audit()
            fp = self._fingerprint(result)
            changed = (
                self._last_fingerprint is not None
                and fp != self._last_fingerprint
            )
            self._last_fingerprint = fp
            if changed:
                self._issue_streak += 1
                if self._issue_streak >= 2:
                    self._issue_streak = 0
                    try:
                        self.on_issue(result)
                    except Exception as exc:
                        self.logger(
                            f"[AutonomyMonitor] issue handler failed: {exc}"
                        )
            else:
                self._issue_streak = 0
            self._check_local_protection()
            self._health_counter += 1
            if self._health_counter >= 6:
                self._health_counter = 0
                self._local_health_check()
            return result
        except Exception as exc:
            self.logger(f"[AutonomyMonitor] audit failed: {exc}")
            return None

    def _check_local_protection(self):
        """Cheap local anomaly check; never kills processes or calls Gemini."""
        try:
            from actions.jarvis_self_repair import jarvis_protection_fingerprint

            fp = tuple(jarvis_protection_fingerprint())
            changed = (
                self._last_protection_fingerprint is not None
                and fp != self._last_protection_fingerprint
            )
            self._last_protection_fingerprint = fp
            if fp and changed:
                self._protection_streak += 1
            else:
                self._protection_streak = 0
            if self._protection_streak >= 2:
                self.logger(
                    "[AutonomyMonitor] process anomaly detected; "
                    "running bounded safe maintenance"
                )
                self._protection_streak = 0
                try:
                    from actions.autonomous_pc_audit import safe_pc_optimization

                    result = safe_pc_optimization({})
                    self.logger(
                        "[AutonomyMonitor] safe maintenance: "
                        + str(result)[:500]
                    )
                except Exception as exc:
                    self.logger(
                        f"[AutonomyMonitor] safe maintenance failed: {exc}"
                    )
        except Exception as exc:
            self.logger(f"[AutonomyMonitor] protection check failed: {exc}")

    def _local_health_check(self):
        """Cheap periodic core check; deliberately avoids Gemini/API calls."""
        checks = (
            "core.confirm",
            "core.autonomy",
            "core.wake_word",
            "memory.memory_manager",
        )
        failed = []
        for name in checks:
            try:
                __import__(name)
            except Exception as exc:
                failed.append(f"{name}: {str(exc)[:120]}")
        if failed:
            message = "[AutonomyMonitor] local health warning: " + " | ".join(failed)
            self.logger(message)
            try:
                from core.status_center import record

                record("health", message, level="warning")
            except Exception:
                pass
            # Repair only the bounded local runtime; never alter user files/processes here.
            try:
                from actions.jarvis_self_repair import jarvis_self_repair

                repair = jarvis_self_repair({})
                self.logger(
                    "[AutonomyMonitor] self-repair: " + str(repair)[:500]
                )
            except Exception as exc:
                self.logger(
                    f"[AutonomyMonitor] self-repair failed: {exc}"
                )
        else:
            self.logger("[AutonomyMonitor] local self-test OK")

    def _loop(self):
        while not self._stop.wait(self.interval):
            self.check_once()
