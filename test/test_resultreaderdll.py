"""
Unit tests for ResultReaderWrapper class.
"""
import os
import sys
import unittest
import ctypes
if sys.platform == "win32":
    from cstmod.dllreader import CSTProjHandle, ResultReaderDLL
else:
    sys.exit("Testing cstmod.dllreader is a Windows-only feature.")

class TestCSTResultReaderWrapper(unittest.TestCase):
    """
    TestCase class for testing CSTResultReaderDLL python wrapper.
    """
    @classmethod
    def setUpClass(cls):
        cst_test_file_name = os.path.join(os.path.abspath(os.path.join(__file__,'..','..','test_data','Simple_Cosim','Simple_Cosim.cst')))
        cls.cst_test_file_name = None
        if os.path.exists(cst_test_file_name):
            cls.cst_test_file_name = cst_test_file_name

    def setUp(self):
        self._rrdll_version = '2020'
        #self.rrdll = ResultReaderDLL()
        #self.projh = CSTProjHandle()


    def test_unittest_setup(self):
        """make sure the unit test frame work is properly initialized and 
        passes a known test.
        """
        self.assertTrue(True)

    def test_CSTProjHandle(self):
        """CST Project handle is a wrapped typedef struct that contains a handle 
        to the open CST project.  
        """
        projh = CSTProjHandle()
        self.assertIsInstance(projh, CSTProjHandle)
        self.assertTrue( hasattr(projh, 'm_pProj') )

    def test_dllversion(self):
        """Query the result reader version.
        """
        rrdll = ResultReaderDLL(self._rrdll_version)
        self.assertIsInstance(rrdll, ResultReaderDLL)
        self.assertEqual(rrdll.dll_version, 2020700)

    def test_ResultReaderDLL(self):
        """Test whether we can instantiate a ResultReaderDLL object
        """
        rrdll = ResultReaderDLL(self._rrdll_version)
        self.assertIsInstance(rrdll, ResultReaderDLL)

    def test_CSTProject_open_close(self):
        """Test the open/close project methods.
        """
        rrdll = ResultReaderDLL(self._rrdll_version)
        self.assertEqual(rrdll.open_project('fakename.cst'), 12)
        self.assertEqual(rrdll.open_project(self.cst_test_file_name), 0)
        rrdll.close_project()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()