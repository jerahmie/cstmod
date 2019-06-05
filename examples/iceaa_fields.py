"""Extract fields from CST em simulation and combine for ICEAA 2019
"""
import os

from cstmod import CSTFieldWriterNonUniform, CSTResultReader

def main(cst_project, field_monitor_regex, output_file):
    """Main routine to set up result reader
    """
    print('Processing ', cst_project)
    print('Matching following field monitors: ', field_monitor_regex)
    
    rr = CSTResultReader('2018')
    rr.open_project(cst_project)
    if not os.path.exists(cst_project):
        raise FileNotFoundError
    else:
        print("Found ", cst_project)
    
    
    fw = CSTFieldWriterNonUniform(rr)
    fw.write('test_efield.mat','e-field')
    rr.close_project()
    print("Saving field results to file: ", output_file)

if "__main__" == __name__:
    cst_project = os.path.join("E:\\", "CST_Results", "KU_ten_32_Tx_MRT.cst")
    #cst_project = os.path.join("..","Test_Data","simple_cosim_7T.cst")
    main(cst_project, 'E-field\e-field*[Tran*]', 'e-field.mat')
    #main(cst_project, 'E-field\e-field*[0-9*]', 'e-field.mat')
    
