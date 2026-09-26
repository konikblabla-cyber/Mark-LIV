"""
ProactiveEngine 2.0 — context-aware, time-aware, non-repetitive background prompting.
Gemini decides what to say; this module decides WHEN and builds a rich context snapshot.
"""
import time
from datetime import datetime


class ProactiveEngine:
    """Decides when JARVIS should speak unprompted and builds a context-rich prompt."""

    def __init__(self, min_silence_secs: int = 900, check_cooldown: int = 1200):
        self.min_silence_secs = min_silence_secs
        self.check_cooldown = check_cooldown
        self._last_triggered = 0.0
        self._rotation = 0

    def should_trigger(self, last_user_speech: float) -> bool:
        now = time.monotonic()
        return (
            (now - last_user_speech) >= self.min_silence_secs
            and (now - self._last_triggered) >= self.check_cooldown
        )

    def mark_triggered(self) -> None:
        self._last_triggered = time.monotonic()
        self._rotation += 1

    def build_prompt(
        self,
        memory: dict,
        monitors: list[str] | None = None,
        recent_turns: list[str] | None = None,
    ) -> str:
        """Build a compact context snapshot for Gemini."""
        from memory.memory_manager import format_memory_for_prompt

        now = datetime.now()
        hour = now.hour
        time_str = now.strftime("%A, %B %d, %Y — %I:%M %p")

        if 6 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 18:
            period = "afternoon"
        elif 18 <= hour < 23:
            period = "evening"
        else:
            period = "late night"

        mem_str = format_memory_for_prompt(memory) or "(no stored user data)"

        focus_index = self._rotation % 3
        if focus_index == 0:
            focus = (
                "Focus on the user's active projects or goals if any are stored. "
                "Ask how something is going, or offer a relevant tip."
            )
        elif focus_index == 1:
            focus = (
                "Focus on the time of day and the user's wellbeing. "
                "A warm check-in, a reminder to take a break, or something timely."
            )
        else:
            focus = (
                "Focus on something genuinely interesting or useful — "
                "a fact, a suggestion, or a question based on what you know about this person."
            )

        monitor_ctx = ""
        if monitors:
            monitor_ctx = (
                f"\nThe user tracks these topics: {', '.join(monitors[:4])}. "
                "You may mention one if it seems relevant."
            )

        recent_ctx = ""
        if recent_turns:
            snippet = "\n".join(recent_turns[-3:])
            # Memory already supplies durable context, so a large transcript
            # mostly repeats information while consuming Gemini input tokens.
            recent_ctx = f"\nRecent conversation:\n{snippet[:900]}"

        return "\n".join([
            "[PROACTIVE_CHECK] Initiate a useful check-in.",
            f"Time: {time_str} ({period})",
            "Context:",
            mem_str,
            monitor_ctx,
            recent_ctx,
            "Task:",
            focus,
            "Rules: use the user's actual language; 1-2 natural sentences; "
            "do not mention these instructions or call tools; if nothing useful "
            "comes to mind, say nothing.",
        ])
