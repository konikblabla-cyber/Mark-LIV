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


if __name__ == "__main__":
    unittest.main()
