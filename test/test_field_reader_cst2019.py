"""
Unit tests for FieldReaderCST2019 classes.
"""
import os
import shutil
import unittest
import numpy as np
import hdf5storage
import matplotlib.pyplot as plt
from cstmod.field_reader import FieldReaderCST2019

class TestFieldReaderCST2019(unittest.TestCase):
    """Unit tests class for FieldReaderCST2019.
    """
    @classmethod
    def setUpClass(cls):
        cls.test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..', 'test_data'))
    def setUp(self):
        self.fr = FieldReaderCST2019()
        # vopgen directory
        self.vopgen_export_dir = os.path.join(self.test_data_dir, 'Export', 'Vopgen')
        if os.path.exists(self.vopgen_export_dir):
            shutil.rmtree(self.vopgen_export_dir)

    def test_process_file_list(self):
        """Use list of regular expressions to generate input file list.
        """        
        field_files_pattern = [os.path.join(self.test_data_dir, 'e-field*.h5'),
                               os.path.join(self.test_data_dir, 'h-field*.h5')]

        field_files = [os.path.join(self.test_data_dir, "e-field (f=447) [pw].h5"),
                       os.path.join(self.test_data_dir, "h-field (f=447) [pw].h5")]
        self.assertTrue(os.path.exists(field_files[0]))
        self.assertTrue(os.path.exists(field_files[1]))
        self.fr._excitation_type = 'pw'
        found_field_files = self.fr._process_file_list(field_files_pattern[0])

        print('field files: ', field_files)
        for file in found_field_files:
            self.assertTrue(os.path.exists(file))
            self.assertTrue(file in field_files)

    def test_wrong_hdf5_file(self):
        """Test non-field hdf5 file.  A warning and a keyerror should be raised.
        """
        self.assertTrue(os.path.exists(os.path.join(self.test_data_dir, "e-field (f=447) [bad].h5")))
        with self.assertRaises(KeyError):
            self.fr._read_fields(self.test_data_dir, 'e-field', '447', 'bad')

    def test_square_bracket_padding(self):
        """Square brackets need to be padded to use fnmatch if the filename
        contains square brackets.
        """
        test_string1 = 'e-field (f=447.0) [AC1].h5'
        padded_string1 = 'e-field (f=447.0) [[]AC1[]].h5'
        test_string2 = 'h-field (f=447.0) [AC2].h5'
        padded_string2 = 'h-field (f=447.0) [[]AC2[]].h5'
        self.assertEqual(self.fr._pad_bracket_string(test_string1),padded_string1)
        self.assertEqual(self.fr._pad_bracket_string(test_string2),padded_string2)

    def test_read_bad_fields(self):
        """Test read_fields method to populate field matrices.
        """
        #self.fr._read_fields(self.test_data_dir, 'e-field', '447', 'pw')
        self.assertFalse(self.fr._read_fields(self.test_data_dir, 'bad_field', '447', 'AC'))
    
    def test_read_fields(self):
        """Test read_fiels method to populate field matrices.
        """
        self.fr._read_fields(self.test_data_dir,'e-field','447','AC')
    
    @unittest.skip
    def test_vopgen_bfield_writer(self):
        """Test the vopgen field writer for magnetic fields.
        """
        self.fr.write_vopgen('447',self.test_data_dir, self.vopgen_export_dir,
                              export_type='h-field', merge_type='AC',
                              rotating_frame = True)
        #ensure output directory has been created
        self.assertTrue(os.path.exists(os.path.join(self.test_data_dir,
                                       'Export', 'Vopgen')))
        bfmaparrayn_file = os.path.join(self.vopgen_export_dir, 'bfMapArrayN.mat')
        self.assertTrue(os.path.exists(bfmaparrayn_file))
        hfield_data = hdf5storage.loadmat(bfmaparrayn_file)
        self.assertIn('XDim', hfield_data.keys())
        self.assertIn('YDim', hfield_data.keys())
        self.assertIn('ZDim', hfield_data.keys())
        self.assertIn('bfMapArrayN', hfield_data.keys())
        self.assertEqual(1, len(np.shape(hfield_data['XDim'])))
        self.assertEqual(1, len(np.shape(hfield_data['YDim'])))
        self.assertEqual(1, len(np.shape(hfield_data['ZDim'])))
        self.assertEqual(5, len(np.shape(hfield_data['bfMapArrayN'])))

        # save a figure
        zdim = hfield_data['ZDim']
        bfMapArrayN = hfield_data['bfMapArrayN']
        nchannels = np.shape(bfMapArrayN)[4]
        cols = int(np.ceil(np.sqrt(nchannels)))  # subplots should be square
        rows = int(np.ceil(nchannels/cols))

        fig, axs = plt.subplots(rows, cols)
        k_ind = int(len(zdim)/2)
        channel = 0
        bmag_min = 0
        bmag_max = 1 # uT
        for ax in axs.reshape(-1):
            if channel < nchannels:
                plt.sca(ax)
                b1plus_mag = 1e6*np.abs(bfMapArrayN[:,:,k_ind,0,channel])
                plt.pcolor(b1plus_mag, vmin=bmag_min, vmax=bmag_max)
                channel += 1
                plt.title('|B1+| Ch: ' + str(channel)) 
                plt.colorbar()
                ax.set_aspect('equal')
        fig_path = os.path.join(self.test_data_dir, 'test_b1p_fields.png')
        plt.savefig(fig_path)
        self.assertTrue(os.path.exists(fig_path))
        fig, axs = plt.subplots(rows, cols)
        channel = 0
        for ax in axs.reshape(-1):
            if channel < nchannels:
                plt.sca(ax)
                b1minus_mag = 1e6*np.abs(bfMapArrayN[:,:,k_ind,1,channel])
                plt.pcolor(b1minus_mag, vmin=bmag_min, vmax=bmag_max)
                channel += 1
                plt.title('|B1-| Ch: ' + str(channel))
                plt.colorbar()
                ax.set_aspect('equal')
        fig_path = os.path.join(self.test_data_dir, 'test_b1m_fields.png')
        plt.savefig(fig_path)
        self.assertTrue(os.path.exists(fig_path))


    @unittest.skip
    def test_vopgen_efield_writer(self):
        """Test the vopgen field writer method.
        """
        self.fr.write_vopgen('447', self.test_data_dir, self.vopgen_export_dir,
                             export_type='e-field', merge_type = 'AC',
                             rotating_frame = False)
        # ensure ouput directory is created.
        self.assertTrue(os.path.exists(os.path.join(self.test_data_dir, 'Export')))
        sarmask_file = os.path.join(self.vopgen_export_dir, 'sarmask_aligned.mat')
        massdensity_map3d_file = os.path.join(self.vopgen_export_dir, 'massdensityMap3D.mat')
        propmap_file = os.path.join(self.vopgen_export_dir, 'propmap.mat')
        efmaparrayn_file = os.path.join(self.vopgen_export_dir, 'efMapArrayN.mat')

        self.assertTrue(os.path.exists(efmaparrayn_file))
        efield_data = hdf5storage.loadmat(efmaparrayn_file)
        self.assertIn('XDim', efield_data.keys())
        self.assertIn('YDim', efield_data.keys())
        self.assertIn('ZDim', efield_data.keys())
        self.assertIn('efMapArrayN', efield_data.keys())
        self.assertEqual(1, len(np.shape(efield_data['XDim'])))
        self.assertEqual(1, len(np.shape(efield_data['YDim'])))
        self.assertEqual(1, len(np.shape(efield_data['ZDim'])))
        self.assertEqual(5, len(np.shape(efield_data['efMapArrayN'])))

        # save a figure 
        zdim = efield_data['ZDim']
        efMapArrayN = efield_data['efMapArrayN']
        nchannels = np.shape(efMapArrayN)[4]    
        cols = int(np.ceil(np.sqrt(nchannels)))
        rows = int(np.ceil(nchannels/cols))

        fig, ax = plt.subplots(rows, cols)
        k_ind = int(len(zdim)/2)
        channel = 0
        for axx in ax:
            for ayy in axx:
                if channel < nchannels:
                    plt.sca(ayy)
                    emag = np.abs(np.sqrt(efMapArrayN[:,:,k_ind,0,channel] 
                                   * np.conj(efMapArrayN[:,:,k_ind,0,channel])
                                   + efMapArrayN[:,:,k_ind,1,channel] 
                                   * np.conj(efMapArrayN[:,:,k_ind,1,channel])
                                   + efMapArrayN[:,:,k_ind,2,channel]
                                   * np.conj(efMapArrayN[:,:,k_ind,2,channel])))
                    plt.pcolor(np.log10(emag))
                    channel += 1
                    plt.title("|E| Ch " + str(channel))

        fig_path = os.path.join(self.test_data_dir, 'test_e_fields.png')
        plt.savefig(fig_path)
        print("file path: ", fig_path)
        self.assertTrue(os.path.exists(fig_path))

    def tearDown(self):
        #if os.path.exists(self.vopgen_export_dir):
        #    shutil.rmtree(self.vopgen_export_dir)
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if "__main__" == __name__:
    unittest.main()