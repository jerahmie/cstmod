#!/bin/env python
"""Plot simulation results.
"""

import os
import sys
import hdf5storage
import numpy as np
import matplotlib.pyplot as plt
from collections.abc import Iterable

def plot_b1plus_ch(bfmap_file, ch_mags, plot_points, mask_file=None):
    """plot the per-channel masked fields
    """
    bfarray_dict = hdf5storage.loadmat(bfmap_file)

    xdim = bfarray_dict['XDim']
    ydim = bfarray_dict['YDim']
    zdim = bfarray_dict['ZDim']

    b1 = bfarray_dict['bfMapArrayN']
    nchannels = np.shape(b1)[4]
    nfield_components = np.shape(b1)[3]
    
    if mask_file:
        mask_dict = hdf5storage.loadmat(mask_file)
        for ch in range(nchannels):
            for comp in range(nfield_components):
                b1[:,:,:,comp,ch] = np.multiply(b1[:,:,:,comp,ch],
                                                mask_dict['sarmask_new']) 
    nrows = len(plot_points)
    ncols = nchannels
    fig, axs = plt.subplots(nrows, ncols)
    zi = -1
    #    for axx in axs:
    #        ch = 0
    #        zi += 1
    #        if not isinstance(axx, Iterable):
    #            axx = [axx]
    #
    ch = 0
    for ayy in axs:
        plt.sca(ayy)
        zind = np.argmin(np.abs(zdim - plot_points[zi]))
        plt.pcolor(np.rot90(1e6*ch_mags[ch]*abs(b1[60:190,60:190,zind,0,ch]),3))
        ayy.set_aspect('equal')
        ch += 1
    plt.show()

def plot_b1plus_shim(bfmap_file, shim_mags, shim_phases,
                     plot_points, mask_file=None):
    """ Plot the b1 fields with a given phase.
    """
    bfarray_dict = hdf5storage.loadmat(bfmap_file)

    xdim = bfarray_dict['XDim']
    ydim = bfarray_dict['YDim']
    zdim = bfarray_dict['ZDim']

    b1 = bfarray_dict['bfMapArrayN']
    b1_shape = np.shape(b1)
    nchannels = b1_shape[4]
    nfield_components = b1_shape[3]
    
    if mask_file:
        mask_dict = hdf5storage.loadmat(mask_file)
        for ch in range(nchannels):
            for comp in range(nfield_components):
                b1[:,:,:,comp,ch] = np.multiply(b1[:,:,:,comp,ch],
                                                mask_dict['sarmask_new'])
    # apply shim
    b1_shim = np.zeros((b1_shape[0], b1_shape[1], b1_shape[2]),
                       dtype=np.complex)

    for ch in range(nchannels):
        b1_shim += shim_mags[ch]*b1[:,:,:,comp,ch]*np.exp(1.0j*shim_phases[ch])

    nrows = len(plot_points)
    ncols = 1
    zi = 0
    fig, axs = plt.subplots(nrows, ncols)
    if not isinstance(axs, Iterable):
        axs = [axs]
        
    for ayy in axs:
        plt.sca(ayy)
        zind = np.argmin(np.abs(zdim - plot_points[zi]))
        plt.pcolor(1e6*abs(b1_shim[:,:,zind]), vmin=0.0, vmax=0.4)
        zi += 1
        ayy.set_aspect('equal')
        plt.colorbar()
    plt.show()
            

if __name__ == "__main__":
    vopgen_dir = os.path.join(r'/export',
                              r'raid1',
                              r'jerahmie-data',
                              r'Vopgen')

    bfmap_array_file = os.path.join(vopgen_dir,
                                    r'bfMapArrayN.mat')
    sarmask_file = os.path.join(vopgen_dir,
                                  r'sarmask_aligned.mat')

    if not os.path.isfile(bfmap_array_file):
        raise FileNotFoundError(bfmap_array_file)
        sys.exit()

    if not os.path.isfile(sarmask_file):
        raise FileNotFoundError(sarmask_file)
        sys.exit()
    
    print("plot the masked field results...")
    # plot per-channel fields
    plot_b1plus_ch(bfmap_array_file,
                   1.0/np.sqrt(8)*np.ones((8), dtype = np.float),
                   np.array([0.0]),
                   sarmask_file)

    # plot zero-phase
    #plot_b1plus_shim(bfmap_array_file,
    #                 np.ones((8), dtype = np.float),
    #                 np.zeros((8), dtype = np.float),
    #                 np.arange(-0.10, 0.15, 0.02),
    #                 sarmask_file)

    # plot cp-like mode
    #plot_b1plus_shim(bfmap_array_file,
    #                 1.0/np.sqrt(8.0)*np.ones((8), dtype = np.float),
    #                 np.array([a/8.0*2.0*np.pi for a in np.arange(0,8)]),
    #                 np.array([0.0]),
    #                 sarmask_file)

    # plot cp-2+
    #plot_b1plus_shim(bfmap_array_file,
    #                 1.0/np.sqrt(8.0)*np.ones((8), dtype = np.float),
    #                 np.array([a/8.0*4.0*np.pi for a in np.arange(0,8)]),
    #                 np.array([0.0]),
    #                 sarmask_file)
    
    # plot zero-phase
    #plot_b1plus_shim(bfmap_array_file,
    #                 1.0/np.sqrt(8.0)*np.ones((8), dtype = np.float),
    #                 np.zeros((8), dtype = np.float),
    #                 np.array([0.0]),
    #                 sarmask_file)
