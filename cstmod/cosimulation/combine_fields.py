"""Cosimulation tools
Implement the combine field step of co-simulation.  This is currently breaking 
in some CST projects.
"""
import sys
import os
import h5py


if __name__ == "__main__":
    if sys.platform == r'win32':
        results_dir = os.path.join(r'D:\\','workspace','cstmod','test_data','Simple_Cosim','Simple_Cosim_4','Export')
    if sys.platform == r'linux':
        results_dir = os.path.join('/mnt','Data','workspace','cstmod',
                                   'test_data', 'Simple_Cosim')

    print(os.path.exists(results_dir))