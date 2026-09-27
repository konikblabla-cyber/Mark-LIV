import unittest
from unittest.mock import patch

import actions.computer_control as computer_control


class ComputerControlTests(unittest.TestCase):
    def test_unknown_action_is_rejected(self):
        result = computer_control.handle({"action": "does_not_exist"})
        self.assertIsInstance(result, dict)
        self.assertFalse(result.get("ok", True))

    @patch("actions.computer_control._uia_click", return_value="UI element clicked.")
    def test_uia_click_dispatches(self, uia_click):
        result = computer_control.handle({
            "action": "uia_click",
            "title": "Notepad",
            "auto_id": "123",
        })
        uia_click.assert_called_once()
        self.assertTrue(result.get("ok", False))
        self.assertEqual(result.get("result"), "UI element clicked.")

    @patch("actions.computer_control._uia_type", return_value="UI text entered.")
    def test_uia_type_dispatches(self, uia_type):
        result = computer_control.handle({
            "action": "uia_type",
            "title": "Notepad",
            "control_title": "Editor",
            "text": "hello",
        })
        uia_type.assert_called_once()
        self.assertTrue(result.get("ok", False))

    def test_invalid_click_button_is_rejected(self):
        result = computer_control.handle({"action": "click", "x": 10, "y": 10, "button": "invalid"})
        self.assertIsInstance(result, dict)
        self.assertFalse(result.get("ok", True))

    @patch("actions.computer_control.pyautogui.click")
    @patch("actions.computer_control._virtual_screen_geometry", return_value=(0, 0, 1920, 1080))
    def test_click_coordinates_are_clamped(self, _geometry, click):
        result = computer_control.handle({
            "action": "click",
            "x": 99999,
            "y": 99999,
            "button": "left",
        })
        click.assert_called_once_with(1919, 1079, button="left", clicks=1, interval=0.0)
        self.assertTrue(result.get("ok", False))


    @patch("actions.computer_control.pyautogui.moveTo")
    @patch("actions.computer_control._virtual_screen_geometry", return_value=(0, 0, 1920, 1080))
    def test_move_coordinates_are_clamped(self, _geometry, move_to):
        result = computer_control.handle({
            "action": "move",
            "x": -50,
            "y": 99999,
        })
        move_to.assert_called_once_with(0, 1079, duration=0.15)
        self.assertTrue(result.get("ok", False))


if __name__ == "__main__":
    unittest.main()

    @patch("actions.computer_control._open_browser_target", return_value="Browser window reused: https://example.com")
    def test_open_browser_dispatches(self, open_browser):
        result = computer_control.handle({
            "action": "open_browser",
            "url": "https://example.com",
            "browser": "opera gx",
        })
        open_browser.assert_called_once_with("https://example.com", "opera gx")
        self.assertTrue(result.get("ok", False))
        self.assertIn("Browser window reused", result.get("result", ""))
