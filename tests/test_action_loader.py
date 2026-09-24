import unittest

from core.action_loader import ActionRegistry


class ActionLoaderTests(unittest.TestCase):
    def test_empty_registry_is_safe(self):
        registry = ActionRegistry({}, lambda _message: None)
        self.assertEqual(registry.names(), set())
        self.assertFalse(registry.has("missing"))
        self.assertEqual(registry.scheduling("missing"), None)

    def test_reserved_context_is_not_exposed_as_tool(self):
        registry = ActionRegistry({}, lambda _message: None)
        self.assertFalse(registry.has("player"))
        self.assertFalse(registry.has("speak"))
        self.assertFalse(registry.has("response"))


if __name__ == "__main__":
    unittest.main()
