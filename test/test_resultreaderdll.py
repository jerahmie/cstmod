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
        #cst_test_file_name = os.path.join("D:\\", 'CST_Projects','Simple_Cosim.cst')
        cls.cst_test_file_name = None
        if os.path.exists(cst_test_file_name):
            cls.cst_test_file_name = cst_test_file_name

    def setUp(self):
        self._rrdll_version = '2020'
        self.rrdll = ResultReaderDLL(self.cst_test_file_name, self._rrdll_version)
        self.rrdll.open_project()

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
        self.assertIsNotNone(rrdll._projh.m_pProj)
        rrdll.close_project()
        self.assertIsNone(rrdll._projh.m_pProj)

    def test_get_item_names(self):
        """Test the get_item_names method. 
        """
        self.assertTrue( hasattr(self.rrdll, 'item_names') )
        #close the default project, if open
        if self.rrdll._projh.m_pProj is not None:
            self.rrdll.close_project()
        nresults_balance = 0
        one_d_results_balance = ''
        with ResultReaderDLL(self.cst_test_file_name, self._rrdll_version) as results:
            hasattr_result = hasattr(results, 'item_names' )
            one_d_results_balance = results.item_names('1D Results\Balance')
        self.assertTrue(hasattr_result)
        self.assertEqual(3, len(one_d_results_balance))
        self.assertEqual(one_d_results_balance,
                         ['1D Results\\Balance\\Balance [1]',
                          '1D Results\\Balance\\Balance [2]',
                          '1D Results\\Balance\\Balance [3]'])

    def test_get_one_d_results(self):
        """More tests for 1D Results
        """
        one_d_results = self.rrdll.item_names('1D Results')
        char_sum = 0
        for res in one_d_results:
            char_sum += len(res)
        self.assertEqual(149, len(self.rrdll.item_names('1D Results')))

    def test_get_number_of_results(self):
        """Tests for CST_GetNumberOfResults
        """
        self.assertTrue( hasattr(self.rrdll, 'number_of_results') )
        self.assertEqual(1, self.rrdll.number_of_results('1D Results\Balance\Balance [1]'))

    def test_cst_project_path(self):
        """project_path - returns the CST project path for the project handle.
        This will be implemented as a parameter to retrieve the project path.
        """
        self.assertEqual(os.path.join(os.path.splitext(self.cst_test_file_name)[0],
                                      'Result\\'), self.rrdll.project_result_path)
        self.assertEqual(os.path.join(os.path.splitext(self.cst_test_file_name)[0],
                                      'Model\\3D\\'), self.rrdll.project_3d_result_path)


    def test_get_1d_result_info(self):
        """Test the get_1d_result_info function
        """
        self.assertTrue( hasattr(self.rrdll, '_get_1d_result_info'))

    def tearDown(self):
        self.rrdll.close_project()

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()