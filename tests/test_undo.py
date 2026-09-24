import unittest

from core import undo


class UndoTests(unittest.TestCase):
    def setUp(self):
        undo.clear()

    def tearDown(self):
        undo.clear()

    def test_last_operation_is_undone(self):
        calls = []
        undo.push_undo("demo", lambda: calls.append("undone") or "restored")
        self.assertTrue(undo.can_undo())
        self.assertEqual(undo.peek(), "demo")
        self.assertEqual(undo.undo_last(), "Undone: demo. restored")
        self.assertEqual(calls, ["undone"])
        self.assertFalse(undo.can_undo())

    def test_history_is_most_recent_first_and_is_bounded(self):
        for i in range(12):
            undo.push_undo(f"item-{i}", lambda: "ok")
        self.assertEqual(undo.history()[0], "item-11")
        self.assertEqual(len(undo.history()), undo.MAX_DEPTH)

    def test_empty_stack_is_safe(self):
        self.assertEqual(undo.undo_last().startswith("There is nothing to undo"), True)


if __name__ == "__main__":
    unittest.main()
