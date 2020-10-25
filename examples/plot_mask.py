#!/bin/env python
"""Plot the SAR mask 
"""

import os
import sys
import numpy as np
from scipy import constants
import h5py
import hdf5storage
import matplotlib.pyplot as plt


def plot_sar_mask(mask_file):
    """Create a 4x4 grid of axial plots of SAR mask.
    """
    if not os.path.isfile(mask_file):
        raise FileNotFoundError

    sarmask_dict = hdf5storage.loadmat(mask_file)
    sarmask = sarmask_dict['sarmask_new']
    xdim = sarmask_dict['XDim']
    ydim = sarmask_dict['YDim']
    zdim = sarmask_dict['ZDim']
    nrows = 4
    ncols = 4
    
    dz = zdim[1]-zdim[0]
    dzslice = int(np.floor(len(zdim)/(nrows*ncols)))
        
    print(zdim[0], zdim[1])
    zslice = dzslice
    fig, axs = plt.subplots(nrows, ncols)
    for axx in axs:
        for ayy in axx:
            plt.sca(ayy)
            pc = plt.pcolor(sarmask[:,:,zslice], vmin=0, vmax=1)
            zslice += dzslice
            ayy.set_aspect('equal')
    plt.show()

def plot_material_properties(mat_file):
    """Plot the material properties.
    """
    if not os.path.isfile(mat_file):
        raise FileNotFoundError
    material_dict = hdf5storage.loadmat(mat_file)
    print(material_dict.keys())
    epsr = material_dict['epsr']
    sigma_eff = material_dict['sigma_eff']
    xdim = material_dict['XDim']
    ydim = material_dict['YDim']
    zdim = material_dict['ZDim']
    print(xdim)
    nrows = 4
    ncols = 4
    dz = zdim[1]-zdim[0]
    dzslice = int(np.floor(len(zdim)/(nrows*ncols)))
    print(zdim[0], zdim[1])
    zslice = dzslice
    fig, axs = plt.subplots(nrows, ncols)
    for axx in axs:
        for ayy in axx:
            plt.sca(ayy)
            pc = plt.pcolor(np.abs(epsr[:,:,zslice]), vmin=0, vmax=50)
            zslice += dzslice
            ayy.set_aspect('equal')
            plt.colorbar()
    plt.show()    

def plot_mag_b1(bfmaparray_rect_file):
    """Plot the b1_plus magnitudes
     """
    if not os.path.isfile(bfmaparray_rect_file):
        raise FileNotFoundError
    bf_rect_dict = hdf5storage.loadmat(bfmaparray_rect_file)
    print(bf_rect_dict.keys())
    bf_rect = bf_rect_dict['bfMapArrayN']
    xdim = bf_rect_dict['XDim']
    ydim = bf_rect_dict['YDim']
    zdim = bf_rect_dict['ZDim']
    bf_rect_shape = np.shape(bf_rect)
    nchannels = bf_rect_shape[-1]
    
    bf_shape = np.shape(bf_rect)
    print(np.shape(bf_rect[:,:,:,0,0]))
    print(np.shape(bf_rect[:,:,:,:,0]))
    zslice = 100
    plt.pcolor(np.reshape(np.abs(bf_rect[:,:,:,0,0]),(bf_shape[0, bf_shape[1]], bf_shape[2], 1)), vmin=0, vmax=1e-6)
    plt.show()    

def plot_raw_fields_hdf5(hdf5_file, field_type='E-Field'):
    """plot a raw field file
    """

    with h5py.File(hdf5_file, 'r') as dataf:
        fxre = np.transpose(dataf[field_type]['x']['re'], (2, 1, 0))
        fxim = np.transpose(dataf[field_type]['x']['im'], (2, 1, 0))
        fyre = np.transpose(dataf[field_type]['y']['re'], (2, 1, 0))
        fyim = np.transpose(dataf[field_type]['y']['im'], (2, 1, 0))
        fzre = np.transpose(dataf[field_type]['z']['re'], (2, 1, 0))
        fzim = np.transpose(dataf[field_type]['z']['im'], (2, 1, 0))
        
    fx = fxre + 1.0j*fxim
    fy = fyre + 1.0j*fyim
    fz = fzre + 1.0j*fzim
    fmag = 1e6*constants.mu_0*np.sqrt(np.abs(fx*np.conj(fx) + fy*np.conj(fy) + fz*np.conj(fz)))
    plt.pcolor(fmag[:,:,100], vmin=0, vmax=2)
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    #sar_mask_file = os.path.join('/export','raid1','jerahmie-data', \
    #                             'Vopgen','sarmask_aligned.mat')
    vopgen_dir = os.path.join('D:', os.sep, 'Temp_CST','Vopgen')
    sar_mask_file = os.path.join(vopgen_dir,'sarmask_aligned_raw.mat')
    material_file = os.path.join(vopgen_dir, 'mat_properties_raw.mat')
    bfmaparrayn_rect_file = os.path.join(vopgen_dir, 'bfMapArrayN_rect.mat')
    print("Plotting the SAR mask")
    plot_sar_mask(sar_mask_file)
    #plot_material_properties(material_file)
    #plot_mag_b1(bfmaparrayn_rect_file)

    #field_data_dir = os.path.join('D:', os.sep, 'Temp_CST',
    #                              'KU_Ten_32_ELD_Dipole_element_v3_with_Rx32_feeds',
    #                              'Export', '3d')
    
    #plot_raw_fields_hdf5(os.path.join(field_data_dir, 'h-field (f=447) [AC1].h5'), 'H-Field')
