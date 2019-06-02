"""CSTFieldWriter class provides methods to export CST field data in various formats on non-uniform
 and uniform grids.
"""
import abc
import re
import numpy as np
import scipy.io as spio
from cstmod import CSTResultReader, CSTFieldMonitor

try:
    from math import isclose
except ImportError:
    def isclose(a,b,rel_tol=1e-9, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol*max(abs(a), abs(b)), abs_tol)

class CSTFieldWriter(object):
    """Base clas for writing cst field data to file.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, result_reader):
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._fx = None
        self._fx_original = None
        self._fy_original = None
        self._fz_original = None
        self._result_reader = result_reader
    
    @property
    def xdim(self):
        """Return x grid values"""
        return self._xdim

    @property
    def ydim(self):
        """Return y grid values"""
        return self._ydim

    @property
    def zdim(self):
        """Return z grid values"""
        return self._zdim


class CSTFieldWriterNonUniform(CSTFieldWriter):
    """CSTFieldWriter exports complex electromagnetic field values 
    Args:
        :result_reader:  a result reader object to read cst field data
    """
    def __init__(self, result_reader):
        self.rr = result_reader
        self._xdim, self._ydim, self._zdim  = self.rr.load_grid_data()
        self._output_filename = None
        self._h_field_monitors = self.rr._query_field_monitors('H-Field')
        self._e_field_monitors = self.rr._query_field_monitors('E-Field')
        self._units = self._get_units()
        self._hfield_results = self.rr.query_result_names('h-field')
        self._efield_results = self.rr.query_result_names('e-field')

    def write(self, file_name, field_type, output_type='mat'):
        """
        Write the CST data to file name with given format.
        Args:
            :filename: path to given export file.
            "output_type: str export type (default is matlab.)
        """
        self._output_filename = file_name

        if 'mat' == output_type:
            self._matwriter(field_type)
        
        else:
            raise Exception("Output type: " + output_type + " has not been implemented.")

    def _get_units(self):
        """Determine local units from field monitor and result reader data.
        """
        fm0 = CSTFieldMonitor(self._h_field_monitors[0])
        if isclose(1000, round(fm0.simulation_domain_min.x/self._xdim[0])):
            self._units = 'mm'
        else:
            raise Exception("Unable to determine units.")
        
        return self._units

    def _matwriter(self, field_type, match_regex=r'\[Tran[0-9]*\]'):
        """Write field data to Matlab v5 mat file.
        """
        match_regex = '2D/3D Results' + '.*' + field_type + '.*' + match_regex
        field_regex = re.compile(match_regex)
        if 'e-field' == field_type:
            prefix = 'E'
            field_results = filter(field_regex.findall, self._efield_results)
        elif 'h-field' == field_type:
            prefix = 'H'
            field_results = filter(field_regex.findall, self._hfield_results)
        else:
            raise Exception("Field type not recognized.")
        field_results = [result for result in field_results]
        field_datax, field_datay, field_dataz = self.rr.load_data_3d(field_results[0])
        print("field_datax shape: ", np.shape(field_datax))
        print("field_datay shape: ", np.shape(field_datay))
        print("field_dataz shape: ", np.shape(field_dataz))
        save_dict = dict()
        save_dict['XDim'] = self._xdim
        save_dict['YDim'] = self._ydim
        save_dict['ZDim'] = self._zdim
        save_dict[prefix+'x'] = field_datax
        save_dict[prefix+'y'] = field_datay
        save_dict[prefix+'z'] = field_dataz

        spio.savemat(self._output_filename, save_dict, oned_as='column')
