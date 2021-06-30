""" write_3dfields.py
Helper functions to save simulation data.
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from cstmod.dllreader import ResultReaderDLL

try:
    import h5py
except ImportError as err:
    print("Please install h5py to use this module.")
    raise(err)

def save_3d_fields_hdf5(cst_project_file, output_file, field_data):
    """save the field data to an hdf5 file.
    """
    with ResultReaderDLL(cst_project_file, '2020') as results:
        field3d = results._get_3d_hex_result(field_data, 0)
        (xdim, ydim, zdim) = results._get_hex_mesh()
    field_len = len(xdim)*len(ydim)*len(zdim)
    with h5py.File(output_file, 'w') as f:
        comp_type = np.dtype([ ('x', np.dtype([ ('re', np.float32), ('im', np.float32) ]) ),
                               ('y', np.dtype([ ('re', np.float32), ('im', np.float32) ]) ),
                               ('z', np.dtype([ ('re', np.float32), ('im', np.float32) ]) ) ])
        field_group = f.create_dataset('H-Field', (len(zdim),len(ydim),len(xdim)),  dtype=comp_type)
        field3d_xre = np.reshape(field3d_xre,(len(zdim), len(ydim), len(xdim)))
        field3d_xim = np.zeros((len(zdim), len(ydim), len(xdim)), dtype=np.float32)
        field3d_yre = np.zeros((len(zdim), len(ydim), len(xdim)), dtype=np.float32)
        field3d_yim = np.zeros((len(zdim), len(ydim), len(xdim)), dtype=np.float32)
        field3d_zre = np.zeros((len(zdim), len(ydim), len(xdim)), dtype=np.float32)
        field3d_zim = np.zeros((len(zdim), len(ydim), len(xdim)), dtype=np.float32)
        #field3d_yre = np.reshape(field3d[1::6],(len(xdim), len(ydim), len(zdim)))
        #field3d_zre = np.reshape(field3d[2::6],(len(xdim), len(ydim), len(zdim)))
        #field3d_xim = np.reshape(field3d[3::6],(len(xdim), len(ydim), len(zdim)))
        #field3d_yim = np.reshape(field3d[4::6],(len(xdim), len(ydim), len(zdim)))
        #field3d_zim = np.reshape(field3d[5::6],(len(xdim), len(ydim), len(zdim)))
        temp_fields =  np.empty((len(zdim), len(ydim), len(xdim)), dtype=comp_type)
        
        for ix in range(len(xdim)):
            for jy in range(len(ydim)):
                for kz in range(len(zdim)):
                    temp_fields[kz,jy,ix] = ((field3d_xre[kz,jy,ix], field3d_xim[kz,jy,ix]),
                                             (field3d_yre[kz,jy,ix], field3d_yim[kz,jy,ix]),
                                             (field3d_zre[kz,jy,ix], field3d_zim[kz,jy,ix]))
        field_group[...] = temp_fields
        field_group.attrs['type'] = 6
        field_group.attrs['unit'] = 'A/m'.encode()
        xgroup = f.create_dataset('Mesh line x', data=xdim)
        xgroup.attrs['type']=2
        xgroup.attrs['unit']='mm'.encode()
        ygroup = f.create_dataset('Mesh line y', data=ydim)
        ygroup.attrs['type']=2
        ygroup.attrs['unit']='mm'
        zgroup = f.create_dataset('Mesh line z', data=zdim)
        zgroup.attrs['type']=2
        zgroup.attrs['unit']='mm'

def write_fields(cst_file, output_file, field_3d_name):
    """Write the fields to an hdf5 file.
    """
    save_3d_fields_hdf5(cst_file, output_file, field_3d_name)

if __name__ == "__main__":
    print("Saving 3D Results: ")
    cst_file = os.path.join(r'D:\\', r'workspace',r'cstmod',r'test_data',
                            r'Simple_Cosim', r'Simple_Cosim.cst')
    output_file = os.path.join(r'D:\\',r'Temp_CST',r'field3d.hdf5')
    field_3d_name = r'2D/3D Results\H-Field\h-field (f=63.65) [1]'
    write_fields(cst_file, output_file, field_3d_name)