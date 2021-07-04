"""
Implement concrete single field reader for CST export fields with hdf5 (CST2019+)
"""
import os
import numpy as np
import errno
import re
try:
    import h5py
except:
    raise ImportError("FieldReader requires HDF5 suport.  Ensure h5py is installed.")
from cstmod.field_reader import FieldReaderABC

# class variables
cst_3d_field_types = [r'e-field', r'h-field']

def extract_field_type(file_name):
    """
    Extract the field type from file name
    Args:
        file_name  
    Returns:
        string valid string type
    Raises:
        FileNotFoundError
    """
    if not os.path.exists(file_name):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_name)
    else:
        for ft in cst_3d_field_types:
            res = re.search(re.escape(ft.lower()), file_name.lower())
            if res is not None:
                field_type = res.group(0)
    return field_type

class FieldReaderH5(FieldReaderABC):
    """
    Concrete implementation of FieldReader
    """
    # class variables
    cst_3d_field_types = {'e-field':'E-Field', 'h-field':'H-Field'}
    
    def __init__(self, file_name):
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._complex_fields = None 
        self._field_type = extract_field_type(file_name)
        self._file_name = file_name
        self._read_fields()

    def _read_fields(self):
        """
        _read_fields - loads fields of given CST export file
        Args:
            None
        Returns:
            None
        Raises:
            FileNotFoundError
        """
        if not os.path.exists(self._file_name):
            raise FileNotFoundError("Could not find file: ", self._file_name)
        with h5py.File(self._file_name,'r') as dataf:
            try:
                xdim = dataf['Mesh line x'][()]
                ydim = dataf['Mesh line y'][()]
                zdim = dataf['Mesh line z'][()]
                fxre = dataf[self.cst_3d_field_types[self._field_type.lower()]]['x']['re']
                fxim = dataf[self.cst_3d_field_types[self._field_type.lower()]]['x']['im']
                fyre = dataf[self.cst_3d_field_types[self._field_type.lower()]]['y']['re']
                fyim = dataf[self.cst_3d_field_types[self._field_type.lower()]]['y']['im']
                fzre = dataf[self.cst_3d_field_types[self._field_type.lower()]]['z']['re']
                fzim = dataf[self.cst_3d_field_types[self._field_type.lower()]]['z']['im']
            except(KeyError) as ex:
                print("A KeyError exception was caught.  It is likely that " 
                      + "the hdf5 file is not a 3d field export or has "
                      + "become corrupted.")
                raise(ex)
            field_shape = np.shape(fxre)
            export_fields_shape = (field_shape[0],
                                   field_shape[1],
                                   field_shape[2], 3)

            self._complex_fields = np.empty(export_fields_shape, dtype=np.complex128)
            self._complex_fields[:,:,:,0] = fxre + 1.0j*fxim
            self._complex_fields[:,:,:,1] = fyre + 1.0j*fyim
            self._complex_fields[:,:,:,2] = fzre + 1.0j*fzim
            self._xdim = xdim
            self._ydim = ydim
            self._zdim = zdim

    @property
    def fields(self):
        """
        Returns: ndarray of field values.
        """
        return self._complex_fields

    @property
    def xdim(self):
        """
        Returns: ndarray of x-grid values.
        """
        return self._xdim

    @property
    def ydim(self):
        """
        Returns: ndarray of y-grid values.
        """
        return self._ydim

    @property
    def zdim(self):
        """
        Returns: ndarray of z-grid values.
        """
        return self._zdim

    @property
    def field_type(self):
        """
        Returns: field type
        """
        return self._field_type