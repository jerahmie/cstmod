"""vopgen_from_mask.py
   A quick and dirty script to create vopgen massdensityMap3D.mat 
   and propmap.mat from sarmake_aligned.mat in uniform phantom
"""
import os
import hdf5storage
import numpy as np


def write_massdensitymap3d(vopgen_dir, mass_density):
    """Writes massdensityMap3D.mat to vopgen directory
       vopgen_dir: vopgen directory
       mass_density: phantom mass density (g/L)
    """
    print('writing massdensityMap3D.mat...')
    sarmask_file = os.path.join(vopgen_dir, 'sarmask_aligned.mat')
    if not os.path.exists(sarmask_file):
        print('Could not find sarmask_file.')
        print(sarmask_file)
        return 
    
    sarmask_dict = hdf5storage.loadmat(sarmask_file)
    xdim = sarmask_dict['XDim']
    ydim = sarmask_dict['YDim']
    zdim = sarmask_dict['ZDim']
    sarmask_new = sarmask_dict['sarmask_new']
    nx = len(xdim)
    ny = len(ydim)
    nz = len(zdim)
    mden3D = np.multiply(mass_density, sarmask_new)
    mden3Dm = np.multiply(mass_density, sarmask_new)
    
    massdensity_dict = dict()
    massdensity_dict['XDim'] = xdim
    massdensity_dict['YDim'] = ydim
    massdensity_dict['ZDim'] = zdim
    massdensity_dict['mden3D'] = mden3D
    massdensity_dict['mden3Dm'] = mden3Dm
    hdf5storage.savemat(os.path.join(vopgen_dir, 'massdensityMap3D.mat'),
                        massdensity_dict,
                        oned_as='column')

    
    print('Done.')

def write_propmat(vopgen_dir, mass_density, conductivity):
    """Writes propmap.mat to vopgen directory
       vopgen_dir: vopgen directory
       mass_density: phantom mass density (g/L)
       conductivity: phantom electrical conductivity at frequency (S/m)
    """
    print('writing propmap.mat...')
    sarmask_file = os.path.join(vopgen_dir, 'sarmask_aligned.mat')
    if not os.path.exists(sarmask_file):
        print('Could not find sarmask_file.')
        print(sarmask_file)
        return 
    
    sarmask_dict = hdf5storage.loadmat(sarmask_file)
    xdim = sarmask_dict['XDim']
    ydim = sarmask_dict['YDim']
    zdim = sarmask_dict['ZDim']
    sarmask_new = sarmask_dict['sarmask_new']
    nx = len(xdim)
    ny = len(ydim)
    nz = len(zdim)

    mdenmap = np.multiply(mass_density, sarmask_new)
    condmap = np.zeros((len(xdim), len(ydim), len(zdim), 3), dtype=np.float)
    condmap1x = np.multiply(conductivity, sarmask_new)
    condmap[:,:,:,0] = condmap1x
    condmap[:,:,:,1] = condmap1x
    condmap[:,:,:,2] = condmap1x

    propmap_dict = dict()
    propmap_dict['XDim'] = xdim
    propmap_dict['YDim'] = ydim
    propmap_dict['ZDim'] = zdim
    propmap_dict['mdenMap'] = mdenmap
    propmap_dict['condMap'] = condmap
    propmap_dict['units'] = 'm'
    hdf5storage.savemat(os.path.join(vopgen_dir, 'propmap.mat'),
                        propmap_dict,
                        oned_as = 'column')

    print('Done.')

if "__main__" == __name__:
    mass_density = 1120.0 # g/L
    conductivity = 0.6958 # S/m
    #vopgen_dir = os.path.join('D:\\', 'CST_Projects','Vopgen')
    vopgen_dir = os.path.join('/home','jerahmie','Data','CST_Projects', 'Vopgen')
    write_massdensitymap3d(vopgen_dir, mass_density)
    write_propmat(vopgen_dir, mass_density, conductivity)
