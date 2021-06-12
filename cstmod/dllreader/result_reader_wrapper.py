"""A wrapper class for the CST ResultReaderDLL.
Warning - The ResustReaderDLL has been marked as deprecated since CST2019, 
though it is included in CST2020 and CST2021.  A migration path that includes 
all functionality for the CST Result Reader has yet to be announced by CST or 
Dassault Systemmes.  JWR 6/10/2021
"""
import os
import traceback
from ctypes import *

try:
    import win32com.client as win32
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
    def __init__(self, cst_project_file, cst_version):
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
        self._CST_GetItemNames.restypes = c_int

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

        # ---------------------------------------------------------------------
        # 1-D Results (not yet implemented)
        # 
        # CST_Get1DResultInfo
        # CST_Get1DResultSize
        # CST_Get1DRealDataOrdinate
        # CST_Get1DRealDataAbszissa
        # CST_Get1D_2Comp_DAta_Ordinate

        #-----------------------------------------------------------------------
        # 3-D Results (not yet implemented)
        #
        # CST_Get3DHexResultInfo
        # CST_Get3DHexResultSize
        # CST_Get3DHexResult

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

        # ----------------------------------------------------------------------
        # Excitations (not yet implemented)
        # 

        # ----------------------------------------------------------------------
        # Hexahedral mesh (Only Regular Grids, no Subgrids, no TST)
        # (not yet implemented)
        # CST_GetHexMeshInfo
        # CST_GetHexMesh

        # ----------------------------------------------------------------------
        # Hexahedral Material Matrix (not yet implemented)
        # matType may be 0: Meps
        #                1: Mmue
        #                2: Mkappa 
        # CST_GetMaterailMatrixHexMesh

        # ----------------------------------------------------------------------
        # Bix-file Information from Header (not yet implemented)
        # 
        # CST_GetBixInfo

        # ----------------------------------------------------------------------
        # BIX-File Information about quantities (not yet implemented)
        # quantity types: Int32 = 1, Int64, Float32, Float64, Vector32, ComplexVector32, Vector64, SerialVector3x32, 
        # SerialVector6x32 = 9 // xre_0 yre_0 zre_0 xim_0 yim_0 zim_0 xre_1 yre_1 ... zim_n
        # UInt32 = 10, UInt64, Int8, UInt8, ComplexScalar32, ComplexScalar64, SerialComplexScalar32, SerialVector3x64
        # CST_GetBixQuantity

        # ----------------------------------------------------------------------
        # BIX-File Information about length of lines
        # CST_GetBixLineLength

        # ----------------------------------------------------------------------
        # Read BIX-File data
        # Call with pointer to allocated memory (n*LineLength, n=3 for vector, n=6 for complex vector, see quantity type)
        # CST_GetBixDataFloat
        # CST_GetBixDataDouble
        # CST_GetBixDataInt32
        # CST_GetBixDataInt64

        # ----------------------------------------------------------------------
        # Write BIX-File
        # CST_AddBixQuantity
        # CST_AddBixLine
        # CST_WriteBixHeader
        # CST_WriteBixDataDouble
        # CST_WriteBixDataInt32
        # CST_WriteBixDataInt64
        # CST_CloseBixFile


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

    def open_project(self, cst_project_file=None):
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

    def item_names(self, item_tree_path):
        """item_names 
        Get the item names for a given item tree path and the number of elements 
        underneath that tree.
        Args: 
            string: item_tree_path - path of the item in the CST Result Tree.
        Return:
            list: results
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

    def number_of_results(self, item_tree_path):
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

    def _get_project_path(self, path_type):
        """_get_project_path 
        Args:
            None
        Return:
            string: Patch of the CST Project file

        Raises:

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