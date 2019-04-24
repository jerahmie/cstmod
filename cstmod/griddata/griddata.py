# -*- coding: utf-8 -*-
"""Explore cst grid data.

Created on Thu Dec 13 17:58:21 2018

@author: jerahmie
"""

#import os
#import ctypes
import winreg
import sys
#import platform
# try:
# import h5py
# except ImportError:
#    print("Package H5PY missing and will be skipped.  Install package h5py.")
#    
try:
    import numpy
except ImportError:
    print("Numpy package is required to continue.")
    print("Please install Numpy package from your package manager.")
    #    raise ImportError("Please install Numpy package to remove this error.")
    sys.exit(-1)

class GridData(object):
    """
    GridData 
    Object to hold cst simulation grid data.
    """
    def __init__(self):
        temp = None
        
if __name__ == "__main__":
    print("This is a test.")