"""
Unit tests for interaction with Windows Registry to obtain information about CST installation.
"""

import os
import sys
import unittest
if sys.platform.startswith("win"):
    from cstmod.cstutil import CSTRegInfo
else:
    print("Testing CSTRegInfo assumes this is a windows platform. Exiting.")
    sys.exit()
    
class TestCstRegInfo(unittest.TestCase):
    """
    TestCase class for extracting CSTResultReader.dll version and location.
    """
    @classmethod
    def setUpClass(csl):
        pass
    
    def setUp(self):
        """
        possible_cst_versions -- list of CST versions supported in this test class.
        """
        self.supported_cst_versions = ['2018','2019']
    
    def test_framework_setup(self):
        """Ensure unittests are set up properly.
        """
        self.assertEqual(1,1)

    def test_installed_versions(self):
        """
        Find versions installed.
        """
        installed_cst_versions = CSTRegInfo.find_cst_reg_version()
        if 0 == len(installed_cst_versions):
            Warning("No versions of CST have been found.")
            sys.exit()
        print(installed_cst_versions)
        #self.assertTrue(set(self.supported_cst_versions).issubset(set(installed_cst_versions)))
        self.assertTrue(set(installed_cst_versions).issubset(set(self.supported_cst_versions)))
        
    def test_result_reader_location(self):
        """
        Find ResultReaderDLL for each installed version.   
        """
        installed_cst_versions = CSTRegInfo.find_cst_reg_version()
        for cst_version in installed_cst_versions:
            self.assertTrue(os.path.exists(CSTRegInfo.find_result_reader_dll(cst_version)))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()