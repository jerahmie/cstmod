"""
Unit tests for CSTFieldWriter
"""
import os
import unittest
from cstmod import CSTFieldWriter, CSTResultReader, CSTFieldWriterNonUniform

class TestCSTFieldWriter(unittest.TestCase):
    """TestCase implementation for TestCSTFieldWriter class.
    """
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(self):
        """Create a CSTFieldWriter that's available for all tests.
        """
        cstmod_test_data_dir = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                                                              r'..', r'..',
                                                                              r'Test_Data'))

        self.cst_project_path = os.path.join(cstmod_test_data_dir,
                                             r'simple_cosim_7T.cst')
        self.rr = CSTResultReader('2018')
        self.rr.open_project(self.cst_project_path)
        self.fw = CSTFieldWriterNonUniform(self.rr)
        self.outputfile = 'test.mat'
        if os.path.exists('test.mat'):
            os.remove(self.outputfile)

    def test_testcase_setup(self):
        """Ensure the TestCase is setup correctly.
        """
        self.assertEqual(1,1)

    def test_cstfieldwriter_hierarchy(self):
        """Verify CSTFieldWriter is an object.
        """
        self.assertIsInstance(self.fw, CSTFieldWriterNonUniform)
        self.assertIsInstance(self.fw, CSTFieldWriter)
        self.assertIsInstance(self.fw.rr, CSTResultReader)

    def test_writer_non_uniform(self):
        if os.path.exists('test_e_field.mat'):
            os.remove('test_e_field.mat')
        if os.path.exists('test_h_field.mat'):
            os.remove('test_h_field.mat')

        self.fw.write('test_e_field.mat', 'e-field')
        self.assertTrue(os.path.exists('test_e_field.mat'))
        self.fw.write('test_h_field.mat', 'h-field')
        self.assertTrue(os.path.exists('test_h_field.mat'))
        

    def tearDown(self):
        self.rr.close_project()
    
    @classmethod
    def tearDownClass(cls):
        pass

if "__main__" == __name__:
    unittest.main()
