"""Unittests for DataNArrayABC.
"""

import unittest
from cstmod.field_reader import DataNArrayABC

class TestDataNArrayABC(unittest.TestCase):
    """Unit tests for DataNArrayABC abstract base class.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_config(self):
        """Ensure the unittest framework is set up properly.
        """
        self.assertTrue(True)

    def test_instantiate(self):
        """Test that DataNArrayABC is abstract.
        """
        with self.assertRaises(TypeError):
            # Cannot instantiate an abs tract base class
            dna = DataNArrayABC()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if "__main__" == __name__:
    unittest.main()