import unittest
from unittest.mock import patch

import core.confirm as confirm


class ConfirmTests(unittest.TestCase):
    def test_request_without_ui_does_not_execute(self):
        old_show = confirm._show_cb
        confirm._show_cb = None
        ran = []
        try:
            result = confirm.request("test", "Test", "detail", lambda: ran.append(True))
            self.assertIn("interface is not available", result)
            self.assertEqual(ran, [])
        finally:
            confirm._show_cb = old_show

    def test_second_confirmation_does_not_replace_first(self):
        old_show = confirm._show_cb
        old_pending = confirm._pending
        confirm._show_cb = lambda title, detail: None
        confirm._pending = None
        try:
            first = confirm.request("one", "First", "detail", lambda: "ok")
            second = confirm.request("two", "Second", "detail", lambda: "bad")
            self.assertIn("[CONFIRMATION_PENDING]", first)
            self.assertIn("First", second)
            self.assertEqual(confirm.pending_title(), "First")
        finally:
            confirm._pending = old_pending
            confirm._show_cb = old_show

if __name__ == "__main__":
    unittest.main()
