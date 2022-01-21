#!/bin/env python
"""plot the afi 
"""
import os
import hdf5storage
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def plot_afi_map_center(b1plus_map,  vmin=0.0, vmax=1.0):
    """plot the afi map
    """
    #afi_dict = hdf5storage.loadmat(afi_file)
    #plt.pcolormesh(afi_dict['myAlpha3dCenter_micTperSqrtW_minusCoeff'], vmin=0, vmax=0.4)
    plt.pcolormesh(b1plus_map, vmin=vmin, vmax=vmax)
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.colorbar()

    return ax

def plot_afi_map3(b1plus_map, delta_xyz, vmin=0.0, vmax=1.0):
    """plot the axial, coronal, and sagittal
    """
    dx = delta_xyz[0]
    dy = delta_xyz[1]
    dz = delta_xyz[2]
    nx, ny, nz = np.shape(b1plus_map)
    
    makedim = lambda dx, nx: np.linspace(-1*round(nx/2)*dx, round(nx/2)*dx, num=nx, endpoint=False)
    gs_kw = dict(width_ratios=[2, ny/nz, nx/nz], height_ratios=[1])

    xdim = makedim(dx, nx)
    ydim = makedim(dy, ny)
    zdim = makedim(dz, nz)
    fig, axs = plt.subplots(1,3, sharey='col', gridspec_kw=gs_kw, figsize=(10, 3))
    plt.set_cmap('jet')
    
    pos2ind = lambda x, xdim: np.argmin(np.abs(xdim-x))

    #xind = pos2ind(x, xdim)
    #yind = pos2ind(y, ydim)
    zind = pos2ind(0, zdim)
    
    #zind = int(round(nz/2))

    print(zdim)
    print(zind)
    # Axial
    XX, YY = np.meshgrid(ydim, xdim)
    print('xx, zz: {}, {}'.format(np.shape(XX), np.shape(YY)))
    print('b1plus_map: {}'.format(np.shape(b1plus_map[:,:,int(round(nz/2))])))    
    axs[0].set_title('Axial')
    axs[0].pcolormesh(XX, YY, np.fliplr(b1plus_map[:,:,zind]), vmin=vmin, vmax=vmax)
    axs[0].set_aspect('equal', 'box')
    
    # Coronal
    YY, ZZ = np.meshgrid(ydim, zdim)
    print('yy, zz: {}, {}'.format(np.shape(YY), np.shape(ZZ)))
    print('b1plus_map: {}'.format(np.shape(b1plus_map[int(round(nx/2)),:,:])))
    axs[1].set_title('Coronal')
    axs[1].pcolormesh(YY, ZZ, np.rot90(b1plus_map[int(round(nx/2)),:,:],3), vmin=vmin, vmax=vmax)
    axs[1].set_aspect('equal', 'box')
    axs[1].hlines(0, ydim[0], ydim[-1], 'w')

    # Sagittal
    XX, ZZ = np.meshgrid(xdim, zdim)
    print('xx, zz: {}, {}'.format(np.shape(XX), np.shape(ZZ)))
    print('b1plus_map: {}'.format(np.shape(b1plus_map[:,int(round(ny/2)),:])))    
    axs[2].set_title('Sagittal')
    im = axs[2].pcolormesh(XX, ZZ, np.fliplr(np.rot90(b1plus_map[:,int(round(ny/2)),:],3)), vmin=vmin, vmax=vmax)
    axs[2].set_aspect('equal', 'box')
    axs[2].hlines(0, xdim[0], xdim[-1], 'w')

    plt.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    plt.colorbar(im, cax=cbar_ax)

    return fig, axs


def plot_hybrid(afi_map):
    """plot the hybrid data
    """
    afi_map_dim = np.shape(afi_map)
    print(afi_map_dim)
    nrows = afi_map_dim[2]
    ncols = afi_map_dim[3]
    
    fig, axs = plt.subplots(nrows,ncols)
    plt.set_cmap('jet')
    z_ind = 0
    for axx in axs:
        ch = 0
        for ayy in axx:
            plt.sca(ayy)
            im = plt.pcolormesh(np.rot90(1/28*np.abs(afi_map[:,:,z_ind,ch]),1), vmin=0, vmax=1)
            ch += 1
            ayy.set_aspect('equal')
            ayy.get_xaxis().set_visible(False)
            ayy.get_yaxis().set_visible(False)
        z_ind += 1
    fig.subplots_adjust(left=0.2, right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    fig.colorbar(im, cax=cbar_ax)

    row_labels = ['z{}'.format(n) for n in range(nrows)]
    for ax, row in zip(axs[:,0], row_labels):
        print(ax,row)
        ax.get_yaxis().set_visible(True)
        ax.get_yaxis().set_ticks([])
        ax.set_ylabel(row, rotation=0, size='large')

    col_labels = ['Ch{}'.format(coil+1) for coil in range(ncols)] 
    for ax, col in zip(axs[0], col_labels):
        print(ax, col)
        ax.set_title(col)
    plt.suptitle("Experimental AFI 20211213 64Rx")

    return fig, axs



if __name__ == "__main__":
    #afi_base_dir = os.path.join('/export','raid1','jerahmie-data',
    #                            'Vopgen','afi')
    #if not os.path.exists(afi_base_dir):
    #    raise FileNotFoundError
    #    sys.exit()
    # cp-mode
    #afi_file = os.path.join(afi_base_dir, 'MR-SE012-AFI_Incremental_250V', 
    #                       'myAlpha3d_micTperSqrtW_minusCoeffMR-ST001-SE012-0001.mat')

    # cp2p
    #afi_file = os.path.join(afi_base_dir, 'MR-SE012-AFI_cp2p_250V',
    #                        'myAlpha3d_micTperSqrtW_minusCoeffMR-ST002-SE012-0001.mat')
    # zero phase
    #afi_file = os.path.join(afi_base_dir, 'MR-SE007-AFI_allZero_250V',
    #                        'myAlpha3d_micTperSqrtW_minusCoeffMR-ST001-SE007-0001.mat')

    #afi_hybrid_file = os.path.join(afi_base_dir, 
    #                               'DAT184_myAlpha3d_micTperSqrtW_minusCoeffminusCableMR-ST001-SE007-0001.mat.mat')


    #try:
    #    afi_hybrid_file
    #except NameError:
    #    Tk().withdraw()
    #    afi_hybrid_file = askopenfilename(title="AFI Hybrid File")
    #afi_dict = hdf5storage.loadmat(afi_hybrid_file)
    #fig1, axs1 = plot_hybrid(afi_dict['b1plusmph'])

    try:
        afi_shim_file
    except NameError:
        Tk().withdraw()
        afi_shim_file = askopenfilename(title="AFI Hybrid Shim Solution")
    afi_shim_dict = hdf5storage.loadmat(afi_shim_file)

    axs2 = plot_afi_map_center(afi_shim_dict['myAlpha3dCenter_micTperSqrtW_minusCoeff'], vmax=0.4)
    fig3, axs3 = plot_afi_map3(afi_shim_dict['myAlpha3d_micTperSqrtW_minusCoeff'], (2,2,5), vmax=0.4)

    plt.show()
