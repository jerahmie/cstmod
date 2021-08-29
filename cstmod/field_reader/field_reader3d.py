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
    cst_3d_field_types = {'e-field':'E-Field', 'h-field':'H-Field','current':'Conduction Current Density','sar':'SAR'}
    #cst_merge_types = ['AC', 'pw', 'Trans', 'TxCh']

    def __init__(self, file_name, field_type, rotating_frame = False):
        self._file_name = file_name
        self._field_type = field_type
        self._rotating_frame = rotating_frame
        self._freq = 0.0
        self._fields3d = None
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._dim_scale = 0.001
        self._read_fields()

    def _is_complex(self):
        """Is the requested field type real or complex?
        """
        if self._field_type == 'e-field':
            return True
        elif self._field_type == 'h-field':
            return True
        elif self._field_type == 'current':
            return True
        elif self._field_type == 'sar':
            return False

    def _read_fields(self):
        """Read 3d data (aka "fields") from a CST hdf5 files. If field_type is a complex field,
            the _read_complex_fields is called, otherwise _read_real_fields is called.
        Raises:
            FileNotFoundError
        """
        if self._is_complex():
            self._read_complex_fields()
        else:
            self._read_3d_fields()

    def _read_3d_fields(self):
        """Read 3d fields from CST hdf5 files.
        Args:
            None
        Raises:
            FileNotFoundError
        """
        # Reset field storage prior to read field.
        self._fields3d = None
        if not os.path.exists(self._file_name):
            print("Could not find file: ", self._file_name)
            raise FileNotFoundError
        with h5py.File(self._file_name,'r') as dataf:
            try:
                xdim = self._dim_scale * dataf['Mesh line x'][()]
                ydim = self._dim_scale * dataf['Mesh line y'][()]
                zdim = self._dim_scale * dataf['Mesh line z'][()]
                self._fields3d = np.transpose(dataf[self.cst_3d_field_types[self._field_type.lower()]],(2,1,0))
            except(KeyError) as ex:
                print("A KeyError exception was caught.  It is likely that " 
                      + "the hdf5 file is not a 3d field export or has "
                      + "become corrupted.")
                raise(ex)

    def _read_complex_fields(self):
        """Read complex fields from CST hdf5 files. 
        Args:
            None
        Raises:
            FileNotFoundError 
        """
        # Reset field storage prior to reading.
        self._fields3d = None
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
        if self._fields3d is None:
            if self._rotating_frame:
                field_dim = (len(xdim), len(ydim), len(zdim),2)
            else:
                field_dim = (len(xdim), len(ydim), len(zdim), 3)
            self._fields3d = np.empty(field_dim, dtype=np.complex128)

        # construct field array

        if self._rotating_frame:
            # positive rotating frame (e.g. B1+)
            fx = fxre + 1.0j*fxim
            fy = fyre + 1.0j*fyim
            rotating_field_plus = 0.5*(fx + 1.0j*fy)
            self._fields3d[:,:,:,0] = rotating_field_plus
            # negative rotating frame (e.g. B1-)
            rotating_field_minus = 0.5*(np.conj(fx) + 1.0j*np.conj(fy))
            self._fields3d[:,:,:,1] = rotating_field_minus
        else:
            # X-fields
            self._fields3d[:,:,:,0] = fxre + 1.0j*fxim
            # Y-fields
            self._fields3d[:,:,:,1] = fyre + 1.0j*fyim
            # Z-fields
            self._fields3d[:,:,:,2] = fzre + 1.0j*fzim
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
        """ Return the complex 3d fields
        """
        return self._fields3d

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    if sys.platform == 'win32':
        data_dir = os.path.join(r'D:', os.sep, r'Temp_CST',
                                r'KU_Ten_32_FDA_21Jul2021_4_6',
                                r'Export', r'3d')
    else: 
        data_dir = os.path.join(r'/mnt', r'Data', r'Temp_CST',
                                r'KU_Ten_32_FDA_21Jul2021_4_6',
                                r'Export', r'3d')

    #currents_file = os.path.join(data_dir, r'current (f=447) [AC1].h5')
    #rr3d = ResultReader3D(currents_file, 'current')
    sar_file = os.path.join(data_dir, r'SAR (f=447) [AC1] (10g).h5')
    rr3d = ResultReader3D(sar_file, 'sar')
    plt.pcolor(np.abs(rr3d.fields3d[:,:,200]))
    plt.show()