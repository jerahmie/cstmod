#!/usr/bin/env python
""" cst_map_materials
map materials from cstdata
"""
import os
import sys
import cstmod
import numpy as np
import scipy.io as spio 
import hdf5storage
from rfutils.material_mapper import MaterialMapper
from cstmod.field_reader import ResultReader3D
import cstmod.vopgen

def map_materials(materials, e_fields, conduction_currents):
    """map_materials
    Args:
        materials: embedded list of materials and properties
        e_field:  ndarray of electric fields 
        conduction_currents:  ndarray of induced currents
    Returns:
        ndarray:  3d array of mapped materials
    """
    conductivity_XYZ =  np.abs(np.divide(conduction_currents, e_fields))
    conductivity = (conductivity_XYZ[:,:,:,0] + \
                    conductivity_XYZ[:,:,:,1] + \
                    conductivity_XYZ[:,:,:,2])/3.0
    print("shape conductivity: ", np.shape(conductivity))
    mm = MaterialMapper(materials)

    kappa, eps, rho, materials = mm.map_materials(conductivity)
    return kappa, eps, rho, materials


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    if sys.platform == 'linux':
        #data_path = os.path.join(r'/mnt',r'Data',r'Temp_CST',r'KU_Ten_32_FDA_21Jul2021_4_6')
        data_path = os.path.join(r'/export',r'scratch1',r'Self_Decoupled_10r5t_16tx_64Rx_Duke_Fields_CST2020_3_1')
    elif sys.platform == 'win32':
        data_path = os.path.join(r'D:', os.path.sep, r'Temp_CST', r'KU_Ten_32_FDA_21Jul2021_4_6')
    else:
        print("Unknown system: ", sys.platform)
        sys.exit()
    
    # materials_file = os.path.join(data_path, r'Model', r'3D',
    #                              r'Duke_34y_V5_2mm_1_Duke_34y_V5_2mm.vmat')
    materials_file = 'Duke_34y_V5_2mm_1_Duke_34y_V5_2mm.vmat'
    conduction_current_file = os.path.join(data_path, r'Export', r'3d', r'current-density (f=447) [AC1].h5')
    efield_file = os.path.join(data_path, r'Export', r'3d', r'e-field (f=447) [AC1].h5')
    mask_file = os.path.join(data_path, "Export", "Vopgen", "sarmask_aligned.mat")
    conduction_currents = ResultReader3D(conduction_current_file, 'current').fields3d

    rr3d_efields = ResultReader3D(efield_file, 'e-field')
    efields = rr3d_efields.fields3d
    xdim = rr3d_efields.xdim
    ydim = rr3d_efields.ydim
    zdim = rr3d_efields.zdim
    fields_dim = np.shape(efields)

    sarmask=spio.loadmat(mask_file)['sarmask_new']
    
    kappa, eps, rho, materials = map_materials(materials_file, efields, conduction_currents)

    # vopgen property map
    propmap_dict = dict()
    propmap_dict['XDim'] = xdim
    propmap_dict['YDim'] = ydim
    propmap_dict['ZDim'] = zdim
    mm_shape = np.shape(kappa)
    kappa_XYZ = np.zeros((mm_shape[0],mm_shape[1],mm_shape[2],3))
    kappa_XYZ[:,:,:,0] = kappa
    kappa_XYZ[:,:,:,1] = kappa
    kappa_XYZ[:,:,:,2] = kappa

    rho_XYZ  = np.zeros((mm_shape[0],mm_shape[1],mm_shape[2],3))
    rho_XYZ[:,:,:,0] = rho
    rho_XYZ[:,:,:,1] = rho
    rho_XYZ[:,:,:,2] = rho

    propmap_dict['condMap'] = kappa_XYZ * sarmask[...,np.newaxis]
    propmap_dict['mdenMap'] = rho_XYZ * sarmask[...,np.newaxis]
    spio.savemat('propmap.mat', propmap_dict, oned_as='column')

    # vopgen massdensity map
    massdensity_dict = dict()
    massdensity_dict['XDim'] = xdim
    massdensity_dict['YDim'] = ydim
    massdensity_dict['ZDim'] = zdim
    massdensity_dict['mden3D'] = rho * sarmask
    massdensity_dict['mden3Dm'] = rho * sarmask
    spio.savemat('massdensityMap3D.mat', massdensity_dict, oned_as='column')
    
    # save mapped materials
    np.save('materials.npy', materials)

