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
    conductivity =  np.abs(np.divide(conduction_currents,e_fields))
    mm = MaterialMapper(materials)
    kappa, eps, rho = mm.map_materials(conductivity)
    return kappa, eps, rho


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    if sys.platform == 'linux':
        data_path = os.path.join(r'/mnt',r'Data',r'Temp_CST',r'KU_Ten_32_FDA_21Jul2021_4_6')
    elif sys.platform == 'win32':
        data_path = os.path.join(r'D:', os.path.sep, r'Temp_CST', r'KU_Ten_32_FDA_21Jul2021_4_6')
    else:
        print("Unknown system: ", sys.platform)
        sys.exit()
    
    materials_file = os.path.join(data_path, r'Duke_34y_V5_2mm_0_Duke_34y_V5_2mm.vmat')
    conduction_current_file = os.path.join(data_path, r'current (f=447) [AC1].h5')
    efield_file = os.path.join(data_path, r'e-field (f=447) [AC1].h5')
    mask_file = os.path.join(data_path, )
    conduction_currents = ResultReader3D(conduction_current_file, 'current').fields3d

    rr3d_efields = ResultReader3D(efield_file, 'e-field')
    efields = rr3d_efields.fields3d
    xdim = rr3d_efields.xdim
    ydim = rr3d_efields.ydim
    zdim = rr3d_efields.zdim
    fields_dim = np.shape(efields)

    kappa, eps, rho = map_materials(materials_file, efields, conduction_currents)
    
    propmap_dict = dict()
    propmap_dict['XDim'] = xdim
    propmap_dict['YDim'] = ydim
    propmap_dict['ZDim'] = zdim
    propmap_dict['condMap'] = kappa
    propmap_dict['mdenMap'] = rho
    spio.savemat('propmap.mat', propmap_dict, oned_as='column')

    sarmask_dict = dict()
    sarmask_dict['XDim'] = xdim
    sarmask_dict['YDim'] = ydim
    sarmask_dict['ZDim'] = zdim
    sarmask = np.zeros((len(xdim), len(ydim), len(zdim)), dtype=np.int)
    sarmask_ind = np.where((kappa[:,:,:,0] > 0.01) & (kappa[:,:,:,0] < 10.0))
    sarmask[sarmask_ind] = 1
    sarmask_dict['sarmask_new'] = sarmask
    spio.savemat('sarmask_aligned.mat', sarmask_dict, oned_as='column')

    massdensity_dict = dict()
    massdensity_dict['XDim'] = xdim
    massdensity_dict['YDim'] = ydim
    massdensity_dict['ZDim'] = zdim
    massdensity_dict['mden3D'] = rho
    massdensity_dict['mden3Dm'] = np.multiply(rho, mask)
    spio.savemat('massdensityMap3D.mat', massdensity_dict, oned_as='column')
    
