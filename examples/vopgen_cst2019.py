#!/bin/env python
"""Trial vopgen exporter using cst2019 hdf5 exported field files.
"""
import os
import sys
import csv
import h5py
import hdf5storage
import numpy as np
import scipy as sp
from rfutils import xmat
from cstmod.field_reader import FieldReaderCST2019, GenericDataNArray

from cstmod.vopgen import SARMaskCST2019

def export_vopgen_fields(project_dir, export_dir, normalization, freq0):
    export_3d_dir = os.path.join(project_dir, 'Export','3d')
    if not os.path.exists(vopgen_dir):
        os.mkdir(vopgen_dir)
    efields_fr = FieldReaderCST2019()
    efields_fr.normalization = normalization
    print('e-field normalization: ', efields_fr.normalization)
    efields_fr.write_vopgen(freq0, export_3d_dir, 
                            os.path.join(export_dir, 'efMapArrayN.mat'),
                            export_type='e-field', merge_type='AC',
                            rotating_frame=False)
    hfields_fr = FieldReaderCST2019()
    hfields_fr.normalization = normalization
    hfields_fr.write_vopgen(freq0, export_3d_dir,
                            os.path.join(export_dir, 'bfMapArrayN.mat'),
                            export_type='h-field', merge_type='AC',
                            rotating_frame=True)
    hfields_fr.write_vopgen(freq0, export_3d_dir,
                            os.path.join(export_dir, 'bfMapArrayN_rect.mat'),
                            export_type='h-field', merge_type='AC',
                            rotating_frame=False)

def export_vopgen_mask(export_dir, f0, xdim, ydim, zdim, efield_data, hfield_data):
    """Calculate and save vopgen masks.
    """
    normal_dielectric = xmat.NormalDielectric(f0, xdim, ydim, zdim,
                                              efield_data, hfield_data)
    sarmask = SARMaskCST2019(f0, xdim, ydim, zdim,
                             normal_dielectric.epsilon_r,
                             normal_dielectric.sigma_eff
                             )
    sarmask.epsr_min = 2
    sarmask.epsr_max = 100
    sarmask.sigma_min = 0.2 # (S/m)
    sarmask.sigma_max = 1.0 # (S/m)  Exclude conductors
    sarmask.write_sarmask(os.path.join(export_dir, 'sarmask_aligned_raw.mat'))
    mat_property_dict = dict()
    mat_property_dict['epsr'] = normal_dielectric.epsilon_r
    mat_property_dict['sigma_eff'] = normal_dielectric.sigma_eff
    mat_property_dict['XDim'] = xdim
    mat_property_dict['YDim'] = ydim
    mat_property_dict['ZDim'] = zdim
    hdf5storage.savemat(os.path.join(export_dir, 'mat_properties_raw.mat'), mat_property_dict, oned_as='column')

def export_vopgen_mask_from_current_density(export_dir, f0, xdim, ydim, zdim, efield_data, hfield_data, current_density):
    """Calculate vopgen masks from electric fields and current density.
    """
    normal_dielectric = xmat.NormalDielectric(f0, xdim, ydim, zdim,
                                              efield_data, hfield_data,
                                               current_density)
    sarmask = SARMaskCST2019(f0, xdim, ydim, zdim,
                             normal_dielectric.epsilon_r,
                             normal_dielectric.sigma_eff_from_currents[:,:,:,0])
    sarmask.epsr_min = 2
    sarmask.epsr_max = 100
    sarmask.sigma_min = 0.2 # (S/m)
    sarmask.sigma_max = 1.0 # (S/m)  Exclude conductors
    sarmask.write_sarmask(os.path.join(export_dir, 'sarmask_aligned_raw.mat'))
    mat_property_dict = dict()
    mat_property_dict['epsr'] = normal_dielectric.epsilon_r
    mat_property_dict['sigma_eff'] = normal_dielectric.sigma_eff_from_currents
    mat_property_dict['XDim'] = xdim
    mat_property_dict['YDim'] = ydim
    mat_property_dict['ZDim'] = zdim
    hdf5storage.savemat(os.path.join(export_dir, 'mat_properties_raw.mat'), mat_property_dict, oned_as='column')    

def load_current_data(field_data_file):
    """Load current density data."""
    with h5py.File(field_data_file, 'r') as dataj:
        jxre = np.transpose(dataj['Conduction Current Density']['x']['re'], (2, 1, 0))
        jxim = np.transpose(dataj['Conduction Current Density']['x']['im'], (2, 1, 0))
        jyre = np.transpose(dataj['Conduction Current Density']['y']['re'], (2, 1, 0))
        jyim = np.transpose(dataj['Conduction Current Density']['y']['im'], (2, 1, 0))
        jzre = np.transpose(dataj['Conduction Current Density']['z']['re'], (2, 1, 0))
        jzim = np.transpose(dataj['Conduction Current Density']['z']['im'], (2, 1, 0))
    jfield_data = np.zeros((np.shape(jxre)[0],
                            np.shape(jxre)[1],
                            np.shape(jxre)[2], 3),
                            dtype = np.complex128)
    jfield_data[:,:,:,0] = jxre + 1.0j*jxim
    jfield_data[:,:,:,1] = jyre + 1.0j*jyim
    jfield_data[:,:,:,2] = jzre + 1.0j*jzim

    return jfield_data

if "__main__" == __name__:
    freq0 = 64  # Frequency of interest, MHz
    nchannels = 1
    generate_mask = True

    if sys.platform == 'win32':
        base_mount = os.path.join(r'D:', os.sep, r'CST_Projects', r'Garwood', r'Loop_1r5T_64MHz')
    elif sys.platform == 'linux':
        base_mount = os.path.join('/mnt', 'Data', 'Temp_CST')
    
    project_path = os.path.join(base_mount, 'Loop_1r5T_64MHz')

    accepted_power_file_pattern = os.path.join(project_path, 'Export',
                                               'Power_Excitation*_Power Accepted (DS).txt')
    #accepted_power_file_pattern = os.path.join(project_path,'Export','Power','Excitation[AC]',)

    accepted_power_narray = GenericDataNArray()
    accepted_power_narray.load_data_one_d(accepted_power_file_pattern)
    f0, accepted_power_at_freq = accepted_power_narray.nchannel_data_at_value(freq0)
    accepted_power_at_freq = np.abs(accepted_power_at_freq)
    print("accepted power: ", accepted_power_at_freq)
    #normalization = [1.0/np.sqrt(power) for power in accepted_power_at_freq]
    normalization = [1.0 for i in range(nchannels)]
    print(normalization)
    
    vopgen_dir = os.path.join(project_path, 'Export', '3d', 'Vopgen2')
    if not os.path.exists(vopgen_dir):
        os.mkdir(vopgen_dir)

    export_vopgen_fields(project_path, vopgen_dir, normalization, freq0)
    efMapArrayN_dict = hdf5storage.loadmat(os.path.join(vopgen_dir, 'efMapArrayN.mat'))
    bfMapArrayN_rect_dict = hdf5storage.loadmat(os.path.join(vopgen_dir, 'bfMapArrayN_rect.mat'))
    efMapArrayN = efMapArrayN_dict['efMapArrayN']
    bfMapArrayN_rect = bfMapArrayN_rect_dict['bfMapArrayN']

    # Choose a shim solution for extracting mask and material properties
    # (initially cp-like mode)
    current_density_file = os.path.join(project_path, 'Export','3d', 'current (f=447) [AC1].h5')
    #if 0:
    if generate_mask:
        if os.path.exists(current_density_file):
            # Calculate mask from current density and E-field
            print('Calculating SAR mask from current density and E-fields.')
            current_density = load_current_data(current_density_file)

            ef_shape = np.shape(efMapArrayN)
            bf_shape = np.shape(bfMapArrayN_rect)
            export_vopgen_mask_from_current_density(vopgen_dir, freq0,
                                                    efMapArrayN_dict['XDim'],
                                                    efMapArrayN_dict['YDim'],
                                                    efMapArrayN_dict['ZDim'],
                                                    efMapArrayN[:,:,:,:,0],
                                                    1.0/sp.constants.mu_0*bfMapArrayN_rect[:,:,:,:,0],
                                                    current_density)
        else:
            # Calculate mask from E- and H- fields
            print('Calculating SAR mask from H- and E-fields.')
            (nx, ny, nz, nfcomp, nchannels) = np.shape(efMapArrayN)
            ef_mask_shim = np.zeros((nx, ny, nz, nfcomp), dtype=np.complex128)
            hf_mask_shim = np.zeros((nx, ny, nz, nfcomp), dtype=np.complex128)

            phases = np.array([2.0*np.pi*ch for ch in range(nchannels)])
            for channel in range(nchannels):
                ef_mask_shim += efMapArrayN[:,:,:,:,channel] * \
                                np.exp(-1.0j*phases[channel])
                hf_mask_shim += (1.0/sp.constants.mu_0)*bfMapArrayN_rect[:,:,:,:,channel] * \
                                np.exp(-1.0j*phases[channel])
    
            export_vopgen_mask(vopgen_dir, freq0,
                               efMapArrayN_dict['XDim'],
                               efMapArrayN_dict['YDim'],
                               efMapArrayN_dict['ZDim'],
                               ef_mask_shim,
                               hf_mask_shim)
