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
        self._CST_GetItemNames.argtypes = [POINTER(CSTProjHandle), c_char_p, c_char_p,
                                           c_int, POINTER(c_int)]
        self._CST_GetItemNames.restypes = c_int

        #
        # CST_GetNumberOfResults
        #

        #
        # CST_GetProjectPath
        #

        # ----------------------------------------------------------------------
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

    def get_item_names(self, item_tree_path):
        """get_item_names 
        Get the item names for a given item tree path and the number of elements 
        underneath that tree.
        Args: 
            string: item_tree_path - path of the item in the CST item tree
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
                               byref(num_items)
                               )
        
        item_names = out_buffer.value.decode('utf-8').splitlines()
        if num_items.value != len(item_names):
            raise(Exception("Expected number of results differs from reported: ", 
                            num_items.value, " vs. ", len(item_names)))
        return  item_names

def query_resultreaderdll(resultreaderdll_file, cst_project_file):
    """Use the win32com.client to 
    """
    #rrdll = WinDLL(resultreaderdll_file)
    #rrdll.restype = c_int
    #rrdll.argtypes = POINTER(c_int)
    #rrdll_version = c_int()
    resultReaderDLL = WinDLL(resultreaderdll_file)

    #
    # CST_OpenProject
    #
    CST_OpenProject = resultReaderDLL.CST_OpenProject
    CST_OpenProject.argtypes = [c_char_p, POINTER(CSTProjHandle)]
    CST_OpenProject.restype = c_int
    
    #
    # CST_CloseProject
    #
    CST_CloseProject = resultReaderDLL.CST_CloseProject
    CST_CloseProject.argtypes = [POINTER(CSTProjHandle)]
    CST_CloseProject.restype = c_int
    
    #
    # CST_GetItemNames
    #
    CST_GetItemNames = resultReaderDLL.CST_GetItemNames
    CST_GetItemNames.argtypes = [POINTER(CSTProjHandle), c_char_p, c_char_p,
                                 c_int, POINTER(c_int)]
    CST_GetItemNames.restypes = c_int

    project_name = create_string_buffer(cst_project_file.encode('utf-8'))
    #project_name = c_char_p("Hello.cst".encode('utf-8'))

    project_handle = CSTProjHandle()
    project_handle2 = CSTProjHandle()
    project_handle_pointer = pointer(project_handle)

    # open project
    print('project_handle_pointer:', type(project_handle_pointer))
    val = CST_OpenProject(project_name, byref(project_handle))
    print(val, project_name.value)
    print(project_handle.m_pProj)

    # Get item names
    print('----------------------------')
    print('CST_GetItemNames')
    out_buffer = create_string_buffer(1024)
    out_buffer_len = c_int(1024)
    num_items = c_int()
    
    val = CST_GetItemNames(byref(project_handle),
                           b'1D Results\Balance',
                           out_buffer, 
                           out_buffer_len,
                           byref(num_items))
    print('val: ', val)
    print('item_names_buffer: ', out_buffer.value)
    print('out_buffer_len: ', out_buffer_len)
    print('num_items: ', num_items)


    # close project and finish up
    val = CST_CloseProject(byref(project_handle))
    print("Close Project: ", val)
    print(project_handle.m_pProj)
    

if __name__ == "__main__":
    cst_project_file = os.path.join(r'D:\\',r'CST_Projects',r'Simple_Cosim.cst')
    print("CST Project found? ", cst_project_file, ': ', os.path.exists(cst_project_file))
    print("Running ResultReaderDLL query...")
    resultreaderdll_file = CSTRegInfo.find_result_reader_dll('2020')
    print("ResultReaderDLL path: ", resultreaderdll_file)
    query_resultreaderdll(resultreaderdll_file, cst_project_file)
    print("Done.")
