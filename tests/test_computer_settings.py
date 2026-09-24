import unittest
from unittest.mock import patch

import actions.computer_settings as cs


class ComputerSettingsTests(unittest.TestCase):
    @patch("actions.computer_settings.pyautogui.hotkey")
    def test_focus_search_uses_windows_search(self, hotkey):
        with patch.object(cs, "_OS", "Windows"):
            cs.focus_search()
        hotkey.assert_called_once_with("win", "s")

    def test_unmute_is_explicit_action(self):
        self.assertIs(cs.ACTION_MAP["unmute"], cs.volume_unmute)

    @patch("actions.computer_settings.subprocess.run")
    @patch("actions.computer_settings._OS", "Linux")
    def test_brightness_up_avoids_shell(self, run):
        run.side_effect = [type("R", (), {"returncode": 1})(), type("R", (), {"stdout": "DP-1 connected\n\tBrightness: 0.5\n"})(), type("R", (), {})()]
        from actions import computer_settings
        computer_settings.brightness_up()
        self.assertFalse(any(kwargs.get("shell") for _, kwargs in run.call_args_list))

if __name__ == "__main__":
    unittest.main()
