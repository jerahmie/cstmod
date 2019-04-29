#!/usr/bin/env python
"""
Test CstResultReader adapter class
"""
import os
from os.path import normpath, realpath, join
import unittest
import winreg

cstmod_test_data_dir = normpath(join(realpath(__file__),
                                     '..', '..',
                                     'Test_Data'))

cst_project_path = 'simple_cosim_7T.cst'

class TestCstResultReader(unittest.TestCase):
    """Unittests for CSTResultReader interface class.
    """
    @classmethod
    def setUpClass(cls):
        cst_versions = ['2018']
        print("Executing tests in " + __file__)


    
    def setUp(self):
        pass

    def testSetup(self):
        """Test the unittest setup.
        """
        self.assertEqual(1,1)
    
    def testLocateResultReaderDLL(self):
        """A simple check to ensure the ResultReaderDLL can be found in the system.
        """
        wr_handle = winreg.ConnectRegistry(None, "SOFTWARE\")

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
