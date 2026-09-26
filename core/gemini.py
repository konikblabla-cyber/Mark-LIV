"""
One place where the assistant's one-shot Gemini calls are made.

WHY THIS EXISTS
    The live conversation runs on the Live API and is not what this file is
    about. Everything else — reading a screenshot, parsing a flight page,
    turning a request into a shell command, working out which WhatsApp button
    answers a call — was a separate `genai.Client(...)` built at the point of
    use, with the model name written inline. Sixteen files did it, twenty-six
    times, and not one of them set a timeout.

    That is not tidiness, it is three real faults:

    NO TIMEOUT.  The SDK waits forever by default. `gemini-flash-latest` spent
    an afternoon returning 504 DEADLINE_EXCEEDED, and every one of those calls
    became an unbounded hang — measured at ten seconds of silence while a phone
    rang, and worse elsewhere, because nothing was there to give up.

    NO FALLBACK.  One hardcoded alias meant that when that alias was unwell,
    the feature was simply gone. A ladder costs nothing when the first rung
    works and saves the feature when it does not.

    NO SINGLE PLACE TO CHANGE.  A new model release meant editing sixteen files
    and hoping none were missed.

THE LIVE MODEL DOES THIS WORK, AND IT LEADS THE LADDER
    Not the user's conversation — a separate, throwaway session per call, so
    nothing a plugin asks is ever heard by the person at the microphone.

    It leads because of quota. This is a voice assistant; the Live API is the
    dependency it already has, and it draws on a different pool from the text
    models. On the free tier it is the TEXT pool that runs out, and when it does
    every side call fails and the feature behind it dies with it. Putting Live
    first means ordinary use stops spending the pool that runs dry.

    The reply arrives through output_transcription, because these models refuse
    response_modalities=["TEXT"] with a 1007 — they only speak. That sounds
    fatal for structured output and is not: the transcription is the model's own
    text of what it said, and it returned "Mum ❤ click here for contact info",
    indented Python inside markdown fences, and src/utils/helpers_v2.py
    character for character.

    It cannot carry grounding metadata, so grounded web search stays on REST.

    Where the answer depends only on stable input, cache it and neither pool is
    touched twice. Concurrent identical requests are also coalesced: one Gemini
    call serves every waiter instead of spending the same tokens multiple times.
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
import threading
from pathlib import Path

if getattr(sys, "frozen", False):
    _BASE = Path(sys.executable).parent
else:
    _BASE = Path(__file__).resolve().parent.parent

_KEY_FILE = _BASE / "config" / "api_keys.json"

FAST = "fast"
SMART = "smart"
SEARCH = "search"
LIVE = "live"

_LADDERS = {
    FAST: (LIVE, "gemini-2.5-flash-lite", "gemini-2.5-flash"),
    SMART: (LIVE, "gemini-2.5-flash", "gemini-2.5-flash-lite"),
    SEARCH: ("gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"),
}
_LIVE_FALLBACK = "models/gemini-3.1-flash-live-preview"
_LIVE_SLOTS = threading.BoundedSemaphore(3)
_LIVE_SLOT_WAIT = 3.0
_ONE_SHOT_SYSTEM = (
    "Return exactly the requested output, with no acknowledgement, explanation, "
    "greeting, closing, or restatement. For JSON/code/one-word requests, output "
    "only that format. Preserve requested spelling, punctuation, case, and "
    "whitespace."
)
DEFAULT_TIMEOUT_MS = 10_000
MIN_TIMEOUT_MS = 10_000
_key_lock = threading.Lock()
_cached_key: str | None = None
_COOLDOWN_SECONDS = 300
_cooldown: dict[str, float] = {}
_cool_lock = threading.Lock()
_TEXT_CACHE_TTL = 90.0
_TEXT_CACHE_MAX = 96
_text_cache: dict[str, tuple[float, str]] = {}
_text_cache_lock = threading.Lock()
_text_inflight: dict[str, threading.Event] = {}


def _cache_key(contents, tier: str, config) -> str | None:
    if not isinstance(contents, str):
        return None
    system = ""
    if config is not None:
        system = getattr(config, "system_instruction", None) or (
            config.get("system_instruction", "") if isinstance(config, dict) else ""
        )
    return json.dumps([tier, str(system), contents], ensure_ascii=False, sort_keys=True)


def _cached_text(key: str) -> str | None:
    with _text_cache_lock:
        item = _text_cache.get(key)
        if not item:
            return None
        if time.monotonic() - item[0] > _TEXT_CACHE_TTL:
            _text_cache.pop(key, None)
            return None
        return item[1]


def _store_text(key: str, value: str) -> None:
    with _text_cache_lock:
        if len(_text_cache) >= _TEXT_CACHE_MAX:
            oldest = min(_text_cache, key=lambda k: _text_cache[k][0])
            _text_cache.pop(oldest, None)
        _text_cache[key] = (time.monotonic(), value)


def _cool(model: str) -> None:
    with _cool_lock:
        _cooldown[model] = time.monotonic() + _COOLDOWN_SECONDS


def _cooling(model: str) -> bool:
    with _cool_lock:
        until = _cooldown.get(model, 0.0)
        if until and time.monotonic() < until:
            return True
        _cooldown.pop(model, None)
        return False


def api_key(refresh: bool = False) -> str:
    global _cached_key
    with _key_lock:
        if _cached_key is not None and not refresh:
            return _cached_key
        try:
            data = json.loads(_KEY_FILE.read_text(encoding="utf-8"))
            _cached_key = str(data.get("gemini_api_key") or "")
        except Exception:
            _cached_key = ""
        return _cached_key


def client(timeout_ms: int = DEFAULT_TIMEOUT_MS, key: str = ""):
    from google import genai
    from google.genai import types as gtypes
    key = key or api_key()
    if not key:
        raise RuntimeError("no Gemini API key is configured")
    return genai.Client(
        api_key=key,
        http_options=gtypes.HttpOptions(timeout=max(MIN_TIMEOUT_MS, int(timeout_ms))),
    )


class _Reply:
    __slots__ = ("text",)

    def __init__(self, text: str):
        self.text = text


def _live_model() -> str:
    return getattr(sys.modules.get("main"), "LIVE_MODEL", None) or _LIVE_FALLBACK


def _to_live_parts(contents) -> list:
    import base64
    items = contents if isinstance(contents, (list, tuple)) else [contents]
    parts = []
    for item in items:
        if isinstance(item, str):
            parts.append({"text": item})
            continue
        blob = getattr(item, "inline_data", None)
        if blob is not None:
            data = getattr(blob, "data", None)
            mime = getattr(blob, "mime_type", None) or "application/octet-stream"
            if isinstance(data, bytes):
                data = base64.b64encode(data).decode("ascii")
            parts.append({"inline_data": {"mime_type": mime, "data": data}})
            continue
        txt = getattr(item, "text", None)
        if txt:
            parts.append({"text": txt})
            continue
        if isinstance(item, dict):
            parts.append(item)
    return parts


async def _live_turn(parts: list, system: str, key: str, timeout_s: float) -> str:
    from google import genai
    from google.genai import types as gtypes
    cl = genai.Client(api_key=key, http_options={"api_version": "v1beta"})
    kwargs = {
        "response_modalities": ["AUDIO"],
        "output_audio_transcription": {},
        "system_instruction": _ONE_SHOT_SYSTEM + (f"\n\n{system}" if system else ""),
    }
    cm = cl.aio.live.connect(model=_live_model(),
                             config=gtypes.LiveConnectConfig(**kwargs))
    session = await asyncio.wait_for(cm.__aenter__(), 30)
    try:
        await session.send_client_content(
            turns={"role": "user", "parts": parts}, turn_complete=True)
        chunks: list[str] = []

        async def drain():
            async for resp in session.receive():
                sc = getattr(resp, "server_content", None)
                if sc and sc.output_transcription and sc.output_transcription.text:
                    chunks.append(sc.output_transcription.text)

        await asyncio.wait_for(drain(), timeout=timeout_s)
        try:
            await asyncio.wait_for(drain(), timeout=1.5)
        except asyncio.TimeoutError:
            pass
        return "".join(chunks).strip()
    finally:
        try:
            await cm.__aexit__(None, None, None)
        except Exception:
            pass


def _live_call(contents, config, timeout_ms: int, key: str):
    system = ""
    if config is not None:
        system = getattr(config, "system_instruction", None) or \
            (config.get("system_instruction") if isinstance(config, dict) else "") or ""
    parts = _to_live_parts(contents)
    if not parts:
        return None
    if not _LIVE_SLOTS.acquire(timeout=_LIVE_SLOT_WAIT):
        raise RuntimeError("no free Live slot — leaving them for the conversation")
    box: dict = {}

    def runner():
        try:
            box["text"] = asyncio.run(
                _live_turn(parts, str(system), key, max(10.0, timeout_ms / 1000.0)))
        except BaseException as e:
            box["error"] = e

    try:
        th = threading.Thread(target=runner, daemon=True, name="gemini-live-oneshot")
        th.start()
        th.join(timeout=max(15.0, timeout_ms / 1000.0 + 20.0))
    finally:
        _LIVE_SLOTS.release()
    if "error" in box:
        raise box["error"]
    text = box.get("text")
    return _Reply(text) if text else None


def call(contents, tier: str = FAST, config=None,
         timeout_ms: int = DEFAULT_TIMEOUT_MS, key: str = ""):
    ladder = _LADDERS.get(tier)
    if ladder is None:
        ladder = (tier,) + tuple(m for m in _LADDERS[SMART] if m != tier)
    resolved_key = key or api_key()
    if not resolved_key:
        print("[Gemini] no Gemini API key is configured")
        return None
    cl = None
    tried = [m for m in ladder if not _cooling(m)] or list(ladder)
    for model in tried:
        try:
            if model == LIVE:
                reply = _live_call(contents, config, timeout_ms, resolved_key)
                if reply is not None:
                    return reply
                raise RuntimeError("the Live turn came back empty")
            if cl is None:
                cl = client(timeout_ms=timeout_ms, key=resolved_key)
            kwargs = {"model": model, "contents": contents}
            if config is not None:
                kwargs["config"] = config
            return cl.models.generate_content(**kwargs)
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                _cool(model)
                print(f"[Gemini] {model}: out of quota — skipping it for "
                      f"{_COOLDOWN_SECONDS // 60} minutes")
            else:
                print(f"[Gemini] {model}: {type(e).__name__}: {msg[:140]}")
    return None


def text(contents, tier: str = FAST, config=None,
         timeout_ms: int = DEFAULT_TIMEOUT_MS, key: str = "", default: str = "") -> str:
    cache_key = None if tier == SEARCH else _cache_key(contents, tier, config)
    if cache_key is not None:
        cached = _cached_text(cache_key)
        if cached is not None:
            return cached

    owner = True
    if cache_key is not None:
        with _text_cache_lock:
            if cache_key in _text_inflight:
                owner = False
                event = _text_inflight[cache_key]
            else:
                event = threading.Event()
                _text_inflight[cache_key] = event
        if not owner:
            event.wait(timeout=max(15.0, timeout_ms / 1000.0 + 25.0))
            cached = _cached_text(cache_key)
            if cached is not None:
                return cached
            # The owner failed. This caller becomes the new owner so a transient
            # failure does not multiply immediately into N identical retries.
            with _text_cache_lock:
                if cache_key in _text_inflight:
                    return default
                event = threading.Event()
                _text_inflight[cache_key] = event
                owner = True

    try:
        resp = call(contents, tier=tier, config=config,
                    timeout_ms=timeout_ms, key=key)
        if resp is None:
            return default
        value = (getattr(resp, "text", None) or "").strip() or default
        if cache_key is not None and value:
            _store_text(cache_key, value)
        return value
    finally:
        if cache_key is not None and owner:
            with _text_cache_lock:
                event = _text_inflight.pop(cache_key, None)
                if event is not None:
                    event.set()


def as_json(contents, tier: str = FAST, config=None,
            timeout_ms: int = DEFAULT_TIMEOUT_MS, key: str = "", default=None):
    raw = text(contents, tier=tier, config=config, timeout_ms=timeout_ms, key=key)
    if not raw:
        return default
    if "{" in raw and "}" in raw:
        raw = raw[raw.find("{"): raw.rfind("}") + 1]
    elif "[" in raw and "]" in raw:
        raw = raw[raw.find("["): raw.rfind("]") + 1]
    try:
        return json.loads(raw)
    except Exception as e:
        print(f"[Gemini] reply was not JSON: {e}")
        return default
