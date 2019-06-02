"""
Unit tests for CSTmod utilities
"""

import unittest
from cstmod import CSTErrorCodes


class TestCSTModUtilities(unittest.TestCase):
    """Tests for CSTmod utilities.
    """
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def testClassConfiguration(self):
        """Ensure the unittest configuration is valid
        """
        self.assertEqual(1,1)

    def testCSTErrorCodes(self):
        """Verify ERROR_CODE_MEMORY
        """
        self.assertEqual(CSTErrorCodes.ERROR_UNKNOWN.value, 1)
        self.assertEqual(CSTErrorCodes.ERROR_FILE_NOT_FOUND.value, 2)
        self.assertEqual(CSTErrorCodes.ERROR_PROJECT_FILE_NOT_VALID.value, 3)
        self.assertEqual(CSTErrorCodes.ERROR_RESULT_TREE_ITEM_NOT_FOUND.value, 4)
        self.assertEqual(CSTErrorCodes.ERROR_REQUESTED_RESULT_DOES_NOT_CORRESPOND.value, 5)
        self.assertEqual(CSTErrorCodes.ERROR_BAD_FUNCTION_ARGUMENT.value, 6)
        self.assertEqual(CSTErrorCodes.ERROR_INCOMPATIBLE_RESULT_TYPE.value, 7)
        self.assertEqual(CSTErrorCodes.ERROR_CODE_MEMORY.value, 8)
        self.assertEqual(CSTErrorCodes.ERROR_UNSUPPORTED_MESH_TYPE.value, 9)
        self.assertEqual(CSTErrorCodes.ERROR_VERSION_CONFLICT.value, 10)
        self.assertEqual(CSTErrorCodes.ERROR_CST_PROJECT_IN_USE.value, 11)
        self.assertEqual(CSTErrorCodes.ERROR_UNPACKED_PROJECT_FOLDER.value, 12)


    
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass



if "__main__" == __name__:
    unittest.main()
