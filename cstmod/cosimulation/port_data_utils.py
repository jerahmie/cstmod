"""port_data_utils.py
Collection of utilities and helper functions to extract and manage CST
   cosimulation port data.
"""

import numpy as np
from cstmod.cstutil import find_cst_files

def data_1d_at_frequency(file_name, frequency):
    """Get the data at frequency.
    Args:
        file_name: String representing the file name of the result value
        frequency: float representing the frequency in appropriate units (defined in simulation)
                    e.g. if the CST simulation units are MHz, then frequency will represent MHz
    Returns:
        list containing [frequency, Real value, Imaginary value] 
    Raises:
        None
    """
    data = np.loadtxt(file_name, delimiter=',')
    freq_ind = np.argmin(np.abs(data[:,0]-frequency))

    return(data[freq_ind])

def data_from_ports(result_path, frequency):
    """
    Args:
        result_path: String representing the path conaining port values.  
    Returns:
        ndarray of dimension complex values of length nports, sorted by port number.
    Raises:
        None
    """
    pass

if __name__ == "__main__":
    if sys.platform == r'win32':
        results_dir = os.path.join(r'D:\\','workspace','cstmod','test_data','Simple_Cosim',
                                    'Simple_Cosim_4','Export')
    if sys.platform == r'linux':
        results_dir = os.path.join('/mnt','Data','workspace','cstmod',
                                   'test_data', 'Simple_Cosim')

    ac_combine_dirs = find_cst_files(os.path.join(results_dir, r'AC*'))
    
    data_1d = data_1d_at_frequency(os.path.join(ac_combine_dirs[0], r'FD Voltages', 'Port1.txt'), 63.65)
