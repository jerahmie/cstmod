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
from tkinter import Tk
from tkinter.filedialog import askdirectory

from cstmod.field_reader import FieldReaderCST2019, GenericDataNArray

from cstmod.vopgen import SARMaskCST2019

def export_vopgen_fields(project_dir, export_dir, normalization, freq0, B0_direction):
    export_3d_dir = os.path.join(project_dir, 'Export','3d')
    if not os.path.exists(vopgen_dir):
        os.mkdir(vopgen_dir)
    efields_fr = FieldReaderCST2019()
    efields_fr.normalization = normalization
    print('e-field normalization: ', efields_fr.normalization)
    print('[DEBUG] Saving',  os.path.join(export_dir, 'efMapArrayN.mat'))
    efields_fr.write_vopgen(freq0, export_3d_dir, 
                            os.path.join(export_dir, 'efMapArrayN.mat'),
                            export_type='e-field', merge_type='AC',
                            rotating_frame=False)
    hfields_fr = FieldReaderCST2019()
    hfields_fr.normalization = normalization
    print('[DEBUG] Saving ', os.path.join(export_dir, 'bfMapArrayN.mat'))
    hfields_fr.write_vopgen(freq0, export_3d_dir,
                            os.path.join(export_dir, 'bfMapArrayN.mat'),
                            export_type='h-field', merge_type='AC',
                            rotating_frame=True, field_direction=B0_direction)
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
    sarmask.sigma_max = 1.5 # (S/m)  Exclude conductors
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

    epsr_clean = np.nan_to_num(normal_dielectric.epsilon_r, copy=True,
                               nan=0.0, posinf=None, neginf=None)
    sigma_clean = np.nan_to_num(normal_dielectric.sigma_eff_from_currents[:,:,:,0],
                                copy=True, nan=0.0, posinf=None, neginf=None)
    
    sarmask = SARMaskCST2019(f0, xdim, ydim, zdim, epsr_clean, sigma_clean)
    # todo: refactor magic numbers to *args
    sarmask.epsr_min = 2.0  
    sarmask.epsr_max = 100
    sarmask.sigma_min = 0.05 # (S/m)
    sarmask.sigma_max = 10.0 # (S/m)  Exclude conductors
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
    freq0 = 447# Frequency of interest, MHz
    nchannels = 16
    generate_mask = True
    normalize_power = None

    #if 'win32' == sys.platform:
    #    base_mount = os.path.join('F:', os.sep)
    #else:
    
    base_mount = os.path.join(r'/export',r'data2',r'jerahmie-data', r'Self_Decoupled_10r5T',
            r'SD3', r'column1')
    project_path = os.path.join(base_mount, r'Self_Decoupled_SD3_10r5t_16tx_Lightbulb_Phantom_1')
    
    #base_mount = os.path.join(r'/export', r'disk4', r'jerahmie-data', r'PTx_Knee_7T')
    #project_path = os.path.join(base_mount, r'Knee_pTx_7T_DB_Siemens_Tom_Leg_Phantom_Flip_Fields_retune_20221106_1')

    #Tk().withdraw()
    #project_path = askdirectory()
    if normalize_power == "Auto":
        accepted_power_file_pattern = os.path.join(project_path, 'Export',
                                               "Power_Excitation (AC*)_Power Accepted.txt")
        print(accepted_power_file_pattern)
        accepted_power_narray = GenericDataNArray()
        accepted_power_narray.load_data_one_d(accepted_power_file_pattern)
        print(accepted_power_narray.nchannels)
        f0, accepted_power_at_freq = accepted_power_narray.nchannel_data_at_value(freq0)
        accepted_power_at_freq = np.abs(accepted_power_at_freq)
        print("accepted power: ", accepted_power_at_freq)
        normalization = [1.0/np.sqrt(power) for power in accepted_power_at_freq]
    elif normalize_power == "Custom":
        normalization = [0.49700988, 0.90923172, 0.52187082, 0.82343631,
                         0.59565747, 0.68619393, 0.62657227, 0.6994412,
                         0.55670951, 0.82025112, 0.56925952, 0.9143282,
                         0.48671153, 0.86331512, 0.46899147, 0.77091553]
    else:
        normalization = [1.0 for i in range(nchannels)]
        
    print(normalization)
    
    vopgen_dir = os.path.join(project_path, 'Export', 'Vopgen')
    export_vopgen_fields(project_path, vopgen_dir, normalization, freq0, b0_direction)
    efMapArrayN_dict = hdf5storage.loadmat(os.path.join(vopgen_dir, 'efMapArrayN.mat'))
    bfMapArrayN_rect_dict = hdf5storage.loadmat(os.path.join(vopgen_dir, 'bfMapArrayN_rect.mat'))
    efMapArrayN = efMapArrayN_dict['efMapArrayN']
    bfMapArrayN_rect = bfMapArrayN_rect_dict['bfMapArrayN']

    # Choose a shim solution for extracting mask and material properties
    # (initially cp-like mode)
    current_density_file = os.path.join(project_path, 'Export','3d', 'current-density (f=' + str(freq0) +') [AC8].h5')
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
