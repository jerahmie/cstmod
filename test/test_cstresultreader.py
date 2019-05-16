#!/usr/bin/env python
"""
Test CstResultReader adapter class
"""
import os
from os.path import normpath, realpath, join
import numpy as np
import scipy.io as spio
import unittest
from cstmod.cstutil import CSTRegInfo
from cstmod import CSTResultReader, CSTMaterialType, CSTBoundaryType, CSTFieldMonitor
cstmod_test_data_dir = normpath(join(realpath(__file__),
                                              r'..', r'..',
                                              r'Test_Data'))

cst_test_data = {}
cst_test_data['nchannels'] = 7
cst_test_data['frequency_scale'] = 1000000
cst_test_data['nx'] = 450
cst_test_data['ny'] = 277
cst_test_data['nz'] = 327

class TestCSTMaterialType(unittest.TestCase):
    """Test the unumeration class for CST material matrix types.
    """
    def test_material_type_enum(self):
        """Verify enumerations values.
        """
        self.assertEqual(0, CSTMaterialType.EPS.value)
        self.assertEqual(1, CSTMaterialType.MUE.value)
        self.assertEqual(2, CSTMaterialType.KAPPA.value)
        self.assertEqual(3, CSTMaterialType.RHO.value)

class TestResultReaderSetup(unittest.TestCase):
    """Unittests that do not require valid cst project handle.
    """
    def setUp(self):
        """Create a valid CSTResultReader
        """
        self.cst_version = r'2018'
        self.rr = CSTResultReader(self.cst_version)
        self.cst_project_path = os.path.join(cstmod_test_data_dir,
                                             r'simple_cosim_7T.cst')

    def test_open_bad_project(self):
        """Ensure an exception is raised if the project does not exist.
        """
        with self.assertRaises(Exception):
            self.rr.open_project("D:\workspace\cstmod\Test_Data\fake_proj.cst")
        self.rr.close_project()

    def test_open_project(self):
        """Opens a CST Project and creates a handle. 
        """
        self.rr.open_project(self.cst_project_path)
        self.rr.close_project()

class TestCstResultReader(unittest.TestCase):
    """Unittests for CSTResultReader interface class.
    """
    @classmethod
    def setUpClass(cls):
        print("Executing tests in " + __file__)

    def setUp(self):
        self.cst_version = r'2018'
        self.rr = CSTResultReader(self.cst_version)
        self.cst_project_path = os.path.join(cstmod_test_data_dir,
                                             r'simple_cosim_7T.cst')
        self.rr.open_project(self.cst_project_path)

    def testSetup(self):
        """Test the unittest setup.
        """
        self.assertEqual(1,1)

    def test_get_dll_version(self):
        """Returns the CSTResultReader version"""
        if '2018' == self.cst_version:
            cst_dll_version = 2018600
        self.assertEqual(cst_dll_version, self.rr.dll_version)

    def test_get_frequency_range(self):
        """Tests the frequency range of the project.
        """
        freq_scale = self.rr.get_frequency_scale()
        self.assertEqual(cst_test_data['frequency_scale'], freq_scale)

    def test_get_number_of_results(self):
        """Check returns the total number of results available for the selected result tree item.
        """
        results = self.rr.query_result_names("S-Parameter")
        self.assertEqual(cst_test_data['nchannels']**2, len(results))
        results = self.rr.query_result_names("2D/3D Results")
        self.assertEqual(cst_test_data['nchannels']*3, len(results))
        
    def test_get_material_matrix(self):
        """Extract the material matrices and test the values make sense.
        """
        xdim, ydim, zdim = self.rr.load_grid_data()
        epsx, epsy, epsz = self.rr.load_grid_mat_data(CSTMaterialType.EPS.value)
        muex, muey, muez = self.rr.load_grid_mat_data(CSTMaterialType.MUE.value)
        #kappax, kappay, kappaz = self.rr.load_grid_mat_data(2)
        rhox, rhoy, rhoz = self.rr.load_grid_mat_data(CSTMaterialType.RHO.value)
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(epsx))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(epsy))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(epsz))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(muex))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(muey))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(muez))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(rhox))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(rhoy))
        self.assertEqual((cst_test_data["nz"], cst_test_data["ny"], cst_test_data["nx"]), np.shape(rhoz))
        export_dict = {}
        export_dict["xdim"] = xdim
        export_dict["ydim"] = ydim
        export_dict["zdim"] = zdim
        export_dict["epsx"] = epsx
        export_dict["epsy"] = epsy
        export_dict["epsz"] = epsz
        export_dict["muex"] = muex
        export_dict["muey"] = muey
        export_dict["muez"] = muez
        export_dict["rhox"] = rhox
        export_dict["rhoy"] = rhoy
        export_dict["rhoz"] = rhoz

        spio.savemat("test_save.mat", export_dict, oned_as='column')

    def test_get_field_monitor_data(self):
        """Find field monitor data for given field type.  Verify dimensions of field monitor.
        """
        self.assertAlmostEqual(h_field_monitor_min.x, xdim[0])

        
    def test_get_boundaries(self):
        """Extract boundary info from project.
        """
        n_boundary = self.rr.load_grid_boundaries()
        self.assertEqual(CSTBoundaryType.PML_expanded.value, n_boundary[0])
        self.assertEqual(CSTBoundaryType.PML_expanded.value, n_boundary[1])
        self.assertEqual(CSTBoundaryType.PML_expanded.value, n_boundary[2])
        self.assertEqual(CSTBoundaryType.PML_expanded.value, n_boundary[3])
        self.assertEqual(CSTBoundaryType.PML_expanded.value, n_boundary[4])
        self.assertEqual(CSTBoundaryType.PML_expanded.value, n_boundary[5])


    def test_get_hex_mesh_info(self):
        """Extract hexahedral mesh data from project.
        """
        result = self.rr.load_grid_data()
        self.assertEqual(cst_test_data["nx"], self.rr._nx)
        self.assertEqual(cst_test_data["ny"], self.rr._ny)
        self.assertEqual(cst_test_data["nz"], self.rr._nz)
        self.assertEqual(cst_test_data["nx"], len(result[0]))
        self.assertEqual(cst_test_data["ny"], len(result[1]))
        self.assertEqual(cst_test_data["nz"], len(result[2]))

    def test_get_3d_hex_result_info(self):
        """Queries info about 3-D field monitor.
        """
        e_field = self.rr.load_data_3d('2D/3D Results\\E-Field\\e-field (f=297) [1]')
        expected_data_size = cst_test_data["nx"]  * cst_test_data["ny"] * cst_test_data["nz"] * 6
        self.assertEqual((expected_data_size,), np.shape(e_field))

    def tearDown(self):
        self.rr.close_project()
    
    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
