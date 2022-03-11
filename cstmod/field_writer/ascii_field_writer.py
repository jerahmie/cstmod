"""acsii_field_writer.py
Export 3d field results to acsii CST field format.
"""

import os
import numpy as np
import cstmod.cstutil as cstutil
from cstmod.field_reader import FieldReaderH5
from multiprocessing import Pool


header = ['            x [mm]           y [mm]           z [mm]       HxRe [A/m]       HxIm [A/m]       HyRe [A/m]       HyIm [A/m]       HzRe [A/m]       HzIm [A/m]\n',
         '---------------------------------------------------------------------------------------------------------------------------------------------------------\n']


def write_ascii_fields(fields_dict, fileout):
    """Write the fields in ascii format.
    Args:
        fields_dict - dictionary with fields, xdim, ydim, zdim 
        fileout - output filenmat
    """
    print(header)
    print(fields_dict.keys())
    fields = fields_dict['H-Field']
    with open(fileout, mode='wt') as fh:
        # write the header
        fh.writelines(header)
        for k,z in enumerate(fields_dict['ZDim']):
            for j,y in enumerate(fields_dict['YDim']):
                for i,x in enumerate(fields_dict['XDim']):
                    fh.write(f"{x:17}{y:17}{z:17}{np.real(fields[k,j,i,0]):17.7e}{np.imag(fields[k,j,i,0]):17.7e}{np.real(fields[k,j,i,1]):17.7e}{np.imag(fields[k,j,i,1]):17.7e}{np.real(fields[k,j,i,2]):17.7e}{np.imag(fields[k,j,i,2]):17.7e}\n")
        

def ascii_field_writer(field_name_h5):
    """Program main
    Args:
        export_dir - path to cst exported 3d data directory
        field_name_pattern - string pattern to match for field results
    """
    field_name_txt = os.path.splitext(field_name_h5)[0] + '.txt'
    fr = FieldReaderH5(field_name_h5)
    write_ascii_fields(fr.fields_dict, field_name_txt)

if __name__ == "__main__":
    project_dir = os.path.join(r'D:\\', r'workspace',r'cstmod',r'test_data',
                               r'Simple_Cosim', r'Simple_Cosim_4')
    project_dir = os.path.join(r'F:\\', r'Simple_Cosim_4')
    field_names_h5 = cstutil.find_cst_files(os.path.join(project_dir, r'Export', r'3d',r'h-field*.h5'))
    
    # batch process results
    pool = Pool()
    pool.map(ascii_field_writer, field_names_h5)
