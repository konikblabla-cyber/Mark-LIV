"""
core/confirm.py — a confirmation the model cannot forge.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional

_continuation: Optional[Callable[[str], None]] = None
TIMEOUT_SECONDS = 90.0


@dataclass
class _Pending:
    key: str
    title: str
    detail: str
    run: Callable[[], str]
    at: float
    continuation: Optional[Callable[[str], None]] = None


_pending: Optional[_Pending] = None
_lock = threading.Lock()
_show_cb: Optional[Callable[[str, str], None]] = None
_hide_cb: Optional[Callable[[], None]] = None
_log_cb: Optional[Callable[[str], None]] = None
_voice_armed_until = 0.0


def bind(show, hide, log=None) -> None:
    global _show_cb, _hide_cb, _log_cb
    _show_cb, _hide_cb, _log_cb = show, hide, log


def _log(msg: str) -> None:
    if _log_cb:
        try:
            _log_cb(msg)
        except Exception:
            pass


def set_continuation(callback: Optional[Callable[[str], None]]) -> None:
    global _continuation
    with _lock:
        _continuation = callback


def arm_voice(seconds: float = 12.0) -> None:
    global _voice_armed_until
    with _lock:
        _voice_armed_until = time.monotonic() + max(1.0, min(float(seconds), 30.0))


def voice_armed() -> bool:
    with _lock:
        return time.monotonic() < _voice_armed_until


def resolve_voice(accepted: bool) -> bool:
    global _voice_armed_until
    with _lock:
        if time.monotonic() >= _voice_armed_until:
            return False
        _voice_armed_until = 0.0
        has_pending = _pending is not None and time.monotonic() - _pending.at <= TIMEOUT_SECONDS
    if not has_pending:
        return False
    resolve(bool(accepted))
    return True


def request(key: str, title: str, detail: str, run: Callable[[], str]) -> str:
    global _pending, _continuation
    with _lock:
        continuation = _continuation
        _continuation = None

        if _show_cb is None:
            return (
                f"I cannot confirm '{title}' right now because the interface is "
                f"not available, so I have not done it."
            )

        now = time.monotonic()
        if _pending is not None and now - _pending.at <= TIMEOUT_SECONDS:
            return (
                f"Another confirmation is already pending for '{_pending.title}'. "
                f"Nothing was done."
            )

        _pending = _Pending(key=key, title=title, detail=detail,
                            run=run, at=now, continuation=continuation)

    try:
        _show_cb(title, detail)
    except Exception as e:
        with _lock:
            _pending = None
        return f"Could not ask for confirmation: {e}. Nothing was done."

    _log(f"SYS: Awaiting confirmation — {title}")
    return (
        f"[CONFIRMATION_PENDING] I have put a confirmation on screen for: {title}. "
        f"Say ONE short sentence in the user's own language telling them you need "
        f"them to confirm it on the HUD before you do it. Do not claim it is done."
    )


def resolve(accepted: bool) -> None:
    global _pending
    with _lock:
        p, _pending = _pending, None

    if _hide_cb:
        try:
            _hide_cb()
        except Exception:
            pass

    if p is None:
        return
    if time.monotonic() - p.at > TIMEOUT_SECONDS:
        _log(f"SYS: Confirmation expired — {p.title}")
        return
    if not accepted:
        _log(f"SYS: Cancelled — {p.title}")
        return

    def _worker():
        try:
            result = p.run() or "Done."
            _log(f"SYS: Confirmed — {p.title}. {result}")
            if p.continuation:
                try:
                    p.continuation(str(result))
                except Exception as e:
                    _log(f"ERR: continuation failed — {e}")
        except Exception as e:
            _log(f"ERR: {p.title} failed — {e}")

    threading.Thread(target=_worker, daemon=True,
                     name=f"confirm-{p.key}").start()


def pending_title() -> str:
    with _lock:
        if _pending is None or time.monotonic() - _pending.at > TIMEOUT_SECONDS:
            return ""
        return _pending.title
