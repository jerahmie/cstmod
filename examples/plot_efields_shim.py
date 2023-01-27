#!/bin/env python
"""Plot simulation results.
"""
import os
import sys
from collections.abc import Iterable
from tkinter import Tk
#from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfile
import hdf5storage
from math import sqrt, ceil
import numpy as np
import matplotlib.pyplot as plt
from cstmod.field_reader import FieldReaderH5

def efield_shim(e1: np.ndarray, shim_mags: np.ndarray, shim_phases: np.ndarray)->np.ndarray:
    """apply shim"""
    # bfarray_dict = hdf5storage.loadmat(bfmap_file)
    e1_shape = np.shape(e1)
    nchannels = e1_shape[4]
    e1_shim = np.zeros(e1_shape[0:4], dtype=np.complex128)
    for ch in range(nchannels):
        e1_shim += shim_mags[ch]*e1[:,:,:,:,ch]*np.exp(1.0j*shim_phases[ch])
    print(np.shape(e1_shim))
    return e1_shim

#def plot_points(nz, deltaz, z0):
#    """ Calculate values of slices to plot through phantom
#    Args:
#        nz:  number of slices
#        deltaz: distance between slices
#        z0: offset of first slice
#    """
#    return [z0 + deltaz * n for n in range(nz)]
#
#def plot_b1plus_ch(bfmap_file, ch_mags, plot_points_z, mask_file=None):
#    """plot the per-channel masked fields
#    """
#    bfarray_dict = hdf5storage.loadmat(bfmap_file)
#    xmin = -200
#    xmax = 200
#    ymin = -200
#    ymax = 200
#    zmin = -150
#    zmax = 250
#
#    xdim = bfarray_dict['XDim']
#    ydim = bfarray_dict['YDim']
#    zdim = bfarray_dict['ZDim']
#
#    ixmin = np.argmin(np.abs(xdim - xmin))
#    ixmax = np.argmin(np.abs(xdim - xmax))
#    jymin = np.argmin(np.abs(ydim - ymin))
#    jymax = np.argmin(np.abs(ydim - ymax))
#    kzmin = np.argmin(np.abs(zdim - zmin))
#    kzmax = np.argmin(np.abs(zdim - zmax))
#
#    b1 = bfarray_dict['bfMapArrayN']
#    nchannels = np.shape(b1)[4]
#    nfield_components = nxp.shape(b1)[3]
#    
#    if mask_file:
#        sarmask = hdf5storage.loadmat(mask_file)['sarmask_new']
#    #    for ch in range(nchannels):
#    #        for comp in range(nfield_components):
#    #            b1mask = np.multiply(b1[xmin:xmax,ymin:ymax,zmin:zmax,comp,ch],
#    #                                            sarmask[xmin:xmax, ymin:ymax, zmin:zmax]) 
#
#    # calculate z-slices
#    
#    nrows = len(plot_points_z)
#    ncols = nchannels
#    fig, axs = plt.subplots(nrows, ncols)
#    plt.set_cmap('jet')
#    
#    zind_slices = [np.argmin(np.abs(zdim - p)) for p in plot_points_z]
#    print(zind_slices)
#
#    for axx, zind in zip(axs, zind_slices):
#        ch = 0
#        for ayy in axx:
#            plt.sca(ayy)
#            #zind = np.argmin(np.abs(zdim - plot_points[zi]))
#            plt.pcolormesh(np.rot90(1e6*ch_mags[ch]*abs(np.multiply(b1[xmin:xmax,ymin:ymax,zind,0,ch],sarmask[xmin:xmax,ymin:ymax,zind] )),0), vmin=0, vmax=0.1)
#            ayy.set_aspect('equal')
#            ayy.get_yaxis().set_visible(False)
#            ayy.get_xaxis().set_visible(False)
#            ch += 1
#    plt.suptitle("Simulation Self-Decoupled")
#    return fig, axs
#
def plot_efield_shim(e1shim, xdim, ydim, zdim, plot_point=(0,0,0),vmax=None):
    """ Plot the e1 fields with a given phase.
    """

    xmin = xdim[0]
    xmax = xdim[-1]
    ymin = ydim[0]
    ymax = ydim[-1]
    zmin = zdim[0]
    zmax = zdim[-1]

    ixmin = np.argmin(np.abs(xdim - xmin))
    ixmax = np.argmin(np.abs(xdim - xmax))
    jymin = np.argmin(np.abs(ydim - ymin))
    jymax = np.argmin(np.abs(ydim - ymax))
    kzmin = np.argmin(np.abs(zdim - zmin))
    kzmax = np.argmin(np.abs(zdim - zmax))

    e1_shape = np.shape(e1shim)
    #nchannels = b1_shape[-1]
    #nfield_components = b1_shape[3]
    
    nrows = 1
    ncols = 3
    zi = 0
    fig, axs = plt.subplots(nrows, ncols, figsize=(10,3))
    plt.set_cmap('jet')


    e1shim_mag = np.abs(np.sqrt(e1shim[:,:,:,0] * np.conjugate(e1shim[:,:,:,0]) + 
            e1shim[:,:,:,1] * np.conjugate(e1shim[:,:,:,1]) + 
            e1shim[:,:,:,2] * np.conjugate(e1shim[:,:,:,2])))

    if vmax is None:
        vmax = np.max(abs(e1shim_mag))/100.0

    # axial    
    xx,yy = np.meshgrid(xdim[ixmin:ixmax], ydim[jymin:jymax])
    plt.sca(axs[0])
    ax = plt.gca()
    zind = np.argmin(np.abs(zdim-plot_point[2]))
    plt.pcolormesh(np.transpose(xx), np.transpose(yy), abs(e1shim_mag[ixmin:ixmax,jymin:jymax,zind]), vmin=0.0, vmax=vmax)
    ax.set_aspect('equal','box')
    ax.set_title('Axial')

    # coronal
    xx, zz = np.meshgrid(xdim[ixmin:ixmax], zdim[kzmin:kzmax])
    yind = np.argmin(np.abs(ydim - 0.0))
    axs[1].pcolormesh(np.transpose(xx), np.transpose(zz), np.fliplr(abs(e1shim_mag[ixmin:ixmax,yind,kzmin:kzmax])), vmin=0.0, vmax=vmax)
    axs[1].hlines(zmax-plot_point[2], xdim[ixmin+1], xdim[ixmax-1],'w')
    axs[1].set_aspect('equal', 'box')
    axs[1].set_title('Coronal')

    # sagittal 
    plt.sca(axs[1])
    ax = plt.gca()
    yy, zz = np.meshgrid(ydim[jymin:jymax], zdim[kzmin:kzmax])
    xind = np.argmin(np.abs(xdim - 0.0))
    im = axs[2].pcolormesh(np.transpose(yy), np.transpose(zz), np.fliplr(abs(e1shim_mag[xind,jymin:jymax,kzmin:kzmax])), vmin=0.0, vmax=vmax)
    axs[2].hlines(zmax-plot_point[2], ydim[jymin+1], ydim[jymax-1], 'w')
    axs[2].set_aspect('equal', 'box')
    axs[2].set_title('Sagittal')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
    plt.colorbar(im, cax=cbar_ax)

    return axs

#def plot_slices_z(field3d, z_slices, vmax=1.0):
#    """Plot the axial slices at given z-values"""
#    print('field shape: ', np.shape(field3d))
#    (nx, ny, nz) = np.shape(field3d)
#    print('nx: ', nx, 'ny: ', ny, 'nz: ', nz)
#    # plot dimensions
#    nz_slices = len(z_slices)
#    print('nz_slices: ', nz_slices)
#    ncols = int(round(sqrt(nz_slices)))
#    nrows = int(ceil(nz_slices/ncols))
#    
#    fig, axs = plt.subplots(nrows, ncols)
#    plt.set_cmap('jet')
#
#    # calculate z index from plot geometry, current row, column.
#    zindex = lambda nxp, nyp, ncols: nxp*ncols + nyp
#    print(ncols)
#    for nxp, axx in enumerate(axs):
#        for nyp, ayy in enumerate(axx):
#            zind = zindex(nxp, nyp, ncols)
#            if zind < nz_slices:
#                ayy.pcolormesh(1e6*np.rot90(np.abs(field3d[:,:,z_slices[zind]]),3),vmax=vmax)
#                ayy.set_title(str(zind))
#            ayy.set_aspect('equal','box')
#    return fig, axs



def plot_efield_h5(file_name:str, mask=None, plot_point: tuple = (0,0,0), vmin: float=0.0, vmax: float = 500) -> plt.axes:
    """
    Plot a single exported h5 field value
    """
    fr = FieldReaderH5(file_name)
    xdim = fr.xdim
    ydim = fr.ydim
    zdim = fr.zdim
    # plot plane indices
    efields = fr.fields
    print('e-field shapes: ', np.shape(efields))

    if mask is None:
        field_mask = np.ones(np.shape(efields)[0:2])
    else:
        field_mask = mask

    efields_abs = np.transpose(np.abs(np.sqrt(efields[:,:,:,0] * np.conjugate(efields[:,:,:,0]) +
            efields[:,:,:,1] * np.conjugate(efields[:,:,:,1]) +
            efields[:,:,:,2] * np.conjugate(efields[:,:,:,2]))), (2,1,0))
    efields_abs = np.multiply(efields_abs, field_mask)
    fig, axs = plt.subplots(1,3)
    plt.set_cmap('jet')
    # plot axial
    zind = np.argmin(np.abs(zdim-plot_point[2]))
    axs[0].pcolormesh(efields_abs[:,:, zind], vmin=vmin, vmax=vmax)

    # plot coronal
    yind = np.argmin(np.abs(ydim-plot_point[1]))
    axs[1].pcolormesh(efields_abs[:,yind,:], vmin=vmin, vmax=vmax)

    # plot sagittal
    xind = np.argmin(np.abs(xdim-plot_point[0]))
    axs[2].pcolormesh(efields_abs[xind,:,:], vmin=vmin, vmax=vmax)

    return axs

if __name__ == "__main__":
    cst_project_dir = os.path.join(r'/export','data2','jerahmie-data','PTx_Knee_7T',
        'Knee_pTx_7T_DB_Siemens_Duke_One_Legs_Fields_retune_20230124_2') 
    cst_export_3d_dir = os.path.join(cst_project_dir, r'Export', r'3d')
    vopgen_dir = os.path.join(cst_project_dir, r'Export', r'Vopgen') 
    #try:
    #    vopgen_dir
    #except NameError:
    #    Tk().withdraw()
    #    vopgen_dir = askdirectory(title="Vopgen Directory")

    #    print("vopgen_dir = \"" + vopgen_dir.strip() + "\"")

    #efmap_array_file = askopenfile(title="E Fields",
    #                               initialdir='/').name
    efmap_array_file = os.path.join(vopgen_dir,
                                    r'efMapArrayN.mat')
    #bfmap_array_file = os.path.join(vopgen_dir,
    #                                r'b1plus_1w_stim.mat')
    sarmask_file = os.path.join(vopgen_dir,
                                  r'sarmask_aligned.mat')
    print(os.path.dirname(efmap_array_file))
    #sarmask_file = askopenfile(title="Mask File", 
    #               initialdir=os.path.dirname(efmap_array_file)).name

    if not os.path.isfile(efmap_array_file):
        raise FileNotFoundError(efmap_array_file)
        sys.exit()

    if not os.path.isfile(sarmask_file):
        raise FileNotFoundError(sarmask_file)
        sys.exit()
    
    #print("plot the masked field results...")
    # plot per-channel fields
    #nz= 56
    #z0 = 0.0
    #deltaz = 0.005  # slice spacing
    #plot_points_z = plot_points(nz, deltaz, z0)
    #plot_points_z  = [z0 + deltaz * n for n in range(nz)]
    #print(plot_points_z[::-1], plot_points_z.reverse())

    # load b1 data
    print('loading e1 data')
    efdict = hdf5storage.loadmat(efmap_array_file)
    print('Done.')
    # load mask
    print('loading mask file')
    sarmask = hdf5storage.loadmat(sarmask_file)['sarmask_new']

    # shim coefficients are from b1CoeffCpx
    nchannels = 8 
    x0 = 0.0
    y0 = 0.0
    z0 = 0.0

    shim_name = 'incremental'

    if shim_name == 'cplike':
        # shim: cp-like mode
        shim_data_re_im = np.array([-0.01184199-0.24971938j,
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


    elif shim_name == 'random8':
        # shim: random 8
        shim_data_re_im = np.array([-0.03292742+0.24782208j,
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


    
    # shim solution 9
    elif shim_name == 'random9':
    # shim: random 9
        shim_data_re_im = np.array([0.01549426+0.24951939j,
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

    elif shim_name == 'ch1':
        # shim: ch1
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[0] = (1.+0.j)/np.sqrt(2.0)

    elif shim_name == 'ch2':
        # shim: ch2
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[1] = (1.+0.j)/np.sqrt(2.0)

    elif shim_name == 'ch3':
        # shim: ch3
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[2] = (1.+0.j)/np.sqrt(2.0)
  
    elif shim_name == 'ch4':
        # shim: ch4
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[3] = (1.+0.j)/np.sqrt(2.0)

    elif shim_name == 'ch5':
        # shim: ch5
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[4] = (1.+0.j)/np.sqrt(2.0)

    elif shim_name == 'ch6':
        # shim: ch6
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[5] = (1.+0.j)/np.sqrt(2.0)

    elif shim_name == 'ch7':
        # shim: ch7
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[6] = (1.+0.j)/np.sqrt(2.0)

    elif shim_name == 'ch8':
        # shim: ch7
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
        shim_data_re_im[7] = (1.+0.j)/np.sqrt(2.0)

    elif shim_name == 'incremental':
        # uniform phases across channels
        shim_data_re_im = np.array([25.0*np.exp(2.0j*ch*np.pi/nchannels) for ch in np.arange(nchannels)])

    else:
        # zeros phase by default
        shim_data_re_im = np.zeros(nchannels, dtype=complex)
    
    print('shim_name: ', shim_name, " | ",  shim_data_re_im)
    e1 = efield_shim(efdict['efMapArrayN'],
                     np.abs(shim_data_re_im),
                     -1*np.angle(shim_data_re_im))

    # masked E1
    e1_masked = np.ones(np.shape(e1), dtype=np.complex128)
    # mask Ex
    e1_masked[:,:,:,0] = np.multiply(e1[:,:,:,0], sarmask)
    # mask Ey
    e1_masked[:,:,:,1] = np.multiply(e1[:,:,:,1], sarmask)
    # mask Ez
    e1_masked[:,:,:,2] = np.multiply(e1[:,:,:,2], sarmask)
    xdim = efdict['XDim']
    ydim = efdict['YDim']
    zdim = efdict['ZDim']

    # range(150,5,-5)

    #plot_slices_z(b1plus_masked, plot_points(56, -2, 130) ,vmax=0.5)
    ax1 = plot_efield_shim(e1_masked, xdim, ydim, zdim, plot_point=(x0,y0,z0),vmax=500)
    ax2 = plot_efield_h5(os.path.join(cst_export_3d_dir, r'e-field (f=297) [CP].h5'), mask=sarmask,
                   plot_point=(0,0,0), vmax=500)
        
    plt.show()
    
    # save the shim to a matlab file
    
#   export_dict = dict()
#   export_dict['XDim'] = xdim
#   export_dict['YDim'] = ydim
#   export_dict['ZDim'] = zdim
#   export_dict['b1p_shim'] = b1plus
#   export_dict['b1p_shim_masked'] = b1plus_masked
#   export_dict['mask'] = sarmask
#   export_dict['shim_name']  = b1shim_name
#   export_dict['shim_data_re_im'] = shim_data_re_im
#   hdf5storage.savemat(b1shim_name+".mat", export_dict, oned_as='column')
