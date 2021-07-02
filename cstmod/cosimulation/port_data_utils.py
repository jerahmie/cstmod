"""port_data_utils.py
Collection of utilities and helper functions to extract and manage CST
   cosimulation port data.
"""
import os
import re
import numpy as np
import fnmatch
from cstmod.cstutil import find_cst_files, sort_by_trailing_number

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
        result_path: String representing the path conaining probe values.  
    Returns:
        ndarray: port data at frequency dimension complex values of length nports, sorted by port number.
    Raises:
        Exception if the last port number does not equal the number of ports.
            This is an indication that the ports are not number correctly, 
            port data is missing, or ports were not sorted correctly.
    """
    probe_re = re.compile('P[0-9]+.txt')
    unfiltered_files = os.listdir(result_path)
    
    filtered_files = list(filter(None, map(lambda x: os.path.join(result_path, probe_re.match(x).group()) if(probe_re.match(x)) else None, unfiltered_files)))
        
    result_ports = sort_by_trailing_number(filtered_files)

    # quick check for correct port numbers
    last_port_number = int(re.search(r'([\d]+).*$',os.path.basename(result_ports[-1])).group(1))
    
    if len(result_ports) != last_port_number:
        raise Exception("Port numbering is inconsistent and/or port values are missing."+str(result_ports))

    results = np.empty((len(result_ports),2))
    for i, port in enumerate(result_ports):
        results[i] = data_1d_at_frequency(port, frequency)[1:]

    return results[:,0]+1.0j*results[:,1]

def power_from_ports(result_path, frequency, normalization=(1.0/np.sqrt(2.0))):
    """
    Args:
        result_path: String representing the path of the AC combine result to be
                     evaluated.  
    Returns:
        ndarray: real power in port with
    Raises:
    """
    fd_voltages_path = os.path.join(result_path, r'FD Voltages')
    if not os.path.exists(fd_voltages_path):
        raise FileNotFoundError("'FD Voltages/' directory missing.")
    
    fd_currents_path = os.path.join(result_path, r'FD Currents')
    if not os.path.exists(fd_currents_path):
        raise FileNotFoundError("'FD Currents/' directory missing.")

    fd_voltages = data_from_ports(fd_voltages_path, frequency)
    fd_currents = data_from_ports(fd_currents_path, frequency)
    print(fd_voltages)
    print(np.real(np.multiply(fd_voltages, np.conj(fd_currents))))
    normalized_power = normalization*np.real(np.multiply(fd_voltages, np.conj(fd_currents)))

    return normalized_power

