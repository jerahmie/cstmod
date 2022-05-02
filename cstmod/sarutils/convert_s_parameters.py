#!/usr/bin/env python
import os
import numpy as np
import skrf
import hdf5storage


def convert_s_parameters(ntwk, f0=447e6):
    """Export S-parameters from Network
    """
    nn = np.shape(ntwk.s)[1]
    print(nn)
    freq = ntwk.f
    f0_ind = np.argmin(np.abs(freq - f0))
    s_at_freq = np.zeros((nn, nn), dtype=complex)
    for i in range(nn):
        for j in range(nn):
            s_at_freq[i,j] = ntwk.s[f0_ind, i,j]
    smatrix_dict = dict()
    smatrix_dict['Smatrix'] = s_at_freq
    hdf5storage.savemat('Smatrix.mat', smatrix_dict)
    

if __name__ == "__main__":
    tstone_file = os.path.join("/export", "scratch1",
                               "Self_Decoupled_10r5t_16tx_64Rx_Duke_Fields_CST2020_3_1",
                               "Export", "3d","Self_Decoupled_10r5t_16tx_64Rx_Duke_Fields_CST2020_3_1.s16p")
    print(os.path.exists(tstone_file))
    ntwk = skrf.Network(tstone_file)
    convert_s_parameters(ntwk)
