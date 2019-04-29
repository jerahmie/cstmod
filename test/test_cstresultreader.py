#!/usr/bin/env python
"""
Test CstResultReader adapter class
"""
import os
from os.path import normpath, realpath, join
import unittest
from cstmod.cstutil import CSTRegInfo
from cstmod import CSTResultReader

cstmod_test_data_dir = normpath(join(realpath(__file__),
                                     '..', '..',
                                     'Test_Data'))

cst_project_path = 'simple_cosim_7T.cst'

class TestCstResultReader(unittest.TestCase):
    """Unittests for CSTResultReader interface class.
    """
    @classmethod
    def setUpClass(cls):
        print("Executing tests in " + __file__)

    def setUp(self):
        self.cst_versions = '2018'


    def testSetup(self):
        """Test the unittest setup.
        """
        self.assertEqual(1,1)

    def test_get_dll_version(self):
        """Returns the CSTResultReader version"""
        self.assertEqual(0, 1)

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
