"""
Implement concrete field reader class for CST 2019.
"""
import os
import sys
import re
if 'win32' == sys.platform:
    import fnmatch
else:
    import glob
try:
    import h5py
    import hdf5storage
except: 
    print("Field reader requires HDF5 support.  Ensure h5py, hdf5storage is installed.")
try:
    import numpy as np
    from scipy.constants import mu_0
except:
    print("Field reader requires Numpy and Scipy.  Ensure package numpy,scipy is installed.")

from cstmod.field_reader import FieldReaderABC

class FieldReaderCST2019(FieldReaderABC):
    """Concrete implementation of FieldReader for CST2019 and later that uses
    HDF5 export format.
    """
    # class variables
    cst_3d_field_types = {'e-field':'E-Field', 'h-field':'H-Field'}
    cst_merge_types = ['AC', 'pw', 'Trans', 'TxCh']

    def __init__(self):
        self._field_file_list = []
        self._freq = 0.0
        self._excitation_type = ''
        self._nchannels = 0
        self._complex_fields = None
        self._source_dir = os.getcwd()
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._normalization = [1.0]
        self._source_dir = ""
        self._dim_scale = 0.001

    def _read_fields(self, field_dir, field_type, freq, excitation_type='', rotating_frame=False, version='2020'):
        """Read fields from multiple files.  A field patter will be constructed
        from input values.  A FileNotFoundError will be raised if a set of files
        cannot be constructed.
        Args:
            field_dir: Directory where hdf5 field data is located
            field_type: one of standard CST 3d "field" types ('e-field', 'h-field',...)
            freq: field monitor frequency value (e.g. 297.3) in MHz
            excitation_type: one of standard CST 3d excitation types 'pw', 'AC', 'Trans',
            rotating_frame: if True, field values will be stored in rotating frame (assumed along z-axis)
        Returns:
            None
        Raises:
            FileNotFoundError 
        """
        # Reset field storage prior to reading.
        self._complex_fields = None
        if version == '2020':
            #try lower case field file naming convention (cst2020)
            file_name_pattern = os.path.abspath(field_dir) + os.path.sep \
                                + field_type.lower() + r' (f=' \
                                + str(freq) + r') [' \
                                + excitation_type + '*].h5'
        else:
            file_name_pattern = os.path.abspath(field_dir) + os.path.sep \
                                + field_type + r' (f=' \
                                + str(freq) + r') [' \
                                + excitation_type + '*].h5'

        self._freq = freq
        self._excitation_type = excitation_type
        self._process_file_list(file_name_pattern)
        self._nchannels = len(self._field_file_list)
        if len(self._normalization) != self._nchannels:
            self._normalization = np.ones((self._nchannels), dtype = np.float)
        for channel, file_name in enumerate(self._field_file_list):
            if not os.path.exists(file_name):
                print("Could not find file: ", file_name)
                raise FileNotFoundError
            with h5py.File(file_name,'r') as dataf:
                try:
                    xdim = self._dim_scale * dataf['Mesh line x'][()]
                    ydim = self._dim_scale * dataf['Mesh line y'][()]
                    zdim = self._dim_scale * dataf['Mesh line z'][()]
                    fxre = np.transpose(dataf[self.cst_3d_field_types[field_type.lower()]]['x']['re'],(2,1,0))
                    fxim = np.transpose(dataf[self.cst_3d_field_types[field_type.lower()]]['x']['im'],(2,1,0))
                    fyre = np.transpose(dataf[self.cst_3d_field_types[field_type.lower()]]['y']['re'],(2,1,0))
                    fyim = np.transpose(dataf[self.cst_3d_field_types[field_type.lower()]]['y']['im'],(2,1,0))
                    fzre = np.transpose(dataf[self.cst_3d_field_types[field_type.lower()]]['z']['re'],(2,1,0))
                    fzim = np.transpose(dataf[self.cst_3d_field_types[field_type.lower()]]['z']['im'],(2,1,0))
                except(KeyError) as ex:
                    print("A KeyError exception was caught.  It is likely that " 
                          + "the hdf5 file is not a 3d field export or has "
                          + "become corrupted.")
                    raise(ex)
                # set dimensions of complex fields
                if self._complex_fields is None:
                    if rotating_frame:
                        field_dim = (len(xdim), len(ydim), len(zdim),2 , self._nchannels)

                    else:
                        field_dim = (len(xdim), len(ydim), len(zdim), 3, self._nchannels)
                    self._complex_fields = np.empty(field_dim, dtype=np.complex)

                # construct field array

                if rotating_frame:
                    # positive rotating frame (e.g. B1+)
                    fx = fxre + 1.0j*fxim
                    fy = fyre + 1.0j*fyim
                    rotating_field_plus = 0.5*(fx + 1.0j*fy)
                    self._complex_fields[:,:,:,0,channel] = self._normalization[channel] * rotating_field_plus
                    # negative rotating frame (e.g. B1-)
                    rotating_field_minus = 0.5*(np.conj(fx) + 1.0j*np.conj(fy))
                    self._complex_fields[:,:,:,1,channel] = self._normalization[channel] * rotating_field_minus
                else:
                    # X-fields
                    self._complex_fields[:,:,:,0,channel] = self._normalization[channel] * (fxre + 1.0j*fxim)
                    # Y-fields
                    self._complex_fields[:,:,:,1,channel] = self._normalization[channel] * (fyre + 1.0j*fyim)
                    # Z-fields
                    self._complex_fields[:,:,:,2,channel] = self._normalization[channel] * (fzre + 1.0j*fzim)
            # set x-, y-, z- dimensions
            self._xdim = xdim
            self._ydim = ydim
            self._zdim = zdim

    def _process_file_list(self, file_name_pattern):
        """Generate a list of files that matches a provided regular expression.
        file_name_pattern: file pattern path to list of files.
        """
        if 'win32' == sys.platform:
            file_list = []
            self._source_dir = os.path.dirname(file_name_pattern)
            file_base_pattern = self._pad_bracket_string(os.path.basename(file_name_pattern))
            print("file_base pattern: ", file_base_pattern)
            print(fnmatch.filter(os.listdir(os.path.dirname(file_name_pattern)),self._pad_bracket_string(file_base_pattern)))
            file_list = [os.path.join(self._source_dir, file) for file in fnmatch.filter(os.listdir(os.path.dirname(file_name_pattern)),file_base_pattern)]
            print("file_list: ", file_list)
        else:
            print('[DEBUG] field_reader_cst2019 process_file_list ', file_name_pattern)
            glob_string = self._pad_bracket_string(file_name_pattern)
            print('glob_string: ', glob_string)
            file_list = glob.glob(glob_string)
            print('file_list: ', file_list)

        if 0 == len(file_list):
            raise KeyError("File pattern not found: " + file_name_pattern )

        #  One-liner to generate a list of filenames sorted by the channel number.
        if 1 == len(file_list):
            self._field_file_list = file_list
        else:
            try:
                self._field_file_list = sorted(file_list, key=lambda fl: int(re.search(r'\['+ self._excitation_type + r'([\d]+)\]', fl).group(1)))
            except(AttributeError): 
                self._field_file_list = []

        # One file per channel is assumed
        self._nchannels = len(self._field_file_list)

        return self._field_file_list

    def _pad_bracket_string(self, string_with_brackets):
        """Pad square bracket characters for pattern matching with square brackets.
        """
        f_right_bracket = string_with_brackets.split('[')  
        f_padded_right_bracket = [] # storage of padded string fragments 
        for fsub in f_right_bracket:
            temp = fsub.split(']')
            f_padded_right_bracket.append("[]]".join(temp))

        return "[[]".join(f_padded_right_bracket)
    
    def write_vopgen(self, frequency, source_dir, output_file, export_type='e-field', 
                     merge_type = 'AC', rotating_frame = False):
        """Create vopgen output files for e-field and b-field, masks, etc.
        Args:
            output_dir: Output directory.  Default is export directory within
                        the source directory.
            export_type: Data to export.  valid options are 'h-field', 'e-field'
        """
        output_dir = os.path.dirname(output_file)
        if not output_dir:
            output_dir = os.path.join(self._source_dir, 'Export', 'Vopgen')
        if not os.path.exists(output_dir):
            print("trying to create vopgen directory")
            os.makedirs(output_dir)

        export_type = self.cst_3d_field_types[export_type]
        self._read_fields(source_dir, export_type, frequency, merge_type, rotating_frame)
        export_dict = dict()
        export_dict[u'XDim'] = self._xdim
        export_dict[u'YDim'] = self._ydim
        export_dict[u'ZDim'] = self._zdim
        if 'E-Field' == export_type:
            export_dict[u'efMapArrayN'] = self._complex_fields
            hdf5storage.savemat(output_file, export_dict, oned_as='column')
        elif 'H-Field' == export_type:
            export_dict[u'bfMapArrayN'] = mu_0 * self._complex_fields
            hdf5storage.savemat(output_file, export_dict, oned_as='column')

    @property
    def normalization(self):
        """Return Normalization.
        """
        return self._normalization

    @normalization.setter
    def normalization(self, new_normalization):
        self._normalization = np.array(new_normalization)
