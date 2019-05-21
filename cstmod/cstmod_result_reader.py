#!/usr/bin/env python
"""CSTResultReader is a facade to provide a clean python interface to the low-level
(ctypes) calls to functions in CST ResultReaderDLL.dll 
"""

import os
import ctypes
import winreg
import sys
import platform
import re
import glob
import numpy as np
from enum import Enum
from cstmod.cstutil import CSTRegInfo
from cstmod import CSTMaterialType, CSTFieldMonitor

class CSTErrorCodes(Enum):
    """Collection of CST DLL return codes
    """
    ERROR_CODE_MEMORY = 8

class CSTResultReader(object):
    """Class that wraps the ResultReaderDLL library.
    """
    # class variables
    _valid_3d_field_types = ['E-Field', 'H-Field', 'Surface Current']
    _field_meta_regex = {'E-Field': r'(e-field \(f=[0-9.]*\))',
                        'H-Field': r'(h-field \(f=[0-9.]*\))',
                        'Surface Current':r'(surface current (\(f=[0-9.]*\)))' }
    
    def __init__(self, cst_version = '2018'):
        rr_dll_path = CSTRegInfo.find_result_reader_dll(cst_version)
        self._rr_dll = ctypes.WinDLL(rr_dll_path)
        self._dll_version = ctypes.c_int()
        try:
                rval = ctypes.c_int(0)
                rval  = self._rr_dll.CST_GetDLLVersion(ctypes.byref(self._dll_version))
        except:
                print("CST_GetDLLVersion() returned ", rval)
                raise

        self._proj_handle = ctypes.c_void_p()
        self._nx = None
        self._ny = None
        self._nz = None
        self._data = None
        self._xdim = None
        self._ydim = None
        self._zdim = None
        self._project_path = None
        self._spatial_units = None

    @property
    def dll_version(self):
        """Returns the version number of the DLL.  Corresponds to the version number of the CST STUDIO
        SUITE it was delivered with.

        :return: int
        """
        return self._dll_version.value

    def open_project(self, project_path):
         """Opens a project
         """
         self._project_path = project_path
         cst_project_path = ctypes.create_string_buffer(project_path.encode('ascii'))
         rval = self._rr_dll.CST_OpenProject(ctypes.byref(cst_project_path),
                                             ctypes.byref(self._proj_handle))
         if 0 != rval:
                raise Exception("An error occurred.  Error type was: " + str(rval))

    def close_project(self):
        """Closes project
        """
        rval = self._rr_dll.CST_CloseProject(ctypes.byref(self._proj_handle))
        if 0 != rval:
                raise Exception("An error occurred. Error type was: " + str(rval))

    def query_result_names(self, result_string):
        """Returns the number of results available for the selected result tree item.
     
        :type: string
        :return: list of str 
        """
        buf_size = 10000
        discovered_string = ""
        num_items = ctypes.c_int(-1)
        search_term = ctypes.create_string_buffer(result_string.encode('ascii'))
         
        discovered_buf = ctypes.create_string_buffer(buf_size)
        while True:
            rval = self._rr_dll.CST_GetItemNames(ctypes.byref(self._proj_handle),
                                                 search_term,
                                                 discovered_buf,
                                                 ctypes.c_int(buf_size),
                                                 ctypes.pointer(num_items))
            if 0 == rval:
                 break
            elif CSTErrorCodes.ERROR_CODE_MEMORY.val == rval:
                 buf_size *= 2
                 discovered_buf = ctypes.create_string_buffer(buf_size)
            else:
                 sys.exit("Error reading items: " + str(rval))

        item_list = discovered_buf.value.split(b'\n')

        return item_list

    def _query_field_monitors(self, field_type):
        """Find field monitor metadata files for given result type.
        
        Args:
            field_type (enum): enumeration of possible field types 'E-field', 'H-field', 'Surface current'                      'Surface Current' = 3
        """
        if field_type not in self._valid_3d_field_types:
            raise Exception("Invalid field type.  Valid types are: ", self._valid_3d_field_types)
        
        field_results = self.query_result_names(field_type)
        p = re.compile(self._field_meta_regex[field_type])
        m = p.findall(field_results[0].decode('ascii'))
        project_dir, project_ext = os.path.splitext(self._project_path)
        if 'Surface Current' == field_type:
            metadata_files = glob.glob(os.path.join(project_dir, r'Result',
                                       'h-field ' + m[0][1] + '*sct.rex'))
        else:
            metadata_files = glob.glob(os.path.join(project_dir, r'Result', m[0] + r'*.rex'))
        
        return metadata_files

    def get_frequency_scale(self):
        """Returns the frequency scale of the simulation.
        """
        rval = ctypes.c_int(0)
        fscale = ctypes.c_double()
        rval = self._rr_dll.CST_GetFrequencyScale(ctypes.byref(self._proj_handle), 
                                                    ctypes.byref(fscale))

        if 0 != rval:
            raise Exception("An error occurred.  The error was: " + str(rval))                                            

        return fscale.value

    def load_grid_boundaries(self):
        """Return the defined boundary condition of the selected project.
        """
        rval = ctypes.c_int(0)
        grid_boundaries = np.zeros((6,), dtype=ctypes.c_int)
        pgrid_boundaries = grid_boundaries.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        rval = self._rr_dll.CST_GetBoundaries(ctypes.byref(self._proj_handle), pgrid_boundaries)
        if 0 != rval:
            raise Exception("An error occurred.  Error type was: " + str(rval))
        
        return grid_boundaries

    def load_grid_data(self):
        """Loads and returns a numpy array of with hexahedral mesh data.
        :return: returns numpy array with appropriate dimensions
        """
        rval = ctypes.c_int(0)
        n_xyz = (ctypes.c_int * 3)()  # grid dimension array

        rval = self._rr_dll.CST_GetHexMeshInfo(ctypes.byref(self._proj_handle),
                                                ctypes.byref(n_xyz))
        if 0 != rval:
            raise Exception("An error occurred.  Error type was: " + str(rval))

        self._nx = n_xyz[0]
        self._ny = n_xyz[1]
        self._nz = n_xyz[2]

        n_xyzlines_size = n_xyz[0] + n_xyz[1] + n_xyz[2]
        n_xyzlines = (ctypes.c_double * (n_xyz[0] + n_xyz[1] + n_xyz[2]))()
        rval = self._rr_dll.CST_GetHexMesh(ctypes.byref(self._proj_handle),
                                            ctypes.byref(n_xyzlines))
        if 0 != rval:
            raise Exception("An error occurred.  Error type was: " + str(rval))

        self._xdim = [n_xyzlines[i] for i in range(n_xyz[0])]
        self._ydim = [n_xyzlines[i + n_xyz[0]] for i in range(n_xyz[1])]
        self._zdim = [n_xyzlines[i + n_xyz[0] + n_xyz[1]] for i in range(n_xyz[2])]

        return self._xdim, self._ydim, self._zdim

    def load_grid_mat_data(self, material_type):
        """Loads and returns the 
        """
        rval = ctypes.c_int(0)
        if (None == self._nx) or (None == self._ny) or (None == self._nz):
            self.load_grid_data()

        n_points = self._nx * self._ny * self._nz
        fmatrix = np.zeros((3*n_points,), dtype = ctypes.c_float) 


        pfmatrix = fmatrix.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        rval = self._rr_dll.CST_GetMaterialMatrixHexMesh(ctypes.byref(self._proj_handle),
                                                         ctypes.c_int(material_type),
                                                         pfmatrix)

        if 0 != rval:
            raise Exception("An error occurred.  Error type was: " + str(rval))

        #reshape material matrices
        fx = fmatrix[0:n_points].reshape(self._nz, self._ny, self._nx)
        fy = fmatrix[n_points:2*n_points].reshape(self._nz, self._ny, self._nx)
        fz = fmatrix[2*n_points:].reshape(self._nz, self._ny, self._nx)

        return fx, fy, fz

    def load_data_3d(self, tree_path_name):
        """Loads and returns numpy array with data from given tree location.
        :param tree_path_name: tree path of data to be retreived
        :return: returns numpy array with appropriate dimensions
        """
        cst_tree_path_name = ctypes.create_string_buffer(tree_path_name.encode('ascii'))
        rval = ctypes.c_int(0)
        n_result_number = ctypes.c_int(0)
        rval = self._rr_dll.CST_GetNumberOfResults(ctypes.byref(self._proj_handle),
                                                    ctypes.byref(cst_tree_path_name),
                                                    ctypes.byref(n_result_number))
        if 0 != rval:
            raise Exception("An error occurred.  Error type was: " + str(rval))

        n_data_size = ctypes.c_int(0)
        n_xyz = (ctypes.c_int * 3)()
        rval = self._rr_dll.CST_GetHexMeshInfo(ctypes.byref(self._proj_handle),
                                                        ctypes.byref(n_xyz))
        if 0 != rval:
            raise Exception("An error occurred. Error type was: " + str(rval))

        grid_size = n_xyz[0] * n_xyz[1] * n_xyz[2]

        rval = self._rr_dll.CST_Get3DHexResultSize(ctypes.byref(self._proj_handle),
                                                    ctypes.byref(cst_tree_path_name),
                                                    n_result_number,
                                                    ctypes.byref(n_data_size))
        if 0 != rval:
            raise Exception("An error occurred. Error type was: " + str(rval))
        print('3d hex result size: ', n_data_size.value, '(', rval, ')')
        print('n_data_size/grid_size: ', n_data_size.value/grid_size)

        info_array_size = ctypes.c_int(1)
        char_buffer_size = ctypes.c_int(1)
        cinfo = ctypes.c_char(b'C')
        iinfo = ctypes.c_int(0)
        dinfo = ctypes.c_double(0.0)

        rval = self._rr_dll.CST_Get3DHexResultInfo(ctypes.byref(self._proj_handle),
                                                    ctypes.byref(cst_tree_path_name),
                                                    n_result_number,
                                                    info_array_size,
                                                    char_buffer_size,
                                                    ctypes.byref(cinfo),
                                                    ctypes.byref(iinfo),
                                                    ctypes.byref(dinfo))
        if 0 != rval:
            raise Exception("An error occurred.  Error type was: " + str(rval))

        print("iinfo: ", iinfo.value)
        if 1 == iinfo.value: 
            # complex 3d vector field
            d_data = np.empty((n_data_size.value,), dtype=ctypes.c_float)
            p_data = d_data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        else:
            raise Exception("Monitor type (" + str(iinfo) + ") not implemented.")

        rval = self._rr_dll.CST_Get3DHexResult(ctypes.byref(self._proj_handle),
                                                ctypes.byref(cst_tree_path_name),
                                                ctypes.byref(iinfo),
                                                p_data)
        if 0 != rval:
            raise Exception("An error occurred. Error type was: " + str(rval))

        return d_data