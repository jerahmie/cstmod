"""
Unit tests for FieldReader helper classes
"""

import unittest
from rfutils import xmat

class TestFieldReader(unittest.TestCase):
    """Unit test class for Field Reader Abstract Base Class.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_fieldreader_abc(self):
        """Ensure a concrete FieldReader is derived from the abstract base class.
        """
        fr_cst2019 = xmat.FieldReaderCST2019()
        self.assertIsInstance(fr_cst2019, xmat.FieldReader)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if "__main__" == __name__:
    unittest.main()


