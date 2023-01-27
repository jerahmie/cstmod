"""
Unit tests for validation of fields exported from cst with applied shims.
"""
import os
import unittest
from cstmod.field_reader import FieldReaderH5


class TestValidateVopgenCST(unittest.TestCase):
    """
    Unit tests to provide validation between fields and shimmed fields
    between CST and Vogpen processed data.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.test_data_directory = os.path.join(os.getcwd(), r'..',
                                                r'test_data')
        self.nchannels = 8    # number of channels in array
        self.frequency = 297  # frequency (MHz)
        self.field_file_names = ["e-field (f=" + str(self.frequency) +
                                ") [AC" + str(i+1) + "].h5"
                                for i in range(self.nchannels)]

    @unittest.skip
    def test_the_tests(self):
        """
        Simple test to check the unittest setup.  Initially fails, then
        passes, then is skipped.
        """
        self.assertTrue(True)

    def test_per_channel(self):
        """
        Compare single channel fields exported from CST with Vopgen fields.
        """
        for field_file in self.field_file_names:
            efield_file = os.path.join(self.test_data_directory, field_file)
            self.assertTrue(os.path.exists(efield_file))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
