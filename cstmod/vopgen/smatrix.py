"""smatrix.py
Create a N-by-N matrix of complex S-parameter values extracted from a 
touchstone file.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import hdf5storage

try:
    import skrf as rf
except(ModuleNotFoundError) as err:
    print("This module uses Scikit-RF.  Please install scikit-rf with pip or otherwise.")
    raise(err)

def network_at_frequency(freq0 :float , network: rf.Network) -> rf.Network:
    """ Reduce network to single frequency.
    Args:
        freq0: single frequency of output network (Hz).
        network: rf network 
    Returns:
        rf network
    Raises:
        None
    """
    #net_temp = network['447Mhz']
    f0_ind = np.argmin(np.abs(network.f[:]-freq0))
    print(network.f[f0_ind])
    #print(np.shape(net_temp))
    #np.shape(netwrk2)
    return rf.Network(frequency=freq0, s=network.s[f0_ind,:,:])
    return None

def write_mat(filename: str, network: rf.Network)-> None: 
    """ Save rf network as rf file.
    Args: 
        network: rf network for single frequency.
        filename: 
    Returns:
        None
    Raises:
        None
    """
    network_dict = dict()
    network_dict['Smatrix'] = network.s[0,:,:]
    hdf5storage.savemat(filename, network_dict)

def plot_mat(smat: np.ndarray) -> plt.axes:
    """
    Plot the single-frequency s-parameter map
    Args:
        smat: smatrix, NxN smatrix at single frequency
    Returns:
        
    """
    to_decibels = lambda a: 20.0*np.log10(a)
    plt.imshow(to_decibels(np.abs(smat)), vmin=-30, vmax=0)
    plt.colorbar()
    return plt.gca()

if __name__ == "__main__":
    ts_file = os.path.join(r'E:', os.path.sep, r'CST_Field_Post', r'KU_Ten_32_FDA_21Jul2021_4_6.s16p')
    smat_file = os.path.join(r'E:', os.path.sep, r'CST_Field_Post', r'Smatrix.mat')
    netwk1 = rf.Network(ts_file)
    netwk2 = network_at_frequency(447.0e6, netwk1)
    write_mat(smat_file, netwk2)
    #plot_mat(netwk2.s[0,:,:])
    #plt.show()
    print("Done.")

