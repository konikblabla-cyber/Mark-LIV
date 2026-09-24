import unittest

from tests.test_permissions import PermissionsTests
from tests.test_permissions_edge import PermissionEdgeTests
from tests.test_action_loader import ActionLoaderTests
from tests.test_computer_control import ComputerControlTests


def suite():
    loader = unittest.TestLoader()
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(PermissionsTests),
        loader.loadTestsFromTestCase(PermissionEdgeTests),
        loader.loadTestsFromTestCase(ActionLoaderTests),
        loader.loadTestsFromTestCase(ComputerControlTests),
        loader.loadTestsFromTestCase(LlmClientTests),
    ])


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
