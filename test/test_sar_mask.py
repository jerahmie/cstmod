"""
Unit tests for SAR mask calculations from CST field data.
"""
import os
import numpy as np
import unittest
import hdf5storage
from cstmod.field_reader import FieldReaderCST2019
from cstmod.vopgen import SARMaskCST2019

class TestSARMaskCST2019(unittest.TestCase):
    """Unit tests class for SAR mask.
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.project_test_dir = os.path.abspath(os.path.dirname(__file__))
        self.project_test_data_dir = os.path.abspath(os.path.join(self.project_test_dir, '..', 'Test_Data'))

        if not os.path.exists(self.project_test_dir):
            raise FileNotFoundError
        if not os.path.exists(self.project_test_data_dir):
            raise FileNotFoundError
        
        self.sarmask_filename = os.path.join(self.project_test_data_dir,
                                             'sarmask_aligned.mat')

        if os.path.exists(self.sarmask_filename):
            os.remove(self.sarmask_filename)


        self.field_reader = FieldReaderCST2019()
        self.xdim = np.arange(0,100)
        self.ydim = np.arange(0,100)
        self.zdim = np.arange(0,100)
        self.sigma = np.zeros((len(self.xdim),
                               len(self.ydim),
                               len(self.zdim)),
                              dtype = np.double)
        self.epsr = np.zeros((len(self.xdim),
                              len(self.ydim),
                              len(self.zdim)),
                             dtype = np.double)

        self.sigma[39:60, 39:60, 39:60] = 0.5
        self.epsr[39:60, 39:60, 39:60] = 55.0

    def test_the_tests(self):
        """Ensure unittest framework is set up correctly.
        """
        self.assertTrue(True)

    def test_sarmask(self):
        """Test reading of fields.
        """
        sarmask = SARMaskCST2019(447.0, self.xdim, self.ydim, self.zdim, 
                                 self.epsr, self.sigma)

        self.assertAlmostEqual(sarmask.sigma_max, 1.0)
        self.assertAlmostEqual(sarmask.sigma_min, 0.1)
        self.assertAlmostEqual(sarmask.epsr_min, 2.0)
        self.assertAlmostEqual(sarmask.epsr_max, 100.0)
        sarmask.sigma_max = 0.7
        sarmask.sigma_min = 0.4
        sarmask.epsr_min = 10.0
        sarmask.epsr_max = 60.0
        self.assertAlmostEqual(sarmask.sigma_max, 0.7)
        self.assertAlmostEqual(sarmask.sigma_min, 0.4)
        self.assertAlmostEqual(sarmask.epsr_min, 10.0)
        self.assertAlmostEqual(sarmask.epsr_max, 60.0)
        testmask  = sarmask.sarmask
        self.assertEqual(np.shape(testmask), (100,100,100))
        self.assertEqual(0, np.size(np.where(testmask > 1)))
        self.assertEqual(0, np.size(np.where(testmask < 0)))
        self.assertNotEqual(0, np.size(np.where(testmask == 1)))
        self.assertNotEqual(0, np.size(np.where(testmask == 0)))

        print('sarmask_filename: ', self.sarmask_filename)
        sarmask.write_sarmask(self.sarmask_filename)
        self.assertTrue(os.path.exists(self.sarmask_filename))
        
        sardict = hdf5storage.loadmat(self.sarmask_filename)
        self.assertTrue(len(sardict['XDim']), 100)
        self.assertTrue(len(sardict['YDim']), 100)
        self.assertTrue(len(sardict['ZDim']), 100)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if "__main__" == __name__:
    unittest.main()
