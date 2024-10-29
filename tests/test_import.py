import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest

class TestImportAccuracyModule(unittest.TestCase):
    def test_import_accuracy(self):
        try:
            # Attempt to import the Accuracy module from the docs package
            from DQMaRC import Accuracy
            self.assertTrue(True)  # If import is successful, pass the test
        except ImportError as e:
            self.fail(f"Failed to import Accuracy module: {e}")  # If import fails, fail the test


if __name__ == '__main__':
    unittest.main()
