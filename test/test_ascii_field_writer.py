"""Unit tests for ascii field writer.
"""
import os
import unittest
from cstmod.field_writer import ascii_field_writer

class TestASCIIFieldWriter(unittest.TestCase):
    """Unit tests for ascii field writer.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.project_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                            r'..',r'test_data',r'Simple_Cosim',
                                            r'Simple_Cosim_4',r'Export',r'3d'))

    def test_unittest_setup(self):
        """Test the unittest class setup.
        """
        self.assertTrue(True)

    def test_write_ascii_fields(self):
        """Test the write_ascii_fields function
        """
        print('project_dir: ', self.project_dir)
        self.assertTrue(os.path.exists(self.project_dir))
        ascii_field_writer(self.project_dir + 'h-field.h5')
        

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()