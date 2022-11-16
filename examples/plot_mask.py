#!/bin/env python
"""Plot the SAR mask 
"""

import os
import numpy as np
from scipy import constants
import h5py
import hdf5storage
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def plot_sar_mask(mask_file: str) -> Figure:
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
            pc = plt.pcolormesh(sarmask[:,:,zslice], vmin=0, vmax=1)
            zslice += dzslice
            ayy.set_aspect('equal')
    return fig
    
def plot_sar_mask_sac(sar_mask: np.ndarray,
                      xdim: np.ndarray, 
                      ydim: np.ndarray,
                      zdim: np.ndarray,
                      plot_point: tuple) -> Figure:
    """Plot the SAR mask Axial, Sagittal, and Coronal planes.
    Attributes:
        mask_file: String of valid mask file path.
        x: 
        y:
        z:
        plot_point: tuple representing the x,y,z position to plot
    
    Returns:
        Matplotlib Figure handle
    """
    fig, axs = plt.subplots(1,3)
    ix = np.argmin(np.abs(xdim-plot_point[0]))
    jy = np.argmin(np.abs(ydim-plot_point[1]))
    kz = np.argmin(np.abs(zdim-plot_point[2]))
    axs[0].pcolormesh(sar_mask[:,:,kz])
    axs[1].pcolormesh(sar_mask[:,jy,:])
    axs[2].pcolormesh(sar_mask[ix,:,:])    
    return fig    

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

    return axs

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
    fig = plt.pcolor(np.reshape(np.abs(bf_rect[:,:,:,0,0]),(bf_shape[0, bf_shape[1]], bf_shape[2], 1)), vmin=0, vmax=1e-6)

    return fig

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
    fig = plt.pcolor(fmag[:,:,100], vmin=0, vmax=2)
    plt.colorbar()
    return fig

def plot_massdensity3d(mass3d_file):
    """plot_massdensity3d
    """
    mdict = hdf5storage.loadmat(mass3d_file)
    xdim = mdict['XDim']
    ydim = mdict['YDim']
    zdim = mdict['ZDim']
    nx = len(xdim)
    ny = len(ydim)
    nz = len(zdim)
    mden3d = mdict['mden3D']
    mden3dm = mdict['mden3Dm']
    fig, axs = plt.subplots(2,3)
    print('shape mden3d: ', np.shape(mden3d))
    print('shape meden3dm: ', np.shape(mden3dm))
    axs[0][0].pcolormesh(mden3d[:,:,int(nz/2)])
    axs[0][1].pcolormesh(mden3d[:,int(ny/2),:])
    im = axs[0][2].pcolormesh(mden3d[int(nx/2),:,:])
    axs[1][0].pcolormesh(mden3dm[:,:,int(nz/2)])
    axs[1][1].pcolormesh(mden3dm[:,int(ny/2),:])
    axs[1][2].pcolormesh(mden3dm[int(nx/2),:,:])
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    plt.colorbar(im, cax=cbar_ax)

    return plt

def plot_propmap(prop_file):
    """plot_propmap
    """
    pdict = hdf5storage.loadmat(prop_file)
    xdim = pdict['XDim']
    ydim = pdict['YDim']
    zdim = pdict['ZDim']
    nx = len(xdim)
    ny = len(ydim)
    nz = len(zdim)
    mdenmap = pdict['mdenMap']
    condmap = pdict['condMap']

    print("units: ", pdict['units'])
    print("mdenmap dims: ", np.shape(mdenmap))
    print("condmap dims: ", np.shape(condmap))
    fig, axs = plt.subplots(4,3)
    axs[0][0].pcolormesh(mdenmap[:,:,int(nz/2)])
    axs[0][1].pcolormesh(mdenmap[:,int(ny/2),:])
    pcm0 = axs[0][2].pcolormesh(mdenmap[int(nx/2),:,:])
    axs[1][0].pcolormesh(condmap[:,:,int(nz/2),0])
    axs[1][1].pcolormesh(condmap[:,int(ny/2),:,0])
    axs[1][2].pcolormesh(condmap[int(nx/2),:,:,0])
    axs[2][0].pcolormesh(condmap[:,:,int(nz/2),1])
    axs[2][1].pcolormesh(condmap[:,int(ny/2),:,1])
    axs[2][2].pcolormesh(condmap[int(nx/2),:,:,1])
    axs[3][0].pcolormesh(condmap[:,:,int(nz/2),2])
    axs[3][1].pcolormesh(condmap[:,int(ny/2),:,2])
    pcm1 = axs[3][2].pcolormesh(condmap[int(nx/2),:,:,2])

    #fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    fig.colorbar(pcm0, ax=axs[0,:], location='right')
    fig.colorbar(pcm1, ax=axs[1:4,:], location='right')

    return fig

if __name__ == "__main__":
    #sar_mask_file = os.path.join('/export','raid1','jerahmie-data', \
    #                             'Vopgen','sarmask_aligned.mat')
    vopgen_dir = os.path.join('/export','disk4','jerahmie-data','PTx_Knee_7T','Knee_pTx_7T_DB_Siemens_Tom_Leg_Phantom_Flip_Fields_retune_20221106_1','Export','Vopgen')
    #vopgen_dir = os.path.join('D:', os.sep, 'Temp_CST','KU_Ten_32_8CH_RL_Tx_Dipole_Tuned_v2_4', 'Vopgen')
    #vopgen_dir = os.path.join('E:', os.sep, 'CST_Field_Post','Self_Decoupled_10r5t_16tx_64Rx_Fields_CST2020_3', 'Export', 'Vopgen')
    sar_mask_file = os.path.join(vopgen_dir,'sarmask_aligned.mat')
    material_file = os.path.join(vopgen_dir, 'mat_properties_raw.mat')
    #massdensity3d_file 
    #propmatfile
    bfmaparrayn_rect_file = os.path.join(vopgen_dir, 'bfMapArrayN_rect.mat')
    print("Plotting the SAR mask")
    sar_dict = hdf5storage.loadmat(sar_mask_file)
    xdim = sar_dict["XDim"]
    ydim = sar_dict["YDim"]
    zdim = sar_dict["ZDim"]
    sar_mask = sar_dict["sarmask_new"]
    #plot_sar_mask(sar_mask_file)
    plot_sar_mask_sac(sar_mask, xdim, ydim, zdim, (0.0, 0.0, 0.0))
    #plot_material_properties(material_file)
    #plot_mag_b1(bfmaparrayn_rect_file)
    #plot_massdensity3d(os.path.join(vopgen_dir, 'massdensityMap3D.mat'))
    #plot_propmap(os.path.join(vopgen_dir, 'propmap.mat'))

    #field_data_dir = os.path.join('D:', os.sep, 'Temp_CST',
    #                              'KU_Ten_32_ELD_Dipole_element_v3_with_Rx32_feeds',
    #                              'Export', '3d')
    
    #plot_raw_fields_hdf5(os.path.join(field_data_dir, 'h-field (f=447) [AC1].h5'), 'H-Field')
    plt.show()
