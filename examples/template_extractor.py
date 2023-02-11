#!/usr/bin/env python

import os

def extract_results(result_dir, prefix: str, postfix: str, nresults: int) -> list:
    """ 
    Extract the results from a series of files to a list
    Each result file contains a single value
    """
    result = list()
    for i in range(nresults):
        with open(os.path.join(result_dir, prefix + str(i+1) + postfix)) as result_file:
            result.append(float(result_file.read()))
    return result

def result_to_csv(result, filename, labels=["Shim", "Peak SAR10g"]):
    """
    Save the result to a csv file.
    """
    with open(filename, 'w+') as fh:
        fh.write(labels[0] + ', ' + labels[1] + '\n')
        for ind, res in enumerate(result):
            fh.write(str(ind) + ',' + str(res) + '\n')

            


if __name__ == "__main__":
    cst_project_dir = os.path.join(r'/export', r'data2', r'jerahmie-data', r'PTx_Knee_7T',
            r'Knee_pTx_7T_DB_Siemens_Duke_One_Legs_Fields_retune_20230124_2')
    assert os.path.exists(cst_project_dir), "Could not find CST project file: " + cst_project_dir
    export_dir = os.path.join(cst_project_dir, r'Export')
    prefix =  r'General SAR Result (Shim'
    postfix_stimulated = r') 1W Stimulated_10g.txt'
    postfix_accepted= r') 1W Accepted_10g.txt'
    nresults=18
    ex_stimulated = extract_results(export_dir, prefix, postfix_stimulated, nresults)
    print("Results Stimulated: ", ex_stimulated)
    result_to_csv(ex_stimulated, os.path.join(export_dir, 'peak_sar10g_stimulated.csv'), ["Shim", "Peak SAR10g"])
    ex_accepted = extract_results(export_dir, prefix, postfix_accepted, nresults)
    print("Results Accepted:   ", ex_accepted)
    result_to_csv(ex_accepted, os.path.join(export_dir, 'peak_sar10g_accepted.csv'), ["Shim", "Peak SAR10g"])
    print("Ratio accepted/stimulated: ", [ex_accepted[i]/ex_stimulated[i] for i in range(nresults)])
    
