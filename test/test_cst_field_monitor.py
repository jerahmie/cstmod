"""
Unittests for CSTFieldMonitor class.
"""
import os
import unittest
from cstmod import CSTFieldMonitor, CSTPoint

class TestCSTFieldMonitor(unittest.TestCase):
    """
    TestCases for CSTFieldMonitor metadata reader.
    """
    @classmethod
    def setUpClass(cls):
        cls.field_monitor_rex_file = os.path.normpath(os.path.join(__file__, r'..', r'..', 'Test_Data',
        r"e-field (f=297)_1,1_m3d.rex"))
        cls.e_field_monitor_data = {}
        cls.e_field_monitor_data['simulation_domain_min'] = [-315.8505554199, -315.9505615234, -252.3505554199]
        cls.e_field_monitor_data['simulation_domain_max'] = [315.8505554199, 315.8505554199, 404.7505493164]
        cls.e_field_monitor_data['subvolume_min'] = [-63.5, -63.59999847412, 0.0]
        cls.e_field_monitor_data['subvolume_max'] = [63.5, 63.5, 152.3999938965]
    
    def setUp(self):
        self.fm = CSTFieldMonitor(self.field_monitor_rex_file)

    def test_framework(self):
        """Test the unittest framework setup.
        """
        self.assertEqual(1,1)

    def test_field_monitor_file(self):
        """Verify field monitor file can be found.
        """
        self.assertTrue(os.path.exists(self.field_monitor_rex_file))

    def test_create_field_monitor(self):
        """Create a field monitor and assert that it is an object.
        """
        self.assertIsInstance(CSTFieldMonitor(self.field_monitor_rex_file), object)
        self.assertIsInstance(self.fm, CSTFieldMonitor)
        self.assertIsInstance(self.fm._simulation_domain_max, CSTPoint)


    def test_simulation_domain(self):
        """Assert simulation domain is found correctly.
        """
        self.assertAlmostEqual(self.fm.simulation_domain_min.x, self.e_field_monitor_data['simulation_domain_min'][0])
        self.assertAlmostEqual(self.fm.simulation_domain_min.y, self.e_field_monitor_data['simulation_domain_min'][1])
        self.assertAlmostEqual(self.fm.simulation_domain_min.z, self.e_field_monitor_data['simulation_domain_min'][2])

        self.assertAlmostEqual(self.fm.simulation_domain_max.x, self.e_field_monitor_data['simulation_domain_max'][0])
        self.assertAlmostEqual(self.fm.simulation_domain_max.y, self.e_field_monitor_data['simulation_domain_max'][1])
        self.assertAlmostEqual(self.fm.simulation_domain_max.z, self.e_field_monitor_data['simulation_domain_max'][2])

    def test_subvolume(self):
        """Assert subvolume of simulation domain is found correctly."""
        self.assertAlmostEqual(self.fm.subvolume_min.x, self.e_field_monitor_data['subvolume_min'][0])
        self.assertAlmostEqual(self.fm.subvolume_min.y, self.e_field_monitor_data['subvolume_min'][1])
        self.assertAlmostEqual(self.fm.subvolume_min.z, self.e_field_monitor_data['subvolume_min'][2])

        self.assertAlmostEqual(self.fm.subvolume_max.x, self.e_field_monitor_data['subvolume_max'][0])
        self.assertAlmostEqual(self.fm.subvolume_max.y, self.e_field_monitor_data['subvolume_max'][1])
        self.assertAlmostEqual(self.fm.subvolume_max.z, self.e_field_monitor_data['subvolume_max'][2])                        

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    

if "__main__" == __name__:
    unittest.main()

