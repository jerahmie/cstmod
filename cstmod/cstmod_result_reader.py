#!/usr/bin/env python
"""CSTResultReader is a facade to provide a clean python interface to the low-level
(ctypes) calls to functions in CST ResultReaderDLL.dll 
"""

import os
import ctypes
import winreg
import sys
import platform
from cstmod.cstutil import CSTRegInfo


class CSTResultReader(object):
    """Class that wraps the ResultReaderDLL library.
    """
    def __init__(self, cst_version = '2018'):
        rr_dll_path = CSTRegInfo.find_result_reader_dll(cst_version)
        print(rr_dll_path)
        self.rr_dll = ctypes.WinDLL(rr_dll_path)
        print(self.rr_dll)

if "__main__" == __name__:
    crr = CSTResultReader()
