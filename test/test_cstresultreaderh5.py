""" Unit testing file for field_reader_h5.py
"""
import os
import sys
import unittest

from cstmod.field_reader import FieldReaderH5, extract_field_type

class Test(unittest.TestCase):
    """ Unit testing FieldReaderH5
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.h5dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      r'..',r'test_data',r'Simple_Cosim',
                                      r'Simple_Cosim_4',r'Export',r'3d'))
        self.unsorted_files = [os.path.join(self.h5dir,hf5) for hf5 in os.listdir(self.h5dir)]

    def test_unittest_config(self):
        self.assertTrue(True)

    def test_extract_field_type(self):
        self.assertEqual(r'h-field', extract_field_type(self.unsorted_files[0]))

    def test_field_reader(self):
        fr = FieldReaderH5(self.unsorted_files[0])
        

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()