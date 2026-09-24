import unittest
from unittest.mock import patch

from core import confirm


class ConfirmTests(unittest.TestCase):
    def setUp(self):
        confirm.resolve(False)
        confirm.bind(lambda *_args: None, lambda: None)

    def tearDown(self):
        confirm.resolve(False)
        confirm.bind(None, None)

    def test_request_creates_pending_confirmation(self):
        result = confirm.request("demo", "Demo action", "details", lambda: "ok")
        self.assertIn("[CONFIRMATION_PENDING]", result)
        self.assertEqual(confirm.pending_title(), "Demo action")
        confirm.resolve(False)
        self.assertEqual(confirm.pending_title(), "")

    def test_request_refuses_without_ui(self):
        confirm.bind(None, None)
        result = confirm.request("demo", "Demo action", "details", lambda: "bad")
        self.assertIn("interface is not available", result)

    def test_cancel_does_not_run_action(self):
        called = []
        confirm.request("demo", "Demo action", "details", lambda: called.append(True) or "ok")
        confirm.resolve(False)
        self.assertEqual(called, [])


if __name__ == "__main__":
    unittest.main()
