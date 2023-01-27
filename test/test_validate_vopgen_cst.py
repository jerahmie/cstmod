"""
Unit tests for validation of fields exported from cst with applied shims.
"""

import unittest
from cstmod.field_reader import FieldReaderH5


class TestValidateVopgenCST(unittest.TestCase):
    """
    Unit tests to provide validation between fields and shimmed fields
    between CST and Vogpen processed data.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    @unittest.skip
    def test_the_tests(self):
        self.assertTrue(True)

    def test_per_channel(self):
        self.assertTrue(True)
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
