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
    conduction_currents = ResultReader3D(conduction_current_file, 'current').fields3d

    rr3d_efields = ResultReader3D(efield_file, 'e-field')
    efields = rr3d_efields.fields3d
    xdim = rr3d_efields.xdim
    ydim = rr3d_efields.ydim
    zdim = rr3d_efields.zdim
    fields_dim = np.shape(efields)

    kappa, eps, rho = map_materials(materials_file, efields, conduction_currents)
    kappa_dict = dict()
    #kappa_dict['XDim'] = xdim
    #kappa_dict['YDim'] = ydim
    #kappa_dict['ZDim'] = zdim
    #kappa_dict['kappa'] =kappa
    #hdf5storage.savemat('kappa.mat', kappa_dict)
    #eps_dict = dict()
    #eps_dict['XDim'] = xdim
    #eps_dict['YDim'] = ydim
    #eps_dict['ZDim'] = zdim
    #eps_dict['eps'] = eps
    #hdf5storage.savemat('eps.mat', eps_dict)
    #rho_dict = dict()
    #rho_dict['XDim'] = xdim
    
    #rho_dict['rho'] = rho
    #hdf5storage.savemat('rho.mat', )
    propmap_dict = dict()
    propmap_dict['XDim'] = xdim
    propmap_dict['YDim'] = ydim
    propmap_dict['ZDim'] = zdim
    propmap_dict['condMap'] = kappa
    propmap_dict['mdenMap'] = rho

    plt.pcolormesh(kappa[:,:,200,0])
    plt.colorbar()
    plt.show()