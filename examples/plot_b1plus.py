#!/bin/env python
"""Plot simulation results.
"""
import os
import sys
import hdf5storage
import numpy as np
import matplotlib.pyplot as plt
from collections.abc import Iterable
from tkinter import Tk
from tkinter.filedialog import askdirectory

def plot_points(nz, deltaz, z0):
    """ Calculate values of slices to plot through phantom
    Args:
        nz:  number of slices
        deltaz: distance between slices
        z0: offset of first slice
    """
    return [z0 + deltaz * n for n in range(nz)]

def plot_b1plus_ch(bfmap_file, ch_mags, plot_points_z, mask_file=None):
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
    #    for ch in range(nchannels):
    #        for comp in range(nfield_components):
    #            b1mask = np.multiply(b1[xmin:xmax,ymin:ymax,zmin:zmax,comp,ch],
    #                                            sarmask[xmin:xmax, ymin:ymax, zmin:zmax]) 

    # calculate z-slices
    
    nrows = len(plot_points_z)
    ncols = nchannels
    fig, axs = plt.subplots(nrows, ncols)
    plt.set_cmap('jet')
    
    zind_slices = [np.argmin(np.abs(zdim - p)) for p in plot_points_z]
    print(zind_slices)

    for axx, zind in zip(axs, zind_slices):
        ch = 0
        for ayy in axx:
            plt.sca(ayy)
            #zind = np.argmin(np.abs(zdim - plot_points[zi]))
            plt.pcolormesh(np.rot90(1e6*ch_mags[ch]*abs(np.multiply(b1[xmin:xmax,ymin:ymax,zind,0,ch],sarmask[xmin:xmax,ymin:ymax,zind] )),0), vmin=0, vmax=0.1)
            ayy.set_aspect('equal')
            ayy.get_yaxis().set_visible(False)
            ayy.get_xaxis().set_visible(False)
            ch += 1
    plt.suptitle("Simulation Self-Decoupled")
    return fig, axs

def plot_b1plus_shim(bfmap_file, shim_mags, shim_phases, plot_point=(0,0,0), mask_file=None):
    """ Plot the b1 fields with a given phase.
    """
    bfarray_dict = hdf5storage.loadmat(bfmap_file)

    xmin = -0.150
    xmax = 0.150
    ymin = -0.150
    ymax = 0.150
    zmin = 0.1
    zmax = 0.5

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
    fig, axs = plt.subplots(nrows, ncols, figsize=(10,3))
    plt.set_cmap('jet')

    # axial    
    xx,yy = np.meshgrid(xdim[ixmin:ixmax], ydim[jymin:jymax])
    plt.sca(axs[0])
    ax = plt.gca()
    zind = np.argmin(np.abs(zdim-plot_point[2]))
    plt.pcolormesh(np.transpose(xx), np.transpose(yy), 1e6*abs(b1_shim[ixmin:ixmax,jymin:jymax,zind]), vmin=0.0, vmax=1.0)
    ax.set_aspect('equal','box')
    ax.set_title('Axial')

    # coronal
    xx, zz = np.meshgrid(xdim[ixmin:ixmax], zdim[kzmin:kzmax])
    yind = np.argmin(np.abs(ydim - 0.0))
    axs[1].pcolormesh(np.transpose(xx), np.transpose(zz), np.fliplr(1e6*abs(b1_shim[ixmin:ixmax,yind,kzmin:kzmax])), vmin=0.0, vmax=1.0)
    axs[1].hlines(zmax-plot_point[2], xdim[ixmin+1], xdim[ixmax-1],'w')
    axs[1].set_aspect('equal', 'box')
    axs[1].set_title('Coronal')

    # sagittal 
    plt.sca(axs[1])
    ax = plt.gca()
    yy, zz = np.meshgrid(ydim[jymin:jymax], zdim[kzmin:kzmax])
    xind = np.argmin(np.abs(xdim - 0.0))
    im = axs[2].pcolormesh(np.transpose(yy), np.transpose(zz), np.fliplr(1e6*abs(b1_shim[xind,jymin:jymax,kzmin:kzmax])), vmin=0.0, vmax=1.0)
    axs[2].hlines(zmax-plot_point[2], ydim[jymin+1], ydim[jymax-1], 'w')
    axs[2].set_aspect('equal', 'box')
    axs[2].set_title('Sagittal')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    plt.colorbar(im, cax=cbar_ax)

    return plt, axs


if __name__ == "__main__":

    vopgen_dir =  "D:/CST_Projects/Self_Decoupled/Self_Decoupled_10r5t_16tx_Cosim_Tune_Match_2/Export/Vopgen"
    try:
        vopgen_dir
    except NameError:
        Tk().withdraw()
        vopgen_dir = askdirectory(title="Vopgen Directory")
        print("vopgen_dir = \"" + vopgen_dir.strip() + "\"")


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
    nz= 9
    z0 = 0.175
    deltaz = 0.02  # slice spaceing
    plot_points_z = plot_points(nz, deltaz, z0)
    print(plot_points_z[::-1], plot_points_z.reverse())
    #plot_b1plus_ch(bfmap_array_file,
    #               1./np.sqrt(16)*np.ones((16), dtype = float),
    #               plot_points_z, sarmask_file)

    # plot zero-phase
    #plot_b1plus_shim(bfmap_array_file,
    #                 np.ones((8), dtype = float),
    #                 np.zeros((8), dtype = float),
    #                 np.arange(-0.10, 0.15, 0.02),
    #                 sarmask_file)


    # shim coefficients are from b1CoeffCpx

    # shim: ch1
    shim_data_re_im_ch1 = np.array([1.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j], dtype=complex)

    # shim: ch2 
    shim_data_re_im_ch2 = np.array([0.+0.j,
                                    1.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j], dtype=complex)
    # shim: ch7
    shim_data_re_im_ch7 = np.array([0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    1.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j,
                                    0.+0.j], dtype=complex)

    # shim: cp-like mode
    shim_data_re_im_cplike = np.array([-0.01184199-0.24971938j,
                                       -0.22589237-0.1071104j,  
                                       -0.23550602-0.08388632j,
                                        0.14713475+0.20211721j,
                                       -0.24588885-0.04515167j,
                                       -0.14483559+0.20377108j,
                                       -0.10531159+0.22673656j,
                                        0.04229996+0.24639544j,
                                       -0.02966685+0.24823352j,
                                        0.20105657+0.1485808j,
                                        0.23753754+0.07794817j,
                                        0.22370263-0.11161154j,
                                        0.24634945+0.04256699j,
                                        0.08441183-0.23531817j,
                                        0.07690808-0.23787633j,
                                       -0.15130578-0.19901397j], dtype=complex)
    # shim: random 8
    shim_data_re_im_random8 = np.array([-0.03292742+0.24782208j,
                                        -0.21384468-0.12950078j,
                                        -0.14390834+0.20442698j,
                                        -0.1146399 -0.22216591j,
                                         0.24278013-0.05964735j,
                                        -0.24992629-0.00607053j,
                                        -0.22044308+0.11791883j,
                                         0.23395988+0.08810661j,
                                        -0.19593719+0.1552695j,
                                        -0.24287012-0.0592799j,
                                        -0.24989404+0.00727787j,
                                        -0.03897027-0.24694396j,
                                        -0.10259736-0.22797759j,
                                        -0.16963674-0.18363926j,
                                        -0.21563548+0.1264964j,
                                         0.20205324+0.14722257j], dtype=complex)

    # shim: random 9
    shim_data_re_im_random9 = np.array([0.01549426+0.24951939j,
                                       -0.07735674-0.2377308j ,
                                        0.22714345+0.10443109j,
                                       -0.21162568-0.1330961j,
                                       -0.10381305+0.22742658j,
                                        0.02165418+0.24906043j,
                                       -0.15255738+0.19805617j, 
                                       -0.16406546+0.1886333j ,
                                       -0.17032496-0.18300112j,
                                        0.21929974-0.12003176j,
                                        0.23783186-0.07704549j,
                                       -0.1532833 +0.19749489j,
                                       -0.15077172-0.19941888j, 
                                        0.18001702-0.17347586j,
                                        0.14815376+0.20137146j,
                                        0.24913421-0.02078815j], dtype=complex)

    nchannels = 16
    x0 = 0.0
    y0 = 0.0
    z0 = 0.23

    if 0:
        plot_b1plus_shim(bfmap_array_file,
                     np.abs(shim_data_re_im_cplike),
                     -1*np.angle(shim_data_re_im_cplike),
                     (x0, y0, z0),
                     sarmask_file)

    # shim solution 8
    if 0:
        plot_b1plus_shim(bfmap_array_file,
                     np.abs(shim_data_re_im_random8), 
                     -1*np.angle(shim_data_re_im_random8),
                     (x0, y0, z0),
                     sarmask_file)
    
    # shim solution 9
    if 1:
        plot_b1plus_shim(bfmap_array_file,
                     np.abs(shim_data_re_im_random9), 
                     -1*np.angle(shim_data_re_im_random9),
                     (x0, y0, z0),
                     sarmask_file)

    if 0:
        plot_b1plus_shim(bfmap_array_file,
                    np.abs(shim_data_re_im_ch1),
                    -1*np.angle(shim_data_re_im_ch1),
                    (x0, y0, z0),
                    sarmask_file)

    if 0:
        plot_b1plus_shim(bfmap_array_file,
                    np.abs(shim_data_re_im_ch2),
                    -1*np.angle(shim_data_re_im_ch2),
                    (x0, y0, z0),
                    sarmask_file)

    if 0:
        plot_b1plus_shim(bfmap_array_file,
                    np.abs(shim_data_re_im_ch7),
                    -1*np.angle(shim_data_re_im_ch7),
                    (x0, y0, z0),
                    sarmask_file)



plt.show()