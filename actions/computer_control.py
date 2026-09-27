    ]


def _mouse_move_verified(x: int, y: int) -> str:
    x, y = _validate_coords(x, y)
    pyautogui.moveTo(x, y, duration=0.3)
    return f"Mouse moved to {x},{y}"

def _click_visual_change(x: int, y: int, button: str = "left", clicks: int = 1) -> str:
    """Click and check a small local screen region; never calls Gemini."""
    _require_pyautogui()
    x, y = _validate_coords(x, y)
    pyautogui.moveTo(x, y, duration=0.08)
    actual = tuple(map(int, pyautogui.position()))
    if abs(actual[0] - x) > 2 or abs(actual[1] - y) > 2:
        raise RuntimeError(f"Mouse coordinate mismatch: requested=({x},{y}) actual={actual}")

    before = after = None
    try:
        import mss
        with mss.mss() as sct:
            mon = sct.monitors[0]
            radius = 80
            left = max(mon["left"], x - radius)
            top = max(mon["top"], y - radius)
            right = min(mon["left"] + mon["width"], x + radius)
            bottom = min(mon["top"] + mon["height"], y + radius)
            region = {"left": left, "top": top, "width": max(1, right-left), "height": max(1, bottom-top)}
            before = bytes(sct.grab(region).rgb)
            pyautogui.click(button=button, clicks=max(1, min(int(clicks), 10)))
            time.sleep(0.12)
            after = bytes(sct.grab(region).rgb)
    except Exception:
        pyautogui.click(button=button, clicks=max(1, min(int(clicks), 10)))
        time.sleep(0.12)

    changed = None
    if before is not None and after is not None and len(before) == len(after):
        step = max(1, len(before) // 4000)
        changed = any(before[i] != after[i] for i in range(0, len(before), step))
    status = "screen changed" if changed is True else ("no visible change" if changed is False else "click sent")
    return f"Clicked ({x}, {y}); {status}"


def _screen_find_and_verify(description: str) -> tuple[int, int] | None:
    coords = _screen_find(description)
    if coords is None:
        return None
    return _validate_coords(coords[0], coords[1])


def _screen_find(description: str) -> tuple[int, int] | None:
    api_key = _get_api_key()
    if not api_key:
        print("[ComputerControl] ⚠️ No API key for screen_find")
        return None

    try:
        from google import genai
        from google.genai import types as gtypes
