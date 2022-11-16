#!/bin/env python
"""Combine a set of N hdf5 3d field export files into a vopgen format.
"""

import os 
import sys
import re
import h5py
import hdf5storage
import timeit
import functools
import numpy as np
import matplotlib.pyplot as plt
from cstmod.field_reader import padbrackets
#if  sys.platform == 'win32':
import fnmatch

try:
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
except ImportError:
    print("module tkinter not found.")

def read_fields(field_files):
    """write_fields
    Args:
        field_files: sorted list of files to process
        output_file: name of saved matlab file
    Returns:
        XDim, YDim, ZDim, BF array
    Raises:
        None
    """
    nchannels = len(field_files)
    with h5py.File(field_files[0]) as field_dict:
        dim_unit = field_dict['Mesh line x'].attrs['unit']
        print('units: ', dim_unit)
        if dim_unit == b'cm':
            convert_to_m = 0.01
        elif dim_unit == b'mm':
            convert_to_m = 0.001
        else:
            convert_to_m = 1.0
        
        xdim = convert_to_m * field_dict['Mesh line x'][()]
        ydim = convert_to_m * field_dict['Mesh line y'][()]
        zdim = convert_to_m * field_dict['Mesh line z'][()]
        f1_shape = np.shape(field_dict['B-Field']['x']['re'])
        f1_array_shape = (len(xdim), len(ydim), len(zdim), nchannels)
    
    b1_arrayn = np.zeros(f1_array_shape, dtype=np.complex128)

    # data is loaded in Fortran-style order: (z, y, x)
    # the data is re-ordered to (x, y, z)
    for ch, filename in enumerate(field_files):
        with h5py.File(filename, 'r') as data_dict:
            b1xre = np.transpose(data_dict['B-Field']['x']['re'], (2, 1, 0))
            b1xim = np.transpose(data_dict['B-Field']['x']['im'], (2, 1, 0))
            b1yre = np.transpose(data_dict['B-Field']['y']['re'], (2, 1, 0))
            b1yim = np.transpose(data_dict['B-Field']['y']['im'], (2, 1, 0))
            b1zre = np.transpose(data_dict['B-Field']['z']['re'], (2, 1, 0))
            b1zim = np.transpose(data_dict['B-Field']['z']['im'], (2, 1, 0))
        b1_arrayn[:,:,:,ch] = b1zre + 1.0j*b1zim

    return xdim, ydim, zdim, b1_arrayn
   
def write_fields(output_file, xdim, ydim, zdim, b1_arrayn):
    """Write a field dictionary to matfile
    Args: 
        output_file
        XDim, YDim, ZDim, bfarrayn
    Returns:
        None
    Raises:
        None
    """
    # create dict 
    save_dict  = dict()
    save_dict['XDim'] = xdim
    save_dict['YDim'] = ydim
    save_dict['ZDim'] = zdim
    save_dict['bfMapArrayN'] = b1_arrayn
    hdf5storage.savemat(file_name=output_file, mdict=save_dict, oned_as='column')
    if os.path.exists(output_file):
        print("Generated " + output_file)
        print("Done.")

if __name__ == "__main__":
    
    cst_export_dir = None

    Tk().withdraw()
    if cst_export_dir is None:
        cst_export_dir = askdirectory(title="CST Project Directory", initialdir='/')

    vopgen_dir = os.path.join(cst_export_dir, r'Export', r'Vopgen')
    print(vopgen_dir, ' Exists?: ', os.path.exists(vopgen_dir))
    if not os.path.exists(vopgen_dir):
        os.mkdir(vopgen_dir)
    field3d_dir = os.path.join(cst_export_dir, r'Export', r'3d')

    #field3d_str_pattern = os.path.join(field3d_dir, field_pattern)
    
    field3d_export_files = os.listdir(field3d_dir)
    b1p_files = fnmatch.filter(field3d_export_files, padbrackets("B1+ (f=*) [AC*].h5"))
    sorted_b1p_files = sorted(b1p_files, key=lambda fl: int(re.search(r'\[AC' r'([\d]+)\]', fl).group(1)))
    sorted_b1p_files_full  = [os.path.join(field3d_dir, file) for file in sorted_b1p_files]

    b1m_files = fnmatch.filter(field3d_export_files, padbrackets("B1- (f=*) [AC*].h5"))
    sorted_b1m_files = sorted(b1m_files, key=lambda fl: int(re.search(r'\[AC' r'([\d]+)\]', fl).group(1)))
    sorted_b1m_files_full  = [os.path.join(field3d_dir, file) for file in sorted_b1m_files]

    print("B1+ files: ", sorted_b1p_files_full)
    print("B1- files: ", sorted_b1m_files_full) 
    # read fields
    xdim, ydim, zdim, b1p_arrayn = read_fields(sorted_b1p_files_full)
    xdim, ydim, zdim, b1m_arrayn = read_fields(sorted_b1m_files_full)

    # combine b1 fields
    b1p_shape = np.shape(b1p_arrayn)
    b1m_shape = np.shape(b1m_arrayn)
    assert b1p_shape == b1m_shape, "B1 Plus and B1 Minus shapes differ."
    
    b1_arrayn  = np.zeros((b1p_shape[0], b1p_shape[1], b1p_shape[2], 2, b1p_shape[-1]), dtype=np.complex128)
    b1_arrayn[:,:,:,0,:] = b1p_arrayn
    b1_arrayn[:,:,:,1,:] = b1m_arrayn

    write_fields(os.path.join(vopgen_dir,"bfMapArrayN.mat"), xdim, ydim, zdim, b1_arrayn)
    #write_fields(os.path.join(vopgen_dir,"b1plus_cst.mat"), xdim, ydim, zdim, b1_arrayn)
