"""Trial vopgen exporter using cst2019 hdf5 exported field files.
"""
import os
import csv
import h5py
import hdf5storage
import numpy as np
import scipy as sp
from rfutils import xmat
import cstmod.field_reader as field_reader
from cstmod.vopgen import SARMaskCST2019

def export_vopgen_fields(project_dir, export_dir, normalization):
    print(project_dir)
    print('exits? ', os.path.exists(project_dir))
    export_3d_dir = os.path.join(project_dir, 'Export','3d')
    
    if not os.path.exists(vopgen_dir):
        os.mkdir(vopgen_dir)
    efields_fr = field_reader.FieldReaderCST2019()
    efields_fr.normalization = normalization
    print('e-field normalization: ', efields_fr.normalization)
    efields_fr.write_vopgen('447', export_3d_dir, 
                            os.path.join(export_dir, 'efMapArrayN.mat'),
                            export_type='e-field', merge_type='AC',
                            rotating_frame=False)
    hfields_fr = field_reader.FieldReaderCST2019()
    hfields_fr.normalization = normalization
    hfields_fr.write_vopgen('447', export_3d_dir,
                            os.path.join(export_dir, 'bfMapArrayN.mat'),
                            export_type='h-field', merge_type='AC',
                            rotating_frame=True)
    hfields_fr.write_vopgen('447', export_3d_dir,
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
                             normal_dielectric.sigma_eff)
    sarmask.epsr_min = 2
    sarmask.epsr_max = 100
    sarmask.sigma_min = 0.2 # (S/m)
    sarmask.sigma_max = 1.0 # (S/m)  Exclude conductors
    sarmask.write_sarmask(os.path.join(export_dir, 'sarmask_aligned.mat'))
    

if "__main__" == __name__:
    print("vopgen cst2019 tests...")
    project_path = os.path.join('D:', os.sep, 'CST_Projects', \
        'KU_ten_32_Tx_MRT_23Jul2019')
    accepted_power_file = os.path.join('D:', os.sep, 'workspace', 'cstmod', 
                                        'accepted_powers.csv')
    with open(accepted_power_file, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            accepted_power = [float(powerval) for powerval in row]
    print("accepted power: ", accepted_power)
    normalization = [1.0/np.sqrt(power) for power in accepted_power]
    print(normalization)
    
    vopgen_dir = os.path.join(project_path, '..', 'Vopgen')
    #export_vopgen_fields(project_path, vopgen_dir, normalization)
    efMapArrayN = hdf5storage.loadmat(os.path.join(vopgen_dir, 'efMapArrayN.mat'))
    bfMapArrayN_rect = hdf5storage.loadmat(os.path.join(vopgen_dir, 'bfMapArrayN_rect.mat'))
    
    ef_cp = np.zeros((efMapArrayN['XDim'], 
                      efMapArrayN['YDim'],
                      efMapArrayN['ZDim']),
                     dtype=np.complex)
    bf_cp = np.zeros((bfMapArrayN_rect['XDim'],
                      bfMapArrayN_rect['YDim'],
                      bfMapArrayN_rect['ZDim']),
                     dtype=np.complex)

    # shim fields.
    
    #export_vopgen_mask(vopgen_dir, 447.0e6,
    #                   efMapArrayN['XDim'],
    #                   efMapArrayN['YDim'],
    #                   efMapArrayN['ZDim'],
    #                   ef_cp, bf_cp)
