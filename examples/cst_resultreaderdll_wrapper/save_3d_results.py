"""Write the 3D results to a hdf5 file.
"""
import os
import h5py
import matplotlib.pyplot as plt
from cstmod.dllreader import ResultReaderDLL
from cstmod import field_writer

def write_fields(cst_file, output_file, field_3d_name):
    """Write the fields to an hdf5 file.
    """
    field_writer.save_3d_fields_hdf5(cst_file, output_file, field_3d_name)

def plot_results(hdf5_file):
    """Read the hdf5 fields and plot the results.
    """
    pass
    
if __name__ == "__main__":
    print("Saving 3D Results: ")
    cst_file = os.path.join(r'D:\\', r'workspace',r'cstmod',r'test_data',
                            r'Simple_Cosim', r'Simple_Cosim.cst')
    output_file = os.path.join(r'D:\\',r'Temp_CST',r'field3d.hdf5')
    field_3d_name = r'2D/3D Results\H-Field\h-field (f=63.65) [1]'
    write_fields(cst_file, output_file, field_3d_name)
