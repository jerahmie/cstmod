#!/usr/bin/env python
"""Scan Results folder for fields files and look for anomalies.
"""

import os
import re
from cstmod.cstutil import *

def check_for_fields(results_dir, results_pattern):
    """Return a sorted list of files in the CST Results directory
    Args:
        results_dir:      Path the CST Results directory
        results_pattern:  Pattern to match

    Returns:
        list: Names of results matching results_pattern, sorted by simulated port number

    Raises:
    """
    cst_internal_results = find_cst_files(os.path.join(results_dir, results_pattern))
    cst_internal_results_sorted = sort_cst_internal_results(cst_internal_results)
    nresults = len(cst_internal_results)
    result_dirname = os.path.dirname(cst_internal_results[0])
    result_name_slices = re.match(r'^([a-zA-Z0-9\(\)\-=. ]*_)([0-9]*)(,[0-9]*.)(m3d|m3t)$', os.path.basename(cst_internal_results_sorted[-1])).groups()
    max_result = int(result_name_slices[1])
    missing_results = []
    
    if max_result == len(cst_internal_results_sorted):
        for result in range(1,max_result+1):
            check_file = os.path.join(result_dirname, result_name_slices[0] + str(result) + result_name_slices[2] + result_name_slices[3])
            if check_file not in cst_internal_results_sorted:
                missing_result.append(check_file)
    return missing_results
 
if __name__ == "__main__":
    cst_dir = os.path.join(r'D:\\', 'Temp_CST', 'KU_Ten_128_Rx_v2_test4_2','Result')
    results_pattern = 'e-field (f=447)*.m3d'
    missing_results = check_for_fields(cst_dir, 'e-field (f=447)*.m3d')
    print("Missing results: ", missing_results)