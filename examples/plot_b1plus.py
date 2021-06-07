#!/bin/env python
"""Plot simulation results.
"""
import os
import sys
import hdf5storage
import numpy as np
import matplotlib.pyplot as plt
from collections.abc import Iterable

def plot_b1plus_ch(bfmap_file, ch_mags, mask_file=None):
    """plot the per-channel masked fields
    """
    bfarray_dict = hdf5storage.loadmat(bfmap_file)
    xmin = -200
    xmax = 200
    ymin = -200
    ymax = 200
    zmin = -150
    zmax = 250

    xdim = bfarray_dict['XDim']
    ydim = bfarray_dict['YDim']
    zdim = bfarray_dict['ZDim']

    ixmin = np.argmin(np.abs(xdim - xmin))
    ixmax = np.argmin(np.abs(xdim - xmax))
    jymin = np.argmin(np.abs(ydim - ymin))
    jymax = np.argmin(np.abs(ydim - ymax))
    kzmin = np.argmin(np.abs(zdim - zmin))
    kzmax = np.argmin(np.abs(zdim - zmax))

    b1 = bfarray_dict['bfMapArrayN']
    nchannels = np.shape(b1)[4]
    nfield_components = np.shape(b1)[3]
    
    if mask_file:
        sarmask = hdf5storage.loadmat(mask_file)['sarmask_new']
        for ch in range(nchannels):
            for comp in range(nfield_components):
                b1mask = np.multiply(b1[xmin:xmax,ymin:ymax,zmin:zmax,comp,ch],
                                                sarmask[xmin:xmax, ymin:ymax, zmin:zmax]) 
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
        plt.pcolor(np.rot90(1e6*ch_mags[ch]*abs(b1[xmin:xmax,ymin:ymax,zind,0,ch]),3))
        ayy.set_aspect('equal')
        ch += 1
    plt.show()

def plot_b1plus_shim(bfmap_file, shim_mags, shim_phases, mask_file=None):
    """ Plot the b1 fields with a given phase.
    """
    plt.set_cmap('jet')
    bfarray_dict = hdf5storage.loadmat(bfmap_file)

    xmin = -200
    xmax = 200
    ymin = -200
    ymax = 200
    zmin = -150
    zmax = 250

    xdim = bfarray_dict['XDim']
    ydim = bfarray_dict['YDim']
    zdim = bfarray_dict['ZDim']

    ixmin = np.argmin(np.abs(xdim - xmin))
    ixmax = np.argmin(np.abs(xdim - xmax))
    jymin = np.argmin(np.abs(ydim - ymin))
    jymax = np.argmin(np.abs(ydim - ymax))
    kzmin = np.argmin(np.abs(zdim - zmin))
    kzmax = np.argmin(np.abs(zdim - zmax))

    b1 = bfarray_dict['bfMapArrayN']
    b1_shape = np.shape(b1)
    nchannels = b1_shape[4]
    nfield_components = b1_shape[3]
    
    if mask_file:
        sarmask = hdf5storage.loadmat(mask_file)['sarmask_new']
        for ch in range(nchannels):
            for comp in range(nfield_components):
                b1[:,:,:,comp,ch] = np.multiply(b1[:,:,:,comp,ch], sarmask)
    # apply shim
    b1_shim = np.zeros((b1_shape[0], b1_shape[1], b1_shape[2]),
                       dtype=np.complex128)

    for ch in range(nchannels):
        b1_shim += shim_mags[ch]*b1[:,:,:,comp,ch]*np.exp(1.0j*shim_phases[ch])

    nrows = 1
    ncols = 3
    zi = 0
    fig, axs = plt.subplots(nrows, ncols)
    #if not isinstance(axs, Iterable):
    #    axs = [axs]
    # axial    
    xx,yy = np.meshgrid(xdim[ixmin:ixmax], ydim[jymin:jymax])
    plt.sca(axs[0])
    ax = plt.gca()
    zind = np.argmin(np.abs(zdim - 0.0))
    plt.pcolor(xx, yy, np.rot90(1e6*abs(b1_shim[ixmin:ixmax,jymin:jymax,zind])), vmin=0.0, vmax=0.6)
    ax.  set_aspect('equal')
    plt.colorbar()

    # sagittal 
    plt.sca(axs[1])
    ax = plt.gca()
    yy, zz = np.meshgrid(ydim[jymin:jymax], zdim[kzmin:kzmax])
    xind = np.argmin(np.abs(xdim - 0.0))
    plt.pcolor(yy, zz, np.rot90(1e6*abs(b1_shim[xind,jymin:jymax,kzmin:kzmax])), vmin=0.0, vmax=0.6)
    ax.  set_aspect('equal')
    plt.colorbar()

    # coronal
    plt.sca(axs[2])
    ax = plt.gca()
    xx, zz = np.meshgrid(xdim[ixmin:ixmax], zdim[kzmin:kzmax])
    yind = np.argmin(np.abs(ydim - 0.0))
    plt.pcolor(xx, zz, np.rot90(1e6*abs(b1_shim[ixmin:ixmax,yind,kzmin:kzmax])), vmin=0.0, vmax=0.6)
    ax.  set_aspect('equal')
    plt.colorbar()
    plt.show()
            

if __name__ == "__main__":
    #vopgen_dir = os.path.join(r'D:', os.sep,
    #                          r'Temp_CST',
    #                          r'KU_Ten_32_ELD_Dipole_element_v3_with_Rx32_feeds',
    #                          r'Vopgen')

    #vopgen_dir = os.path.join(r'D:', os.sep,
    #                         r'Temp_CST',
    #                         r'KU_Ten_32_ELD_Dipole_element_v3_with_Rx32_feeds_hard_ground',
    #                          r'Vopgen')

    vopgen_dir = os.path.join(r'D:', os.sep,
                             r'Temp_CST', r'Vopgen',
                             r'KU_ten_32_Tx_MRT_23Jul2019',
                              r'Vopgen')
                              
    #vopgen_dir = os.path.join(r'D:', os.sep,
    #                          r'Temp_CST',
    #                          r'KU_Ten_32_8CH_RL_Tx_Dipole_Tuned_v2_4',
    #                          r'Vopgen')



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
    #plot_b1plus_ch(bfmap_array_file,
    #               1.0/np.sqrt(8)*np.ones((8), dtype = np.float),
    #               sarmask_file)

    # plot zero-phase
    #plot_b1plus_shim(bfmap_array_file,
    #                 np.ones((8), dtype = np.float),
    #                 np.zeros((8), dtype = np.float),
    #                 np.arange(-0.10, 0.15, 0.02),
    #                 sarmask_file)

    # plot cp-like mode
    nchannels = 16
    plot_b1plus_shim(bfmap_array_file,
                     1.0/np.sqrt(nchannels)*np.ones((nchannels), dtype = np.float64),
                     np.array([a/nchannels*2.0*np.pi for a in np.arange(0,nchannels)]),
                     sarmask_file)

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
