import unittest

from core.action_loader import ActionRegistry, ActionRecord


class ActionLoaderDispatchTests(unittest.TestCase):
    def test_handler_exception_is_returned_without_crashing_registry(self):
        def bad(**_kwargs):
            raise RuntimeError("boom")
        record = ActionRecord(name="read_bad", description="bad", parameters={"type":"OBJECT"}, handler=bad, file="bad.py", valid=True)
        registry = ActionRegistry({"bad": record}, lambda _msg: None)
        result = registry.run("read_bad", {})
        self.assertIsInstance(result, str)
        self.assertIn("failed", result.lower())


if __name__ == "__main__":
    unittest.main()
