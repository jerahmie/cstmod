"""
Unit tests for ResultReaderWrapper class.
"""
import os
import sys
import unittest
import tempfile
import functools
import numpy as np
from cstmod.cstutil import *
from cstmod.cosimulation import *

class Test(unittest.TestCase):
    """
    Testing class for CSTCosimReader
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        if sys.platform == 'win32':
            self.results_dir = os.path.join(__file__, r'..', r'..',
                                            r'test_data',r'Simple_Cosim',
                                            r'Simple_Cosim_4',r'Export')
        else:
            self.results_dir = ''

    def test_test_config(self):
        """Test the unittest configuration
        Makes sure testing framework 
        """
        self.assertTrue(True)

    def test_data_1d_at_frequency(self):
        """Test data_1d_at_frequency 
        """
        self.assertTrue(os.path.exists(self.results_dir))
        ac_combine_dirs = sort_by_trailing_number(find_cst_files(os.path.join(self.results_dir,'AC*')))
        self.assertEqual(len(ac_combine_dirs),2)
        self.assertEqual(os.path.join(self.results_dir, r'AC1'), ac_combine_dirs[0])
        self.assertEqual(os.path.join(self.results_dir, r'AC2'), ac_combine_dirs[1])
        port_voltage_path = os.path.join(ac_combine_dirs[0], r'FD Voltages',r'Port1.txt')
        print(data_1d_at_frequency(port_voltage_path, 63.65))
        self.assertTrue(np.allclose(data_1d_at_frequency(port_voltage_path, 63.65),np.array([63.65, 0.12405656, -1.4993948])))

    def test_data_from_ports(self):
        

    def test_sorting_many_AC_combines(self):
        """Create a large number of AC combine targets and make sure they are sorted 
        by the trailing number.
        """
        sorted_ac_combine_dirs = []
        with tempfile.TemporaryDirectory() as tempdir:
            for i in range(128):
                os.mkdir(os.path.join(tempdir, 'AC'+str(i)))
                sorted_ac_combine_dirs.append(os.path.join(tempdir, 'AC' + str(i)))
            unsorted_ac_combine_dirs = [os.path.join(tempdir, dir1) for dir1 in os.listdir(tempdir)]

        self.assertTrue(functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, sorted_ac_combine_dirs, sort_by_trailing_number(unsorted_ac_combine_dirs)),True))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()