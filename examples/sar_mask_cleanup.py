#!/bin/env python
"""sar_mask_cleanup.py
Post-process sarmask.  Apply cleanup and filter steps and save as new file.
"""
import sys
import os
import numpy as np
import hdf5storage

def sarmask_cleanup(input_filename, output_filename):
    """Clean up sarmaksk and save to file.
    """
    sarmask_dict = hdf5storage.loadmat(input_filename)
    sarmask = sarmask_dict['sarmask_new']
    xdim = sarmask_dict['XDim']
    ydim = sarmask_dict['YDim']
    zdim = sarmask_dict['ZDim']
    
    x0 = 0.0
    y0 = 0.0
    z0 = 0.0

    mask_radius = 0.100 # mm

    zmax = 0.150 # mm
    zmin = -0.150 # mm
    print('zdim: ', zdim)
    zmax_ind = np.argmin(abs(zdim - zmax))
    zmin_ind = np.argmin(abs(zdim - zmin))

    # zero-out z>zmax, z<zmin
    sarmask[:,:,zmax_ind:-1] = 0
    print('zmin_ind: ', zmin_ind)
    print('zmax_ind: ', zmax_ind)
    sarmask[:,:,0:zmin_ind] = 0
    
    xmin_ind = np.argmin(abs(xdim - (x0 - mask_radius)))
    xmax_ind = np.argmin(abs(xdim - (x0 + mask_radius)))
    ymin_ind = np.argmin(abs(ydim - (y0 - mask_radius)))
    ymax_ind = np.argmin(abs(ydim - (y0 + mask_radius)))

    print('xmin_ind', xmin_ind)
    print('xmax_ind', xmax_ind)
    print('ymin_ind', ymin_ind)
    print('ymax_ind', ymax_ind)

    # zero-out x- and y- regions
    sarmask[0:xmin_ind,:,:] = 0
    sarmask[xmax_ind:-1,:,:] = 0
    for x_ind in range(xmin_ind, xmax_ind):
        y_top = y0 + np.sqrt(mask_radius**2 - (xdim[x_ind]-x0)**2)
        y_top_ind = np.argmin(abs(ydim - y_top))
        y_bottom = y0 - np.sqrt(mask_radius**2 - (xdim[x_ind]-x0)**2)
        y_bottom_ind = np.argmin(abs(ydim - y_bottom))
        sarmask[x_ind,0:y_bottom_ind,:] = 0
        sarmask[x_ind,y_top_ind:-1,:] = 0

    # save cleaned sarmask
    sarmask_dict_clean = dict()
    sarmask_dict_clean[u'sarmask_new'] = sarmask
    sarmask_dict_clean[u'XDim'] = xdim
    sarmask_dict_clean[u'YDim'] = ydim
    sarmask_dict_clean[u'ZDim'] = zdim

    hdf5storage.savemat(output_filename, sarmask_dict_clean, oned_as='column')

if "__main__" == __name__:
    print("Post-processing SAR mask.")
    if 'win32' == sys.platform:
        sarmask_filename = os.path.join(r'F:', os.sep,
                                        r'16Tx_7T_LB Phantom_40mm shield_1_4_1', 
                                        r'Export',
                                        r'3d',
                                        r'Vopgen',
                                        r'sarmask_aligned_raw.mat')
    elif 'linux' == sys.platform:
        sarmask_filename = os.path.join(r'/export',
                                        r'raid1',
                                        r'jerahmie-data',
                                        r'Vopgen',
                                        r'sarmask_aligned_raw.mat')

    if not os.path.exists(sarmask_filename):
        print("Could not find filename: ", sarmask_filename)
        sys.exit(1)

    sarmask_path = os.path.dirname(sarmask_filename)
    
    if not os.path.exists(sarmask_path):
        print("Could not find directory: ", sarmask_path)
    

    sarmask_output_filename = os.path.join(sarmask_path, 'sarmask_aligned.mat')
    sarmask_cleanup(sarmask_filename, sarmask_output_filename)
    print('Done.')
