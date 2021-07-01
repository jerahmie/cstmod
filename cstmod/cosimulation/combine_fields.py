"""Cosimulation tools
Implement the combine field step of co-simulation.  This is currently breaking 
in some CST projects.
"""
import sys
import os

import h5py
import numpy as np
from cstmod.cstutil import find_cst_files


if __name__ == "__main__":
    if sys.platform == r'win32':
        results_dir = os.path.join(r'D:\\','workspace','cstmod','test_data','Simple_Cosim',
                                    'Simple_Cosim_4','Export')
    if sys.platform == r'linux':
        results_dir = os.path.join('/mnt','Data','workspace','cstmod',
                                   'test_data', 'Simple_Cosim')

    ac_combine_dirs = find_cst_files(os.path.join(results_dir, r'AC*'))
    
    data_1d = data_1d_at_frequency(os.path.join(ac_combine_dirs[0], r'FD Voltages', 'Port1.txt'), 63.65)
