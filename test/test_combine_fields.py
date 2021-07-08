"""
Unit tests for ResultReaderWrapper class.
"""
import os
import sys
import unittest
import tempfile
import functools
import fnmatch
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
            self.results_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                            r'..',
                                            r'test_data',r'Simple_Cosim',
                                            r'Simple_Cosim_4',r'Export'))
        else:
            self.results_dir = ''
        
        self.frequency = 63.65

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
        port_voltage_path = os.path.join(ac_combine_dirs[0], r'FD Voltages',r'P1.txt')
        print('P1: ', data_1d_at_frequency(port_voltage_path, 63.65))
        #self.assertTrue(np.allclose(data_1d_at_frequency(port_voltage_path, 63.65),np.array([63.65, 0.12405656, -1.4993948])))

    def test_data_from_ports(self):
        """Get data and test results
        """
        voltages_dir = os.path.join(self.results_dir,r'AC1',r'FD Voltages')
        port_voltages = data_from_ports(voltages_dir, 63.65)
        self.assertEqual(np.shape(port_voltages),(5,))
        print(port_voltages)

    def test_sorting_many_AC_combines(self):
        """Create a large number of AC combine targets and make sure they are sorted 
        by the trailing number.
        """
        sorted_ac_combine_dirs = []
        with tempfile.TemporaryDirectory() as tempdir:
            for i in range(128):
                os.mkdir(os.path.join(tempdir, r'AC'+str(i)))
                sorted_ac_combine_dirs.append(os.path.join(tempdir, r'AC' + str(i)))
            unsorted_ac_combine_dirs = [os.path.join(tempdir, dir1) for dir1 in os.listdir(tempdir)]

        self.assertTrue(functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, sorted_ac_combine_dirs, sort_by_trailing_number(unsorted_ac_combine_dirs)),True))

    def test_find_missing_data(self):
        """Test utility function to find items missing in sequence.
        """
        sorted_port_dirs = []
        with tempfile.TemporaryDirectory() as tempdir:
            for i in range(1,228):
                if i%112 != 0:
                    open(os.path.join(tempdir,'P'+str(i)+'.txt'),'a').close()
            sorted_port_dirs = sort_by_trailing_number([os.path.join(tempdir, d) for d in os.listdir(tempdir)])
        print(sorted_port_dirs)
        print(len(sorted_port_dirs))
        missing_files = find_missing_data(sorted_port_dirs, 228, "P*.txt")
        print(missing_files)
        self.assertEqual(len(missing_files),2)

    def test_sorting_port_data(self):
        """Check that list of Port
        """
        sorted_port_file_names = []
        with tempfile.TemporaryDirectory() as tempdir:
            ac_path = os.path.join(tempdir,r'AC1')
            os.mkdir(ac_path)
            self.assertTrue(os.path.exists(ac_path))
            for i in range(500):
                port_file_name = os.path.join(ac_path,'Port'+str(i+1)+'.txt')
                sorted_port_file_names.append(port_file_name)
                with open(port_file_name,'wb') as fp:
                    pass # create empty file for sorting
            unsorted_port_file_names = list(os.path.join(ac_path,pf) for pf in os.listdir(ac_path))

            self.assertFalse(functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, sorted_port_file_names, unsorted_port_file_names)),True)
            self.assertTrue(functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, sorted_port_file_names, sort_by_trailing_number(unsorted_port_file_names))),True)

    def test_power_from_ports(self):
        """evaluate the power at each port for a given combine.
        """
        ac_results_path = sort_by_trailing_number([os.path.join(self.results_dir, path) for path in fnmatch.filter(os.listdir(self.results_dir),'AC*')])
        nports = len(data_from_ports(os.path.join(ac_results_path[0],r'FD Voltages'), self.frequency))
        powers = np.empty((len(ac_results_path), nports))
        print('powers shape: ', np.shape(powers))
        print(powers)
        for i, ac_result in enumerate(ac_results_path):
            print('i: ', i)
            print('ac_result: ', ac_result)
            powers[i,:] = power_from_ports(ac_result, self.frequency)
        self.assertEqual(np.shape(powers), (len(ac_results_path), nports))
        print('powers: ', powers, np.shape(powers))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()