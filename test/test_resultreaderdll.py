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
        #cst_test_file_name = os.path.join(os.path.abspath(os.path.join(__file__,'..','..','test_data','Simple_Cosim','Simple_Cosim.cst')))
        cst_test_file_name = os.path.join("D:\\", 'CST_Projects','Simple_Cosim.cst')
        cls.cst_test_file_name = None
        if os.path.exists(cst_test_file_name):
            cls.cst_test_file_name = cst_test_file_name

    def setUp(self):
        self._rrdll_version = '2020'
        print('test_file: ', self.cst_test_file_name)
        self.rrdll = ResultReaderDLL(self.cst_test_file_name, self._rrdll_version)
        self.rrdll.open_project()
        print(self.rrdll._projh.m_pProj)

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
        rrdll = ResultReaderDLL(self.cst_test_file_name, self._rrdll_version)
        self.assertIsInstance(rrdll, ResultReaderDLL)
        self.assertEqual(rrdll.dll_version, 2020700)
        self.assertEqual(self.rrdll.dll_version, 2020700)

    def test_ResultReaderDLL(self):
        """Test whether we can instantiate a ResultReaderDLL object
        """
        rrdll = ResultReaderDLL(self.cst_test_file_name, self._rrdll_version)
        self.assertIsInstance(rrdll, ResultReaderDLL)
        
    def test_CSTProject_open_close(self):
        """Test the open/close project methods.
        """
        if self.rrdll._projh.m_pProj is not None:
            self.rrdll.close_project()
            
        rrdll = ResultReaderDLL(self.cst_test_file_name, self._rrdll_version)
        rrdll.open_project()
        print('test_CSTProject_open_close: ', rrdll._cst_project_file)
        self.assertIsNotNone(rrdll._projh.m_pProj)
        rrdll.close_project()
        self.assertIsNone(rrdll._projh.m_pProj)

    def test_get_item_names(self):
        """Test the get_item_names method. 
        """
        print(self.rrdll._projh.m_pProj)
        self.assertTrue( hasattr(self.rrdll, 'get_item_names') )
        # close the default project, if open
        if self.rrdll._projh.m_pProj is not None:
            self.rrdll.close_project()

        with ResultReaderDLL(self.cst_test_file_name, self._rrdll_version) as results:
            self.assertTrue( hasattr(results, 'get_item_names' ))
        #self.assertEqual(self.rrdll.get_item_names('1D Results\Balance'),
        #                 (0,'1D Results\Balance'))
        #self.assertEqual(self.rrdll.get_item_names('1D Results'),
        #                 (0,'1D Results'))
        #self.assertEqual(self.rrdll.get_item_names('1D Results\Balance'),
        #                 (0,'1D Results\Balance'))

    def tearDown(self):
        self.rrdll.close_project()

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()