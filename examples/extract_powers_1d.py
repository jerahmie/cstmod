#!/usr/bin/env python
"""
extract_powers_1d.py

extract the per-port powers from exported 1d simulation results
"""

import os
from cstmod.cosimulation import data_1d_at_frequency

if __name__ == "__main__":
    freq0 = 297
    project_path = os.path.join(r'/export', r'data2', r'jerahmie-data', r'PTx_Knee_7T', 
            r'Knee_pTx_7T_DB_Siemens_Duke_One_Legs_Fields_retune_20230124_2')
    assert os.path.exists(project_path), "Could not find project path"
    power1d_path = os.path.join(project_path, r'Export', r'1d', r'Power')
    assert os.path.exists(power1d_path)
    freq, power_re, power_im = data_1d_at_frequency(os.path.join(power1d_path, r'Excitation [AC1]', r'Power Accepted.txt'),freq0)
    print(str(float(freq)), str(float(power_re)))
    
