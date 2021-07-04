"""Cosimulation tools
Implement the combine field step of co-simulation.  This is currently breaking 
in some CST projects.
"""
import sys
import os
import h5py
import hdf5storage
import numpy as np
import matplotlib.pyplot as plt
from cstmod.cstutil import find_cst_files, sort_cst_results_export
from cstmod.cosimulation import *
import cstmod.field_reader as field_reader

def ac_combine_fields(field_files, weights):
    """Combine fields 
    Args: 
        field_files: list of full file paths 
        
    Returns: 
        exports field file in an hdf5 format
    Raises: 
    """
    # Initialize Numpy storage space by reading first field result
    # Initialized ndarrays are more efficient than appended
    print('[ac_combine_fields] file: ', field_files[0])
    fr0 = field_reader.FieldReaderH5(field_files[0])
    xdim = fr0.xdim
    ydim = fr0.ydim
    zdim = fr0.zdim
    combined_fields = weights[0]*fr0.fields
    field_type = fr0.field_type
    
    # combine the remaining fields
    for i, ff in enumerate(field_files[1:]):
        print('[ac_combine_fields] file: ', ff)
        fr = field_reader.FieldReaderH5(ff)
        combined_fields = np.add(combined_fields, np.multiply(weights[i+1],fr.fields))
        print('[ac_combine_fields] freeing field reader')
        del fr

    combined_fields_dict = dict()
    combined_fields_dict['xdim'] = xdim
    combined_fields_dict['ydim'] = ydim
    combined_fields_dict['zdim'] = zdim
    combined_fields_dict[field_type] = combined_fields

    return combined_fields_dict
    
def magnitude_3d(fields):
    """magnitude_3d
    Args:
        fields: ndarray of type complex128.  dimensions (xdim, ydim, zdim, 3)
    Returns:
        ndarray representing the magnitude of the 3d field array. 
                type = float64, dimensions = (xdim, ydim, zdim)
    """
    return np.abs(np.sqrt(np.multiply(fields[:,:,:,0], np.conj(fields[:,:,:,0])) +
                          np.multiply(fields[:,:,:,1], np.conj(fields[:,:,:,1])) +
                          np.multiply(fields[:,:,:,2], np.conj(fields[:,:,:,2]))))

def plot_fields(file_name):
    """plot the fields
    """
    h_fields_dict = hdf5storage.loadmat(file_name)
    h_fields = magnitude_3d(h_fields_dict['h-field'])
    print('h_fields: ', np.shape(h_fields))
    xdim = h_fields_dict['xdim']
    ydim = h_fields_dict['ydim']
    zdim = h_fields_dict['zdim']
    x1 = -65
    x2 = 65
    y1 = -65
    y2 = 65
    z1 = 0
    z2 = 176 # mm
    xind_min = np.argmin(np.abs(xdim - x1))
    xind_max = np.argmin(np.abs(xdim - x2))
    yind_min = np.argmin(np.abs(ydim - y1))
    yind_max = np.argmin(np.abs(ydim - y2))
    zind_min = np.argmin(np.abs(zdim - z1))
    zind_max = np.argmin(np.abs(zdim - z2))

    nrows = 6
    ncols = 6
    fig, axs = plt.subplots(nrows,ncols)
    zind = zind_min
    for i in range(nrows):
        for j in range(ncols):
            im = axs[i][j].pcolor((1/50)*h_fields[zind,yind_min:yind_max,xind_min:xind_max], vmin=0, vmax=10)
            zind += 1
            axs[i][j].set_title(zind)
            plt.colorbar(im, ax=axs[i,j])
    plt.show()

def main(combine_dir, combine_name, frequency_0): 
    """Combine fields from AC combine fields step.
    Args:
        combine_dir: 
        combine_name:
        frequency_0: 
    Returns:
    Raises:
    """
    h_field_files = sort_cst_results_export(find_cst_files(os.path.join(results_dir,'3d',r'h-field*.h5')))
    print("Using following h-fields for field combine steps: ")
    print(h_field_files)
    ac_combine_dirs = find_cst_files(os.path.join(results_dir, r'AC*'))
    print('combine_dirs: ', ac_combine_dirs)
    for ac_dir in ac_combine_dirs:
        print("Processing AC combine directory: ", ac_dir)
        combined_fields = ac_combine_fields(h_field_files, power_from_ports(ac_dir, frequency_0))

        # save combined fields
        print('[main] saving combined_fields_' + os.path.basename(ac_dir) )
        hdf5storage.savemat(r'combined_fields_' + os.path.basename(ac_dir) +  r'.mat', combined_fields)
        
        # free memory
        print('[main] freeing combined_fields dictionary from RAM')
        del combined_fields
        

if __name__ == "__main__":
    if sys.platform == r'win32':
        results_dir = os.path.join(r'D:\\','workspace','cstmod','test_data','Simple_Cosim',
                                    'Simple_Cosim_4','Export')
    if sys.platform == r'linux':
        results_dir = os.path.join('/mnt','Data','workspace','cstmod',
                                   'test_data', 'Simple_Cosim')
    f0 = 63.65
    main(results_dir, 'AC*', f0)
    plot_fields('combined_fields_AC2.mat')