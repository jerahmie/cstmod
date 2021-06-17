"""A wrapper class for the CST ResultReaderDLL.
Warning - The ResustReaderDLL has been marked as deprecated since CST2019, 
though it is included in CST2020 and CST2021.  A migration path that includes 
all functionality for the CST Result Reader has yet to be announced by CST or 
Dassault Systemmes.  JWR 6/10/2021
"""
import os
import traceback
from ctypes import *
import numpy as np

try:
    import win32com.client as win3
except ImportError as error:
    print("This script assumes Windows with pywin32 installed.")
    print(error.__class__.__name__ + ": " + error.message)

try:
    from cstmod.cstutil import CSTRegInfo
except ImportError as error:
    print("This script assumes cstmod is installed: See README.md")
    print(error.__class__.__name__ + ": " + error.message)

RESULTS_TREE_MAX_PATH=500000  # maximum number of characters in tree path

class CSTProjHandle(Structure):
    """CSTProjHandle
    CST Project handle for open projects.  Wraps the following typedef struct:
        typedef struct {void *m_pProj;} CSTProjHandle;
    """
    _fields_ = [("m_pProj", c_void_p)]

class ResultReaderDLL(object):
    """ResultReaderDLL - A wrapper class to provide an interface to the library
    functions provided by the CSTResultReaderDLL.

    Args:
        string: cst_project_file: path to CST Project file
        string: cst_version
    """
    def __init__(self, cst_project_file: str, cst_version: str):
        resultreaderdll_file = CSTRegInfo.find_result_reader_dll(cst_version)
        self._resultReaderDLL = WinDLL(resultreaderdll_file)
        self._projh = CSTProjHandle() # project handle 
        self._dll_version = None
        self._cst_project_file = cst_project_file
        self._project_result_path = None
        self._project_3d_result_path = None

        # ResultReaderDLL functions
        #
        # CST_GetDLLVersion
        #
        self._CST_GetDLLVersion = self._resultReaderDLL.CST_GetDLLVersion
        self._CST_GetDLLVersion.argtypes = [POINTER(c_int)]
        self._CST_GetDLLVersion.restype = c_int

        #
        # CST_OpenProject
        #
        self._CST_OpenProject = self._resultReaderDLL.CST_OpenProject
        self._CST_OpenProject.argtypes = [c_char_p, POINTER(CSTProjHandle)]
        self._CST_OpenProject.restype = c_int

        #
        # CST_CloseProject
        #
        self._CST_CloseProject = self._resultReaderDLL.CST_CloseProject
        self._CST_CloseProject.argtypes = [POINTER(CSTProjHandle)]
        self._CST_CloseProject.restype = c_int

        #
        # CST_GetItemNames
        #
        self._CST_GetItemNames = self._resultReaderDLL.CST_GetItemNames
        self._CST_GetItemNames.argtypes = [POINTER(CSTProjHandle), c_char_p, 
                                           c_char_p, c_int, POINTER(c_int)]
        self._CST_GetItemNames.restype = c_int

        #
        # CST_GetNumberOfResults
        #
        self._CST_GetNumberOfResults = self._resultReaderDLL.CST_GetNumberOfResults
        self._CST_GetNumberOfResults.argtypes = [POINTER(CSTProjHandle), 
                                                c_char_p, POINTER(c_int)]
        self._CST_GetNumberOfResults.restype = c_int

        #
        # CST_GetProjectPath
        #
        self._CST_GetProjectPath = self._resultReaderDLL.CST_GetProjectPath
        self._CST_GetProjectPath.argtypes = [POINTER(CSTProjHandle), 
                                             c_char_p, c_char_p]
        self._CST_GetProjectPath.restype = c_int

        # ----------------------------------------------------------------------
        # 1-D Results 
        # ----------------------------------------------------------------------
        #
        # CST_Get1DResultInfo
        # 
        self._CST_Get1DResultInfo = self._resultReaderDLL.CST_Get1DResultInfo
        self._CST_Get1DResultInfo.argtypes = [POINTER(CSTProjHandle),
                                              c_char_p, c_int, c_int, c_int, 
                                              c_char_p, POINTER(c_int), 
                                              POINTER(c_double)]
        self._CST_Get1DResultInfo.restype = c_int
        
        #
        # CST_Get1DResultSize
        #
        self._CST_Get1DResultSize = self._resultReaderDLL.CST_Get1DResultSize
        self._CST_Get1DResultSize.argtypes = [POINTER(CSTProjHandle),
                                              c_char_p, c_int, POINTER(c_int)]
        self._CST_Get1DResultSize.restype =  c_int
        #
        # CST_Get1DRealDataOrdinate
        #
        self._CST_Get1DRealDataOrdinate = self._resultReaderDLL.CST_Get1DRealDataOrdinate
        self._CST_Get1DRealDataOrdinate.argtypes = [POINTER(CSTProjHandle), 
                                                    c_char_p, c_int, POINTER(c_double)]
        self._CST_Get1DRealDataOrdinate.restype = c_int

        #
        # CST_Get1DRealDataAbszissa
        #
        self._CST_Get1DRealDataAbszissa = self._resultReaderDLL.CST_Get1DRealDataAbszissa
        self._CST_Get1DRealDataAbszissa.argtypes = [POINTER(CSTProjHandle), 
                                                    c_char_p, c_int, POINTER(c_double)]
        self._CST_Get1DRealDataAbszissa.restype = c_int

        #
        # CST_Get1D_2Comp_DAta_Ordinate
        #
        self._CST_Get1D_2Comp_DataOrdinate = self._resultReaderDLL.CST_Get1D_2Comp_DataOrdinate
        self._CST_Get1D_2Comp_DataOrdinate.argtypes = [POINTER(CSTProjHandle),
                                                       c_char_p, c_int, POINTER(c_double)]
        self._CST_Get1D_2Comp_DataOrdinate.restype = c_int

        #-----------------------------------------------------------------------
        # 3-D Results (not yet implemented)
        #-----------------------------------------------------------------------
        #
        # CST_Get3DHexResultInfo
        #
        self._CST_Get3DHexResultInfo = self._resultReaderDLL.CST_Get3DHexResultInfo
        self._CST_Get3DHexResultInfo.argtypes = [POINTER(CSTProjHandle), c_char_p,
                                                 c_int, c_int, c_int,
                                                 c_char_p, POINTER(c_int),
                                                 POINTER(c_double)]
        self._CST_Get3DHexResultInfo.restype = c_int

        #
        # CST_Get3DHexResultSize
        #
        self._CST_Get3DHexResultSize = self._resultReaderDLL.CST_Get3DHexResultSize
        self._CST_Get3DHexResultSize.argtypes = [POINTER(CSTProjHandle), 
                                                 c_char_p, c_int, POINTER(c_int)]
        self._CST_Get3DHexResultSize.restype = c_int
        #
        # CST_Get3DHexResult
        #
        #self._CST_Get3DHexResult = self._resultReaderDLL.CST_Get3DHexResult
        # ---------------------------------------------------------------------
        # Far Fields (not implemented)

        # ---------------------------------------------------------------------
        # Probe Collection (not implemented)

        # ---------------------------------------------------------------------
        # Symmetries / Boundaries (not yet implemented)
        # 
        # CST_GetSymmetries
        # CST_GEtBoundaries

        # ----------------------------------------------------------------------
        # Units (not yet implemented)
        # LENGTH = 1, TEMPERATURE = 2, VOLTAGE = 3, CURRENT = 4, RESISTANCE = 5,
        # CONDUCTANCE = 6, CAPACITANCE = 7, INDUCTANCE = 8, FREQUENCY = 9, 
        # TIME = 10, POWER = 11
        #self._CST_GetUnitScale = self._resultReaderDLL.CST_GetUnitScale
        #self._CST_GetFrequencyScale = self._resultReaderDLL.CST_GetFrequencyScale
        #self._CST_GetTimeScale = self._resultReaderDLL.CST_GetTimeScale
        #self._CST_GetFrequencyMin = self._resultReaderDLL.CST_GetFrequencyMin
        #self._CST_GetFrequencyMax = self._resultReaderDLL.CST_GetFrequencyMax

        # ----------------------------------------------------------------------
        # Excitations (not yet implemented)
        # 

        # ----------------------------------------------------------------------
        # Hexahedral mesh (Only Regular Grids, no Subgrids, no TST)
        # (not yet implemented)
        # CST_GetHexMeshInfo
        self._CST_GetHexMeshInfo = self._resultReaderDLL.CST_GetHexMeshInfo
        self._CST_GetHexMeshInfo.argtypes = [POINTER(CSTProjHandle),
                                             POINTER(c_int)]
        self._CST_GetHexMeshInfo.restype = c_int

        #
        # CST_GetHexMesh
        #
        self._CST_GetHexMesh = self._resultReaderDLL.CST_GetHexMesh
        self._CST_GetHexMesh.argtypes = [POINTER(CSTProjHandle),
                                         POINTER(c_double)]
        self._CST_GetHexMesh.restype = c_int

        # ----------------------------------------------------------------------
        # Hexahedral Materiall Matrix (not yet implemented)
        # matType may be 0: Meps
        #                1: Mmue
        #                2: Mkappa 
        # CST_GetMaterialMatrixHexMesh
        #self._CST_GetMaterialMatrixHexMesh = self._resultReaderDLL.CST_GetMaterialMatrixHexMesh

        # ----------------------------------------------------------------------
        # Bix-file Information from Header (not yet implemented)
        # 
        # CST_GetBixInfo
        #self._CST_GetBixInfo = self._resultReaderDLL.CST_GetBixInfo

        # ----------------------------------------------------------------------
        # BIX-File Information about quantities (not yet implemented)
        # quantity types: Int32 = 1, Int64, Float32, Float64, Vector32, ComplexVector32, Vector64, SerialVector3x32, 
        # SerialVector6x32 = 9 // xre_0 yre_0 zre_0 xim_0 yim_0 zim_0 xre_1 yre_1 ... zim_n
        # UInt32 = 10, UInt64, Int8, UInt8, ComplexScalar32, ComplexScalar64, SerialComplexScalar32, SerialVector3x64
        # CST_GetBixQuantity
        #self._CST_GetBixQuantity = self._resultReaderDLL.CST_GetBixQuantity

        # ----------------------------------------------------------------------
        # BIX-File Information about length of lines
        # CST_GetBixLineLength
        #self._CST_GetBixLineLength = self._resultReaderDLL.CST_GetBixLineLength

        # ----------------------------------------------------------------------
        # Read BIX-File data
        # Call with pointer to allocated memory (n*LineLength, n=3 for vector, n=6 for complex vector, see quantity type)
        # CST_GetBixDataFloat
        # CST_GetBixDataDouble
        # CST_GetBixDataInt32
        # CST_GetBixDataInt64
        #self._CST_GetBixDataFloat = self._resultReaderDLL.CST_GetBixDataFloat
        #self._CST_GetBixDataDouble = self._resultReaderDLL.CST_GetBixDataDouble
        #self._CST_GetBixDataInt32 = self._resultReaderDLL.CST_GetBixDataInt32
        #self._CST_GetBixDataInt64 = self._resultReaderDLL.CST_GetBixDataInt64

        # ----------------------------------------------------------------------
        # Write BIX-File
        # CST_AddBixQuantity
        # CST_AddBixLine
        # CST_WriteBixHeader
        # CST_WriteBixDataDouble
        # CST_WriteBixDataInt32
        # CST_WriteBixDataInt64
        # CST_CloseBixFile
        #self._CST_AddBixQuantity = self._resultReaderDLL.CST_AddBixQuantity
        #self._CST_AddBixLine = self._resultReaderDLL.CST_AddBixLine
        #self._CST_WriteBixHeader = self._resultReaderDLL.CST_WriteBixHeader
        #self._CST_WriteBixDataDouble = self._resultReaderDLL.CST_WriteBixDataDouble
        #self._CST_WriteBixDataInt32 = self._resultReaderDLL.CST_WriteBixDataInt32
        #self._CST_WriteBixDataInt64 = self._resultReaderDLL.CST_WriteBixDataInt64
        #self._CST_CloseBixFile = self._resultReaderDLL.CloseBixFile

    def __enter__(self):
        """ Open CST project upon entering class.
        """
        ret_val = self.open_project()
        if ret_val != 0:
            raise(Exception("CST project file could not be opened (" + 
                            self._cst_project_file + ")"))
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """ Close CST project upon exiting class. 
        """

        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        if self._projh.m_pProj is not None:
            self.close_project()
        return True

    def _get_dll_version(self):
        """Retrieve ResultReaderDLL version.
        """
        rrdll_version = c_int()
        val = self._CST_GetDLLVersion(byref(rrdll_version))
        if val == 0:
            self._dll_version = rrdll_version.value
        else:
            raise(Exception("CST_GetDLLVersion returned error", val))

    @property
    def dll_version(self):
        """Return the version of ResultReaderDLL.
        """
        if self._dll_version is None:
            self._get_dll_version()
        return self._dll_version

    def open_project(self, cst_project_file=None ):
        """Open the CST Project
            Args:
                string: cst_project - CST project file name
            Return: 
                int: Return value - 0 = success
                                    12 = file not found
        """
        if cst_project_file is not None:
            self._cst_project_file = cst_project_file
        project_file_string_buffer = create_string_buffer(self._cst_project_file.encode('utf-8'))
        val = self._CST_OpenProject(project_file_string_buffer, byref(self._projh))
        return val

    def close_project(self):
        """Close the Open CST Project
        Args: None
        Return:
            int: return value
        """
        val = self._CST_CloseProject(byref(self._projh))
        return val 

    def item_names(self, item_tree_path: str) -> list:
        """item_names 
        Get the item names for a given item tree path and the number of elements 
        underneath that tree.
        Args: 
            string: item_tree_path - path of the item in the CST Result Tree.
        Return:
            list: results
        Raises:
            Raises exception when return value from ResultReaderDLL is not 0
            0 - Success
        """
        out_buffer = create_string_buffer(RESULTS_TREE_MAX_PATH)
        out_buffer_len = c_int(RESULTS_TREE_MAX_PATH)
        num_items = c_int(0)
    
        val = self._CST_GetItemNames(byref(self._projh),
                               item_tree_path.encode(),
                               out_buffer, 
                               out_buffer_len,
                               byref(num_items))
        
        item_names = out_buffer.value.decode('utf-8').splitlines()
        if num_items.value != len(item_names):
            raise(Exception("Expected number of results differs from reported: ", 
                            num_items.value, " vs. ", len(item_names)))
        
        if val != 0:
            raise(Exception("ResultReaderDLL::CST_GetItemNames returned error code: " + str(val)))

        return  item_names

    def number_of_results(self, item_tree_path: str) -> int:
        """number_of_results
        Returns the number of results under the result tree.
        Args:
            string: item_tree_path - path of the item in the CST Result Tree.
        Return:
            int: number of results  
        Raises:
            Raises exception when return value from ResultReaderDLL is not 0
            5 - Tree path is not a leaf
        """
        num_items = c_int(0)
        val = self._CST_GetNumberOfResults(byref(self._projh),
                                     item_tree_path.encode(),
                                     byref(num_items))
        print('number of results: ', num_items.value)
        if val != 0:
            raise(Exception("ResultReaderDLL::CST_GetNumberOfResults returned error code: " + str(val)))

        return num_items.value

    def _get_project_path(self, path_type: str) -> None:
        """_get_project_path 
        Args:
            path_type: Path type is "result" or "model3d"
        Return:
            None

        Raises:
            Raises exception when return value from ResultReaderDLL is not 0
            0 - Success
        """
        project_path_buffer = create_string_buffer(RESULTS_TREE_MAX_PATH)
        val = self._CST_GetProjectPath(self._projh,
                                       path_type.encode(),
                                       project_path_buffer)
        if val != 0:
            raise(Exception("ResultReaderDLL::CST_GetProjectPath returned error code: " + str(val)))
        
        result_path = project_path_buffer.value.decode('utf-8')
        if path_type.lower() == 'result':
            self._project_result_path = result_path
        elif path_type.lower() == 'model3d':
            self._project_3d_result_path = result_path
        else:
            raise(Exception("Unknown CST Result Path Type: " + path_type))

    @property
    def project_result_path(self):
        """Return the project Results path.
        """
        if self._project_result_path is None:
            self._get_project_path('Result')

        return self._project_result_path

    @property
    def project_3d_result_path(self):
        """Return the project 3D Results path.
        """
        if self._project_3d_result_path is None:
            self._get_project_path('Model3D')

        return self._project_3d_result_path

    def _get_1d_result_info(self, tree_path_name: str,
                            result_number: int, ) -> int:
        """Get 1D result info.
        This method is of limited usefullness, since most library info features 
        are not implemented in the DLL. It is wrapped as a Python method for 
        completeness.
        Args: 
            tree_path_name (str):  path of 1d result
            result_number (int): result ID number, 0 for most recent. 
                                See CST documentation for simulation result
                                numbering.
        Return:
            Raises exception when return value from ResultReaderDLL is not 0
            0 - Success
            5 - Tree path is not a leaf
        Raises:
        """
        info_array_size = 2**10
        char_buffer_size = 2**25
        c_info_array_size = c_int(info_array_size)
        c_char_buffer_size = c_int(char_buffer_size)
        char_buffer = create_string_buffer("", char_buffer_size)
        i_info_p = (c_int * info_array_size)()
        d_info = c_double(0)

        c_result_number = c_int(result_number)
        print('before get 1d result info: ')
        val = self._CST_Get1DResultInfo(self._projh, tree_path_name.encode(),
                                        c_int(result_number),
                                        c_info_array_size, c_char_buffer_size, 
                                        char_buffer, i_info_p, byref(d_info))
        print('After get 1d result info: ')
        print('Val: ', val)
        print('tree_path: ', tree_path_name)
        #print('c_info: ', type(c_info))
        print('c_info_array_size: ', c_info_array_size.value)
        print('c_char_buffer_size: ', c_char_buffer_size.value)
        #print('d_info: ', d_info.value)
        print(info_buffer.value)
        print('i_info_p: ', i_info_p[0])

        if val != 0:
            raise(Exception("ResultReaderDLL::CST_Get1DResultInfo returned error code: " + str(val)))
        return val

    def _get_1d_result_size(self, tree_path_name: str, 
                            result_number: int ) -> int:
        """Get 1D result size.
        Args:
            tree_path_name : path of the 1d result.
            result_number : result ID number, 0 for most recent.
                                 See CST documentation for simulation result
                                 numbering.
        Return:
            int : number of elements in 1D data structure.
        Raises:
            Raises exception when return value from ResultReaderDLL is not 0
            0 - Success
            4 - Result tree path not valid
            6 - Result number is not found
        """
        c_data_size = c_int(0)
        val = self._CST_Get1DResultSize(self._projh, tree_path_name.encode(),
                                        c_int(result_number), byref(c_data_size))
        if val != 0:
            raise(Exception("ResultReaderDLL::CST_Get1DResultSize returned error code: " + str(val)))

        return c_data_size.value

    def _get_1d_real_data_ordinate(self, tree_path_name: str,
                                   result_number: int) -> np.ndarray:
        """ _get_1d_read_data_ordinate
        Args:
            tree_path_name : path of the 1d result
            result_number : result ID number, 0 for most recent
                                 See CST documentation for simulation result
                                 numbering.
        Returns:
            numpy ndarray :  length=data_length, type=np.float64
        Raises:
            Raises exception when return value from ResultReaderDLL is not 0
            0 - Success
            5 - Value does not have ordinate?
        """
        buffer_size = self._get_1d_result_size(tree_path_name, result_number)
        data_buffer = (c_double*buffer_size)()
        val = self._CST_Get1DRealDataOrdinate(self._projh, tree_path_name.encode(),
                                              c_int(result_number), data_buffer)

        if val != 0:        
            raise(Exception("ResultReaderDLL::CST_Get1DRealDataOrdinate returned error code: " + str(val)))
        return np.array(data_buffer, dtype=np.float64)

    def _get_1d_real_data_abszissa(self, tree_path_name: str,
                                   result_number: int) -> np.ndarray:
        """_get_1d_real_data_abszissa
        Args:
            tree_path_name : path of the 1d result
            result_number  : result ID number, 0 for most recent
                                 See CST documentation for simulation result
                                 numbering.
        Returns:
            numpy ndarray :  length=data_length, type=np.float64
        Raises:
            Raises exception when return value from ResultReaderDLL is not 0
            0 - Success
        """
        buffer_size = self._get_1d_result_size(tree_path_name, result_number)
        data_buffer = (c_double*buffer_size)()
        val = self._CST_Get1DRealDataAbszissa(self._projh, tree_path_name.encode(),
                                              c_int(result_number), data_buffer)

        return np.array(data_buffer, dtype=np.float64)

    def _get_1d_2comp_data_ordinate(self, tree_path_name: str,
                                    result_number: int) -> np.ndarray:
        """_get_1d_2comp_data_ordinate
         Args:
            tree_path_name : path of the 1d result
            result_number : result ID number, 0 for most recent
                                 See CST documentation for simulation result
                                 numbering.
         Returns: 
            numpy ndarray : length=data_length, type
        Raises:
            Raises exception when return value from ResultReaderDLL is not 0
            0 - Success
        """
        buffer_size  = self._get_1d_result_size(tree_path_name, result_number)
        data_buffer = (c_double*(buffer_size*2))()
        val = self._CST_Get1D_2Comp_DataOrdinate(self._projh, tree_path_name.encode(),
                                                c_int(result_number), data_buffer)
        if val != 0:
           raise(Exception("ResultReaderDLL::CST_Get1D_2Comp_DataOrdinate returned error code: " + str(val)))
        
        data_re = np.array(data_buffer[0::2], dtype=np.float64)
        data_im = np.array(data_buffer[1::2], dtype=np.float64)
        return data_re + 1.0j*data_im

    def _get_3d_hex_result_info(self, tree_path_name: str,
                                 result_number: int):
        """_get_3d_hex_result_info
        Args:
        Results:
        Raises:
        """
        info_array_size = 2**8
        char_buffer_size = 2**8
        c_info_array_size = c_int(info_array_size)
        c_char_buffer_size = c_int(char_buffer_size)
        info_buffer = create_string_buffer(char_buffer_size)
        i_info_p = (c_int * info_array_size)()
        d_info = c_double(0)
        
        val = self._CST_Get3DHexResultInfo(self._projh,
                                           tree_path_name.encode(),
                                           c_int(result_number),
                                           c_info_array_size,
                                           c_char_buffer_size,
                                           info_buffer, i_info_p, byref(d_info))

        if val != 0:
            raise(Exception("ResultReaderDLL::CST_Get3DHexResultInfo returned error code: " + str(val)))
        return i_info_p[:]

    def _get_3d_hex_result_size(self, tree_path_name: str, 
                                result_number: int) -> int:
        """_get_3d_hex_result_size
        Args:
        Returns:
            data_size : reported size fo the data 3D data.
        Raises:
        """
        data_size = c_int(0)

        val = self._CST_Get3DHexResultSize(self._projh,
                                           tree_path_name.encode(),
                                           c_int(result_number),
                                           byref(data_size))
        if val != 0:
            raise(Exception("ResultReaderDLL::CST_Get3DHexResultSize returned error code: " + str(val)))

        return data_size.value

    def _get_hex_mesh_info(self) -> tuple:
        """_get_hex_mesh_info
        Args:
        Returns:
        Raises:
        """
        nxyz = (c_int*3)()
        val = self._CST_GetHexMeshInfo(self._projh, nxyz)
        if val != 0:
            raise(Exception("ResultReaderDLL::CST_GetHexMeshInfo returned error code: " + str(val)))

        return tuple(nxyz)

    def _get_hex_mesh(self) -> tuple:
        """_get_hex_mesh
        Args:
        Returns:
        Raises:
        """
        (nx, ny, nz) = self._get_hex_mesh_info()
        nxyz_lines = (c_double*(nx + ny + nz))()
        val = self._CST_GetHexMesh(self._projh, nxyz_lines)
        if val != 0:
            raise(Exception("ResultReaderDLL::CST_GetHexMesh returned error code: " + str(val)))

        return ( nxyz_lines[0:nx], nxyz_lines[0:ny], nxyz_lines[0:nz] )