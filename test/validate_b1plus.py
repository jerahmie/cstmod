#!/bin/env python
"""
"""

import os
import sys
import numpy as np
import hdf5storage
import matplotlib.pyplot as plt

try:
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
except ImportError:
    print("module tkinter not found.")

def apply_mask(field_array_n, mask):
    """apply mask to b1 map_array
    """
    field_array_shape = np.shape(field_array_n)
    masked_fields = np.zeros(field_array_shape, dtype=np.complex128)
    nchannels = field_array_shape[4]
    #assert np.shape(mask) == field_array_shape[0:3], "Mask and field array dimensions unequal."
    for ch in range(nchannels):
        for fr in range(2):
            masked_fields[:,:,:,fr,ch] = np.multiply(field_array_n[:,:,:,fr,ch], mask)
    return masked_fields


def index_of_x(xdim, x):
    """
    Get the closest index to a given point in array of distances.
    Args:
        xdim: array of ordered points
        x: value 
    Returns:
        x_index: index of closest value in xdim
    Raises:
        None
    """
    return np.argmin(np.abs(xdim-x))

def plot_diff(b1a, b1b, ch, z_ind, vmax=1e-6):
    """ compare two b1 matrices
    """
    fig, axs = plt.subplots(1,3)
    p0 = axs[0].pcolormesh(np.abs(b1a[:,:,z_ind,0,ch]), vmin=0.0, vmax=vmax)
    plt.colorbar(p0, ax=axs[0])
    p1 = axs[1].pcolormesh(np.abs(b1b[:,:,z_ind,1,ch]), vmin=0.0, vmax=vmax)
    plt.colorbar(p1, ax=axs[1])
    p2 = axs[2].pcolormesh(np.divide(np.abs(b1b[:,:,z_ind,1,ch]),np.abs(b1a[:,:,z_ind,0,ch])), vmin=0.8, vmax=1.2)
    plt.colorbar(p2, ax=axs[2])

    return fig, axs

if __name__ == "__main__":

    # load files
    Tk().withdraw()
    b1plus_cst_fn = askopenfilename(title="CST B1+ fields file")
    b1plus_vopgen_fn = askopenfilename(title="Vopgen fields")
    mask_file = askopenfilename(title="Mask file")
    b1pm_cst = hdf5storage.loadmat(b1plus_cst_fn)
    zdim = b1pm_cst['ZDim']
    #zpos = 0.188 # mid upper ring
    #zpos = 0.20
    zpos = 0.298 # mid lower ring
    b1pm_vopgen = hdf5storage.loadmat(b1plus_vopgen_fn)
    mask = hdf5storage.loadmat(mask_file)['sarmask_new']

    # plot fields
    b1_vopgen_mask = apply_mask(b1pm_vopgen['bfMapArrayN'], mask)
    b1_cst_mask = apply_mask(b1pm_cst['bfMapArrayN'], mask)
    
    fig1, axs1 = plot_diff(b1_cst_mask,
                           b1_vopgen_mask, 
                           15,
                           index_of_x(zdim, zpos))
    plt.show()
