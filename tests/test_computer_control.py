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


    @patch("actions.computer_control.permission_decision", return_value=("deny", "READ level allows only read/inspection operations"))
    @patch("actions.computer_control._click")
    def test_permission_gate_blocks_click(self, click, decision):
        result = computer_control.computer_control({"action": "click", "x": 10, "y": 10})
        self.assertIn("Permission denied", result)
        click.assert_not_called()
        decision.assert_called_once()

    @patch("actions.computer_control.permission_decision", return_value=("confirm", "NORMAL: confirmation required for consequential operation"))
    @patch("actions.computer_control._recover_process")
    def test_permission_gate_blocks_direct_process_restart_until_confirmed(self, recover, decision):
        result = computer_control.computer_control({
            "action": "process_recover",
            "process_name": "notepad",
            "restart": True,
        })
        self.assertIn("Confirmation required", result)
        recover.assert_not_called()
        decision.assert_called_once()

    @patch("actions.computer_control.permission_decision", return_value=("allow", "NORMAL: read-only operation"))
    @patch("actions.computer_control._active_window_info", return_value="window")
    def test_permission_gate_allows_read_action(self, active_window, decision):
        result = computer_control.computer_control({"action": "active_window_info"})
        self.assertEqual(result, "window")
        active_window.assert_called_once()
        decision.assert_called_once()

    @patch("actions.computer_control.permission_decision", return_value=("deny", "READ level allows only read/inspection operations"))
    @patch("actions.computer_control.pyautogui.click")
    def test_legacy_handle_cannot_bypass_permission_gate(self, click, decision):
        result = computer_control.handle({"action": "click", "x": 10, "y": 10})
        self.assertFalse(result.get("ok", True))
        self.assertIn("Permission denied", result.get("result", ""))
        click.assert_not_called()
        decision.assert_called_once()


if __name__ == "__main__":
    unittest.main()
