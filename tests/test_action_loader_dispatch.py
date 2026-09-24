import unittest

from core.action_loader import ActionRecord, ActionRegistry


class ActionLoaderDispatchTests(unittest.TestCase):
    def test_run_passes_only_declared_context(self):
        calls = {}

        def handler(parameters, speak=None):
            calls["parameters"] = parameters
            calls["speak"] = speak
            return "ok"

        record = ActionRecord(
            name="demo",
            description="demo",
            parameters={"type": "OBJECT", "properties": {}},
            handler=handler,
            valid=True,
        )
        registry = ActionRegistry({"demo": record}, lambda _message: None)

        result = registry.run(
            "demo",
            {"value": 7},
            {"speak": "speaker", "player": "player", "response": "response"},
        )

        self.assertEqual(result, "ok")
        self.assertEqual(calls["parameters"], {"value": 7})
        self.assertEqual(calls["speak"], "speaker")

    def test_missing_action_returns_safe_message(self):
        registry = ActionRegistry({}, lambda _message: None)
        self.assertEqual(
            registry.run("missing", {}),
            "Action 'missing' is not available.",
        )


if __name__ == "__main__":
    unittest.main()
