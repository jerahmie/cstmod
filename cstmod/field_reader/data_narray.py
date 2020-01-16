"""Represents a generic complex data type from CST ascii export.
"""
import os
import sys
import csv
if 'win32' == sys.platform:
    import fnmatch
else:
    import glob

try:
    import numpy as np

except:
    print("Field reader requires Numpy and Scipy.  Ensure package numpy,scipy is installed.")
from cstmod.field_reader import DataNArrayABC


class GenericDataNArray(DataNArrayABC):
    """Class to manage n-channels of generic 1-D ascii data exported from CST.
    """
    def __init__(self):
        self._data = None
        self._data_shape = None
        self._data_length = 0
        self._nchannels = 0
        self._data_valid = False
        self._source_dir = ""
        self._xdim = None

    def _process_file_list(self, file_name_pattern):
        """Generate a list of export files based on provided file name pattern.
        Args:        
            file_name_pattern (str): filename pattern with Unix-style wild cards.

        Returns: 
            sorted list of filenames matching file_name_pattern
        """
        if 'win32' == sys.platform:
            file_list = []
            self._source_dir = os.path.dirname(file_name_pattern)
            file_base_pattern = self._pad_bracket_string(os.path.basename(file_name_pattern))
            file_list = [os.path.join(self._source_dir, file) for file in fnmatch.filter(os.listdir(os.path.dirname(file_name_pattern)),file_base_pattern)]
        else: 
            
            file_list = glob.glob(self._pad_bracket_string(file_name_pattern))
            print("[DEBUG]: glob_pattern: ", self._pad_bracket_string(file_name_pattern))
            print("[DEBUG]: file_list: ", file_list)
        
        if 0 == len(file_list):
            raise KeyError("File pattern not found: " + file_name_pattern)

        return file_list

    def _pad_bracket_string(self, string_with_brackets):
        """Pad square bracket characters for pattern matching with square brackets.
        """
        f_right_bracket = string_with_brackets.split('[')  
        f_padded_right_bracket = [] # storage of padded string fragments 
        for fsub in f_right_bracket:
            temp = fsub.split(']')
            f_padded_right_bracket.append("[]]".join(temp))

        return "[[]".join(f_padded_right_bracket)            

    def load_data_one_d(self, filename_pattern):
        """Load data corresponding to filename pattern.
        """
        file_list = self._process_file_list(filename_pattern)
        
        if len(file_list) == 0:
            raise KeyError("File list is empty. File pattern: ", file_pattern)
        else:
            self._nchannels = len(file_list)
            # load first file in file_list to get dimensions
            with open(file_list[0], 'r', newline='') as csvfile:
                datareader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                self._data_length = sum(1 for row in datareader)
                self._data_shape = (self._data_length, self._nchannels)
                self._xdim = np.zeros(self._data_length, dtype = np.float)
                # go back to reader beginning and read xdim 
                csvfile.seek(0)
                ind = 0
                for row in datareader:
                    self._xdim[ind] = np.float(row[0])
                    ind += 1

            self._data = np.zeros(self._data_shape, dtype=np.complex)
            xdim = np.zeros(self._data_length, dtype=np.float)
            for channel in range(self._nchannels):
                with open(file_list[channel], 'r', newline='') as csvfile:
                    datareader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                    irow = 0
                    for row in datareader:
                        xdim[irow] = np.float(row[0])
                        self._data[irow,channel] = np.float(row[1]) + 1.0j*np.float(row[2])
                        irow += 1


    def nchannel_data_at_val(self, val0):
        """Returns the n-channel data at given value.
        """
        # find index of element nearest to 
        ind = np.argmin(np.abs(self._xdim - val0))
        x_nearest = self._xdim[ind]
        print(self._xdim)
        data_at_val  = [self._data[ind, channel] for channel in range(self._nchannels)]
        return x_nearest, data_at_val

    @property
    def nchannels(self):
        """Returns the number of channels in the antenna array.
        """
        return self._nchannels

    @nchannels.setter
    def nchannels(self, new_nchannels):
        """Sets the number of channels in the antenna array.
        This will be checked against number of matching ascii files when loading data.
        """
        self._nchannels = new_nchannels

    @property
    def data_shape(self):
        return self._data_shape

    @property 
    def data_length(self):
        return self._data_length


    @property
    def xdim(self):
        """Returns the x-dimension of the data.
        """
        return self._xdim
