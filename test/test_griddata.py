#!/usr/bin/env python
"""
Test griddata extractor for CST.
"""
import numpy
import unittest

class TestGridData(unittest.TestCase):
    """Tests for griddata extraction from CST project.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_unittest_config(self):
        """Test the setup to ensure unittest asserts behave as expected.
        """
        self.assertEqual(1,1)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
