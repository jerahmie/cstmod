#!/bin/env python
"""plot the afi 
"""
import os
import hdf5storage
import numpy as np
import matplotlib.pyplot as plt


def plot_afi_map(afi_file):
    """plot the afi map
    """
    afi_dict = hdf5storage.loadmat(afi_file)
    for key in afi_dict.keys():
        print(key, np.shape(afi_dict[key]))
    plt.pcolor(afi_dict['myAlpha3dCenter_micTperSqrtW_minusCoeff'], vmin=0, vmax=0.4)
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.colorbar()
    plt.show()

def plot_hybrid(afi_file, z_ind):
    """plot the hybrid data
    """
    hybrid_dict = hdf5storage.loadmat(afi_file)
    afi_hybrid = hybrid_dict['b1plusmph']
    afi_hybrid_dim = np.shape(afi_hybrid)
    print(afi_hybrid_dim)
    ncols = afi_hybrid_dim[3]
    nrows = 1
    fig, axs = plt.subplots(nrows,ncols)
    z_ind = 0
    #for axx in axs:
    ch = 0
    for ayy in axs:
        plt.sca(ayy)
        plt.pcolor(np.rot90(np.abs(afi_hybrid[:,:,2,ch]),1), vmin=0, vmax=40)
        ch += 1
        ayy.set_aspect('equal')
        #plt.colorbar()

    plt.show()
    

if __name__ == "__main__":
    afi_base_dir = os.path.join('/export','raid1','jerahmie-data',
                                'Vopgen','afi')
    if not os.path.exists(afi_base_dir):
        raise FileNotFoundError
        sys.exit()
    # cp-mode
    #afi_file = os.path.join(afi_base_dir, 'MR-SE012-AFI_Incremental_250V', 
    #                       'myAlpha3d_micTperSqrtW_minusCoeffMR-ST001-SE012-0001.mat')

    # cp2p
    #afi_file = os.path.join(afi_base_dir, 'MR-SE012-AFI_cp2p_250V',
    #                        'myAlpha3d_micTperSqrtW_minusCoeffMR-ST002-SE012-0001.mat')
    # zero phase
    #afi_file = os.path.join(afi_base_dir, 'MR-SE007-AFI_allZero_250V',
    #                        'myAlpha3d_micTperSqrtW_minusCoeffMR-ST001-SE007-0001.mat')

    afi_hybrid_file = os.path.join(afi_base_dir, 
                                   'DAT184_myAlpha3d_micTperSqrtW_minusCoeffminusCableMR-ST001-SE007-0001.mat.mat')

    
    #plot_afi_map(afi_file)
    plot_hybrid(afi_hybrid_file, 2)
        
