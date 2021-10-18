"""A script to query ResultReaderDLL.
"""
import os
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


class CSTProjHandle(Structure):
    _fields_ = [("m_pProj", c_void_p)]


def query_resultreaderdll(resultreaderdll_file, cst_project_file):
    """Use the win32com.client to 
    """
    resultReaderDLL = WinDLL(resultreaderdll_file)
    #rrdll = WinDLL(resultreaderdll_file)
    #rrdll.restype = c_int
    #rrdll.argtypes = POINTER(c_int)
    rrdll_version = c_int()
    
    #
    # CST_GetDLLVersion
    #
    #val = rrdll.CST_GetDLLVersion(byref(rrdll_version))
    CST_GetDLLVersion = resultReaderDLL.CST_GetDLLVersion
    CST_GetDLLVersion.argtypes = [POINTER(c_int)]
    CST_GetDLLVersion.restype = c_int
    val = CST_GetDLLVersion(byref(rrdll_version))
    print(val, ', ', rrdll_version)

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
    #print('project_handle: ', type(project_handle))
    project_handle_pointer = pointer(project_handle)
   # projh = project_handle_pointer()

    # open project
    print('project_handle_pointer:', type(project_handle_pointer))
    val = CST_OpenProject(project_name, byref(project_handle))
    print(val, project_name.value)
    print(project_handle.m_pProj)

    # Get item names
    #tree_path_name = create_string_buffer("1D Results")
    print('----------------------------')
    print('CST_GetItemNames')
    out_buffer = create_string_buffer(1024)
    out_buffer_len = c_int(32)
    num_items = c_int(1)
    
    val = CST_GetItemNames(byref(project_handle),
                           b'1D Results\Balance\Balance [2]',
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
