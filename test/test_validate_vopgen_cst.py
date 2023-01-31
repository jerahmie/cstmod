#!/usr/bin/env python
"""
Unit tests for validation of fields exported from cst with applied shims.
"""
import os
import unittest
import numpy as np
import hdf5storage
import matplotlib.pyplot as plt
from cstmod.field_reader import FieldReaderH5



def apply_shim(fields: np.ndarray, mags: np.ndarray, phases: np.ndarray) -> np.ndarray:
    """
    Apply a magnitude and phase shim to the exported fields.
    Args:
        fields: (nx,ny,nz,3,nchannels) ndarray complex field values in the vopgen-format
        mags: (1xnchannels) ndarray of shim magnitudes
        phases: (1,nchannels) ndarray of phase magnitudes

    Returns:
        ndarray: (nx,ny,nz,3) complex field components with mag/phase shim applied
    """
    fields_shape =  np.shape(fields)
    nchannels = fields_shape[-1]
    assert len(mags) == len(phases), "Unequal number of magnitudes and phases."
    assert len(mags) == nchannels, "Magnitudes and phases must equal number of field channels."
    
    # apply shim
    ef_shim = np.zeros(fields_shape[0:4], dtype=np.complex128)
    for ch in range(nchannels):
        ef_shim += mags[ch]*fields[:,:,:,:,ch]*np.exp(-1.0j*phases[ch])

    return ef_shim

class TestValidateVopgenCST(unittest.TestCase):
    """
    Unit tests to provide validation between fields and shimmed fields
    between CST and Vogpen processed data.
    """
    @classmethod
    def setUpClass(cls):
        cst_export_dir = os.path.join(r'/export',r'data2',
                r'jerahmie-data',r'PTx_Knee_7T',
                r'Knee_pTx_7T_DB_Siemens_Duke_One_Legs_Fields_retune_20230124_2', r'Export')
        cls.cst_export_3d_dir = os.path.join(cst_export_dir, '3d')
        cls.cst_export_vopgen_dir = os.path.join(cst_export_dir, 'Vopgen')

    def setUp(self):
        self.test_data_directory = os.path.join(os.getcwd(), r'..',
                                                r'test_data')
        self.nchannels = 8    # number of channels in array
        self.frequency = 297  # frequency (MHz)
        self.field_file_names = ["e-field (f=" + str(self.frequency) +
                                ") [AC" + str(i+1) + "].h5"
                                for i in range(self.nchannels)]
        self.cst_efields_file_name = "e-field (f=" + str(self.frequency) + ") [CP].h5"


    @unittest.skip
    def test_the_tests(self):
        """
        Simple test to check the unittest setup.  Initially fails, then
        passes, then is skipped.
        """
        self.assertTrue(True)

    @unittest.skip("Currently passes.  Skipping for time.")
    def test_per_channel(self):
        """
        Compare single channel fields exported from CST with Vopgen fields.
        """
        self.assertTrue(os.path.exists(self.cst_export_3d_dir))
        self.assertTrue(os.path.exists(self.cst_export_vopgen_dir))
        vopgen_file_name = os.path.join(self.cst_export_vopgen_dir,
                'efMapArrayN.mat')
        self.assertTrue(os.path.exists(vopgen_file_name))
        # load Vopgen dictionary
        vopgen_dict = hdf5storage.loadmat(vopgen_file_name)
        vopgen_xdim = vopgen_dict['XDim']
        vopgen_ydim = vopgen_dict['YDim']
        vopgen_zdim = vopgen_dict['ZDim']

        for i in range(self.nchannels):
            print("Compare channel: ", str(i))
            # load vopgen data
            vopgen_efield = np.transpose(vopgen_dict['efMapArrayN'][:,:,:,:,i],(2,1,0,3))
            # load CST E-field file
            cst_field_file_name = self.field_file_names[i]
            cst_field_file = os.path.join(self.cst_export_3d_dir,
                cst_field_file_name)
            self.assertTrue(os.path.exists(cst_field_file))
            print(cst_field_file)
            print(vopgen_file_name)
            efield_fr = FieldReaderH5(cst_field_file)
            cst_efield = efield_fr.fields
            cst_xdim = efield_fr.xdim/1000.0
            cst_ydim = efield_fr.ydim/1000.0
            cst_zdim = efield_fr.zdim/1000.0
            # check result shapes
            self.assertEqual(np.shape(cst_efield),
                (len(cst_zdim), len(cst_ydim), len(cst_xdim),3))
            self.assertEqual(len(vopgen_xdim), len(cst_xdim))
            self.assertEqual(len(vopgen_ydim), len(cst_ydim))
            self.assertEqual(len(vopgen_zdim), len(cst_zdim))
            self.assertEqual(np.shape(vopgen_efield), np.shape(cst_efield))
            # compare values
            self.assertTrue(np.allclose(vopgen_xdim, cst_xdim))
            self.assertTrue(np.allclose(vopgen_ydim, cst_ydim))
            self.assertTrue(np.allclose(vopgen_zdim, cst_zdim))
            self.assertTrue(np.allclose(vopgen_efield, cst_efield))
            #save figures
            fig, axs = plt.subplots(2,3)
            XX, YY = np.meshgrid(vopgen_xdim, vopgen_ydim)
            XX = np.transpose(XX)
            YY = np.transpose(YY)
            zind = int(len(vopgen_zdim)/2)
            # Vopgen Field components
            axs[0][0].pcolormesh(XX, YY, np.abs(vopgen_efield[zind,:,:,0]))
            axs[0][0].set_title('Vopgen |Ex|')
            axs[0][1].pcolormesh(XX, YY, np.abs(vopgen_efield[zind,:,:,1]))
            axs[0][1].set_title('Vopgen |Ey|')
            axs[0][2].pcolormesh(XX, YY, np.abs(vopgen_efield[zind,:,:,2]))
            axs[0][2].set_title('Vopgen |Ez|')
            # CST h5 field components
            axs[1][0].pcolormesh(XX, YY, np.abs(cst_efield[zind,:,:,0]))
            axs[1][0].set_title('CST (h5) |Ex|')
            axs[1][1].pcolormesh(XX, YY, np.abs(cst_efield[zind,:,:,1]))
            axs[1][1].set_title('CST (h5) |Ey|')
            axs[1][2].pcolormesh(XX, YY, np.abs(cst_efield[zind,:,:,2]))
            axs[1][2].set_title('CST (h5) |Ez|')
            fig.savefig('cst_vopgen_efield_ch' + str(i+1) + '.png')

    def test_cp_shim_export(self):
        """
        Test application of magnitude and phase shim between CST AC combine and post-processing.
        CST excitation is CP with magnitude of 25 and phases progress incrementally with
        positive 45-deg
        """

        # shim specification
        shim_mags = 25*np.ones(8)
        shim_phases = 2.0*np.pi/180.0 * np.arange(0,360,45)
        
        # load Vopgen mat file into dictionary
        vopgen_file_name = os.path.join(self.cst_export_vopgen_dir,
                'efMapArrayN.mat')
        vopgen_dict = hdf5storage.loadmat(vopgen_file_name)
        vopgen_xdim = vopgen_dict['XDim']
        vopgen_ydim = vopgen_dict['YDim']
        vopgen_zdim = vopgen_dict['ZDim']

        # z,y,x,component,channel
        vopgen_efield = np.transpose(vopgen_dict['efMapArrayN'],(2,1,0,3,4))

        # load cst e-field cp data
        cst_efield_cp_file_name = os.path.join(self.cst_export_3d_dir, self.cst_efields_file_name)
        self.assertTrue(os.path.exists(cst_efield_cp_file_name))
        efield_fr = FieldReaderH5(cst_efield_cp_file_name)
        cst_efield = efield_fr.fields
        cst_xdim = efield_fr.xdim/1000.0
        cst_ydim = efield_fr.ydim/1000.0
        cst_zdim = efield_fr.zdim/1000.0

        # apply shim
        e1_shim = apply_shim(vopgen_efield, shim_mags, shim_phases)
        #self.assertTrue(np.allclose(e1_shim, np.zeros(np.shape(e1_shim), dtype=np.complex128)))
        # result plots for visual inspection
        fig, axs = plt.subplots(2,3)
        XX, YY = np.meshgrid(vopgen_xdim, vopgen_ydim)
        XX = np.transpose(XX)
        YY = np.transpose(YY)
        xind_cst = np.argmin(np.abs(cst_xdim))
        xind_vopgen = np.argmin(np.abs(vopgen_xdim)) 
        yind_cst = np.argmin(np.abs(cst_ydim))
        yind_vopgen = np.argmin(np.abs(vopgen_ydim))
        zind_cst = np.argmin(np.abs(cst_zdim))
        zind_vopgen = np.argmin(np.abs(vopgen_zdim))
        print("cstind: (", xind_cst, ',', yind_cst, ',', zind_cst, ')')
        print("vopind: (", xind_vopgen, ',', yind_vopgen, ',', zind_vopgen, ')')
         
        axs[0][0].pcolormesh(XX, YY, np.abs(cst_efield[zind_cst,:,:,2]),vmin=0, vmax=500)
        axs[0][1].pcolormesh(np.abs(cst_efield[:,yind_cst,:,2]), vmin = 0, vmax=500)
        im = axs[0][2].pcolormesh(np.abs(cst_efield[:,:,xind_cst,2]), vmin=0, vmax=500)
        axs[1][0].pcolormesh(XX, YY, np.abs(e1_shim[zind_vopgen,:,:,0]), vmin=0, vmax=500)
        axs[1][1].pcolormesh(np.abs(e1_shim[:,yind_vopgen,:,0]), vmin=0, vmax=500)
        axs[1][2].pcolormesh(np.abs(e1_shim[:,:,xind_vopgen,0]), vmin=0, vmax=500)
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
        plt.colorbar(im, cax=cbar_ax)
        fig.savefig("cst_vopgen_efield_shim.png")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
