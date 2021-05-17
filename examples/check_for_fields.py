#!/usr/bin/env python
"""Scan Results folder for fields files and look for anomalies.
"""

import os
import sys
import re
from cstmod.cstutil import *

def usage():
    """Print a usage message and exit.
    """


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
    cst_internal_results_sorted = sort_cst_internal_results([os.path.basename(result) for result in cst_internal_results])
    nresults = len(cst_internal_results)
    result_dirname = os.path.dirname(cst_internal_results[0])
    result_name_slices = re.match(r'^([a-zA-Z0-9\(\)\-=. ]*_)([0-9]*)(,[0-9]*.)(m3d|m3t)$', os.path.basename(cst_internal_results_sorted[-1])).groups()
    max_result = int(result_name_slices[1])
    missing_results = []
    
    if max_result == len(cst_internal_results_sorted):
        for result in range(1,max_result+1):
            check_file = os.path.join(result_dirname, result_name_slices[0] + str(result) + result_name_slices[2] + result_name_slices[3])
            if check_file in cst_internal_results_sorted:
                missing_results.append(check_file)
    return missing_results
 
if __name__ == "__main__":
    cst_dir = sys.argv[1]
    results_pattern = sys.argv[2]
    print('cst_dir: ', cst_dir)
    print('results_pattern: ', results_pattern)
    missing_results = check_for_fields(cst_dir, results_pattern)
    print("Missing results: ", missing_results)