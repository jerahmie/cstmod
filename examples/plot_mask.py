#!/bin/env python
"""Plot the SAR mask 
"""

import os
import sys
import numpy as np
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
            pc = plt.pcolor(sarmask[:,:,zslice])
            zslice += dzslice
            ayy.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    sar_mask_file = os.path.join('/export','raid1','jerahmie-data', \
                                 'Vopgen','sarmask_aligned.mat')
    print("Plotting the SAR mask")
    plot_sar_mask(sar_mask_file)
    
