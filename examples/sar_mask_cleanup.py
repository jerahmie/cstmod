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
    #x0_ind = np.argmin(abs(xdim - x0))
    #y0_ind = np.argmin(abs(ydim - y0))
    #z0_ind = np.argmin(abs(zdim - z0))
    mask_radius = 100 # mm

    zmax = 390 # mm
    zmin = 150 # mm
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

    sarmask[0:xmin_ind,:,:] = 0
    sarmask[xmax_ind:-1,:,:] = 0
    sarmask[:,0:ymin_ind,:] = 0
    sarmask[:,ymax_ind:-1,:] = 0
    sarmask_dict_clean = dict()
    sarmask_dict_clean[u'sarmask_new'] = sarmask
    sarmask_dict_clean[u'XDim'] = xdim
    sarmask_dict_clean[u'YDim'] = ydim
    sarmask_dict_clean[u'ZDim'] = zdim

    hdf5storage.savemat(output_filename, sarmask_dict_clean, oned_as='column')

if "__main__" == __name__:
    print("Post-processing SAR mask.")
    sarmask_filename = os.path.join(r'D:', os.sep,
                                    r'CST_Projects', 
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