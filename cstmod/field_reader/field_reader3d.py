"""
result_reader3d.py  
reads CST2019 and newer hdf5 formatted output data.
"""

import os
import sys
import re
#if 'win32' == sys.platform:
#    import fnmatch
#else:
#    import glob
try:
    import h5py
    #import hdf5storage
except: 
    print("Field reader requires HDF5 support.  Ensure h5py is installed.")
try:
    import numpy as np
    from scipy.constants import mu_0
except:
    print("Field reader requires Numpy and Scipy.  Ensure package numpy,scipy is installed.")

class ResultReader3D(object):
    """ Read CST fields exported in HDF5 export format.
    """
    # class variables
    cst_3d_field_types = {'e-field':'E-Field', 'h-field':'H-Field','current':'Conduction Current Density'}
    #cst_merge_types = ['AC', 'pw', 'Trans', 'TxCh']

    def __init__(self, file_name, field_type, rotating_frame = False):
        self._file_name = file_name
        self._field_type = field_type
        self._rotating_frame = rotating_frame
        self._freq = 0.0
        self._complex_fields = None
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._dim_scale = 0.001
        self._read_fields()

    def _read_fields(self):
        """Read fields from multiple files.  A field patter will be constructed
        from input values.  A FileNotFoundError will be raised if a set of files
        cannot be constructed.
        Args:
            rotating_frame: if True, field values will be stored in rotating frame (assumed along z-axis)
            Returns:
            None
        Raises:
            FileNotFoundError 
        """
        # Reset field storage prior to reading.
        self._complex_fields = None
        if not os.path.exists(self._file_name):
            print("Could not find file: ", self._file_name)
            raise FileNotFoundError
        with h5py.File(self._file_name,'r') as dataf:
            try:
                xdim = self._dim_scale * dataf['Mesh line x'][()]
                ydim = self._dim_scale * dataf['Mesh line y'][()]
                zdim = self._dim_scale * dataf['Mesh line z'][()]
                fxre = np.transpose(dataf[self.cst_3d_field_types[self._field_type.lower()]]['x']['re'],(2,1,0))
                fxim = np.transpose(dataf[self.cst_3d_field_types[self._field_type.lower()]]['x']['im'],(2,1,0))
                fyre = np.transpose(dataf[self.cst_3d_field_types[self._field_type.lower()]]['y']['re'],(2,1,0))
                fyim = np.transpose(dataf[self.cst_3d_field_types[self._field_type.lower()]]['y']['im'],(2,1,0))
                fzre = np.transpose(dataf[self.cst_3d_field_types[self._field_type.lower()]]['z']['re'],(2,1,0))
                fzim = np.transpose(dataf[self.cst_3d_field_types[self._field_type.lower()]]['z']['im'],(2,1,0))
            except(KeyError) as ex:
                print("A KeyError exception was caught.  It is likely that " 
                      + "the hdf5 file is not a 3d field export or has "
                      + "become corrupted.")
                raise(ex)
            # set dimensions of complex fields
            if self._complex_fields is None:
                if self._rotating_frame:
                    field_dim = (len(xdim), len(ydim), len(zdim),2)
                else:
                    field_dim = (len(xdim), len(ydim), len(zdim), 3)
                self._complex_fields = np.empty(field_dim, dtype=np.complex128)

            # construct field array

            if self._rotating_frame:
                # positive rotating frame (e.g. B1+)
                fx = fxre + 1.0j*fxim
                fy = fyre + 1.0j*fyim
                rotating_field_plus = 0.5*(fx + 1.0j*fy)
                self._complex_fields[:,:,:,0] = rotating_field_plus
                # negative rotating frame (e.g. B1-)
                rotating_field_minus = 0.5*(np.conj(fx) + 1.0j*np.conj(fy))
                self._complex_fields[:,:,:,1] = rotating_field_minus
            else:
                # X-fields
                self._complex_fields[:,:,:,0] = fxre + 1.0j*fxim
                # Y-fields
                self._complex_fields[:,:,:,1] = fyre + 1.0j*fyim
                # Z-fields
                self._complex_fields[:,:,:,2] = fzre + 1.0j*fzim
            # set x-, listy-, z- dimensions
        self._xdim = xdim
        self._ydim = ydim
        self._zdim = zdim

    @property
    def xdim(self):
        """ Return xdim
        """
        return self._xdim

    @property
    def ydim(self):
        """ Return ydim 
        """
        return self._ydim

    @property
    def zdim(self):
        """ Return zdim
        """
        return self._zdim
    
    @property
    def fields3d(self):
        """ Return the 3d fields
        """
        return self._complex_fields

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    data_dir = os.path.join(r'/mnt', r'Data', r'Temp_CST', r'KU_Ten_32_FDA_21Jul2021_4_6')
    currents_file = os.path.join(data_dir, r'current (f=447) [AC1].h5')
    rr3d = ResultReader3D(currents_file, 'current')
    plt.pcolor(np.abs(rr3d.fields3d[:,:,200,0]))
    plt.show()