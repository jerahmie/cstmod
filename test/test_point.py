"""
Unittests for Point class.
"""

import unittest
from cstmod import CSTPoint

class TestPoint(unittest.TestCase):
    """Test cases for Point class.
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.tp = CSTPoint()

    def test_setup(self):
        """Test the unittest framework setup.
        """
        self.assertTrue(True)

    def test_point(self):
        """Verify that a Point object can be instantiated.
        """
        self.assertIsInstance(CSTPoint(), object)
        self.assertIsInstance(self.tp, CSTPoint)
    
    def test_defaults(self):
        """Test the default values for Point()
        """
        myPoint = CSTPoint()
        self.assertAlmostEqual(0.0, myPoint.x)
        self.assertAlmostEqual(0.0, myPoint.y)
        self.assertAlmostEqual(0.0, myPoint.z)

    def test_equality_operator(self):
        """Test the __eq__ definition in point.
        """
        self.assertNotEqual(CSTPoint(0.0, 1.1, 2.2), CSTPoint(3.3, 4.4, 5.5))
        self.assertAlmostEqual(CSTPoint(1.1, 2.2, 3.3), CSTPoint(1.1, 2.2, 3.3))
        self.assertEqual(CSTPoint(9.9, 8.8, 7.7), CSTPoint(9.9, 8.8, 7.7))

    def test_bad_types(self):
        """Test that TypeError is thrown if attempt to assign non-number quantity to points.
        """
        with self.assertRaises(TypeError):
            CSTPoint('0', 0, 0)
            CSTPoint(0,'1', 10)
            CSTPoint(2,1,'5')

    def test_setters_getters(self):
        """Test the setters and getters.
        """
        self.tp.x = 12.5
        self.tp.y = 8.3
        self.tp.z = -9.15
        self.assertAlmostEqual(12.5, self.tp.x)
        self.assertAlmostEqual(8.3, self.tp.y)
        self.assertAlmostEqual(-9.15, self.tp.z)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if "__main__" == __name__:
    unittest.main()
