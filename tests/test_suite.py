import unittest

from tests.test_permissions import PermissionsTests
from tests.test_permissions_edge import PermissionEdgeTests
from tests.test_action_loader import ActionLoaderTests
from tests.test_action_loader_dispatch import ActionLoaderDispatchTests
from tests.test_computer_control import ComputerControlTests
from tests.test_llm_client import LlmClientTests
from tests.test_memory_manager import MemoryManagerTests
from tests.test_imports import ImportSmokeTests
from tests.test_desktop_sandbox import DesktopSandboxTests
from tests.test_broad_control import BroadControlTests


def suite():
    loader = unittest.TestLoader()
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(PermissionsTests),
        loader.loadTestsFromTestCase(PermissionEdgeTests),
        loader.loadTestsFromTestCase(ActionLoaderTests),
        loader.loadTestsFromTestCase(ActionLoaderDispatchTests),
        loader.loadTestsFromTestCase(ComputerControlTests),
        loader.loadTestsFromTestCase(LlmClientTests),
        loader.loadTestsFromTestCase(MemoryManagerTests),
        loader.loadTestsFromTestCase(ImportSmokeTests),
        loader.loadTestsFromTestCase(DesktopSandboxTests),
        loader.loadTestsFromTestCase(BroadControlTests),
    ])


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
