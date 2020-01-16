"""Unit tests for handling arrays of CST exported data.
"""
import os
import unittest
from cstmod.field_reader import DataNArrayABC, GenericDataNArray

class TestOneDimemensionalCSTData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'test_data',
                                             'Export'))
        print(self.test_data_dir)
        print("---->>>> ", os.path.exists(self.test_data_dir))
        self.gdr = GenericDataNArray()

    def test_config(self):
        self.assertTrue(True)

    def test_generic_data_reader_object(self):
        """Create an instance of Gereric data reader object.
        """
        gdr_empty = GenericDataNArray()
        self.assertEqual(gdr_empty.nchannels, 0)
        self.assertEqual(gdr_empty.data_shape, None)
        self.assertEqual(gdr_empty.data_length, 0)  
        gdr_empty.nchannels = 16
        self.assertEqual(gdr_empty.nchannels, 16)

    def test_process_file_list(self):
        """Make sure file lists are processed correctly.
        """
        #file_name_pattern = "Power_Excitation (AC*)_Power Accepted (DS).txt"
        file_name_pattern = os.path.join(self.test_data_dir,
                                         "Power_Excitation*(DS).txt")

        print(file_name_pattern)
        file_list = self.gdr._process_file_list(file_name_pattern)
        self.assertEqual(len(file_list), 16)
        self.gdr.load_data_one_d(file_name_pattern)
        self.assertEqual(self.gdr.nchannels, 16)
        self.assertEqual(self.gdr.data_shape, (1001,16))
        self.assertEqual(self.gdr.data_length, 1001)
        
        f0, power_admitted = self.gdr.nchannel_data_at_val(447.0)
        self.assertEqual(len(power_admitted), 16)
        print("f0: ", f0, ", power_admitted: ", power_admitted)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if "__main__" == __name__:
    unittest.main()