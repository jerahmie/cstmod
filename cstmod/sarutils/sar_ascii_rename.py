#!/usr/bin/env python
import sys
import glob
import os
import re

def files_sorted(input_glob: str) -> list:
    """ Return a list of sorted files that match input pattern.
    """
    pass

def extract_mnq(input_name: str) -> (int, int, str):
    """ Given an input name, extract the (M, N) of the excitation and quadrature indicator
    
    arguments:
    input_name: str  - A string filename that represents SAR file with the
                        default export file name: "SAR (f=FREQ) [ACM_N(Q)] (SARMASS).txt"
                        FREQ is the frequency in simulation units
                        Q is optional Quadrature designation.
                        ex: "SAR (f=447) [AC1_2Q] (10g).txt"

    returns: (int, int, str) - Returns extracted quantities: 
                                (m, n, '')  for non-quadrature 
                                (m, n, 'Q')  for quadrature 
    """

    # On-diagonal pattern
    sarmmre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)\].*.txt")
    sarmm_match = sarmmre.match(input_name)
    if sarmm_match:
        m = int(sarmm_match[1])
        return (m, m, '')

    # off-diagonal pattern
    sarmnre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)_([0-9]+)([Q]?)\].*.txt")
    sarmn_match = sarmnre.match(input_name)
    if sarmn_match:
        m = int(sarmn_match[1])
        n = int(sarmn_match[2])
        Q = sarmn_match[3]
        return (m, n, 'Q' if Q else '')

    # no match found
    return None


def new_sar_name(input_name: str) -> str:
    """ Rename the input file name to match the expected output file name.
    """
    sar_dirname = os.path.dirname(input_name)
    sar_basename = os.path.basename(input_name)
    (m,n,q) = extract_mnq(sar_basename)
    if q == '':
        return os.path.join(sar_dirname, "SAR_Q" + str(m) + str(n) + ".txt")
    elif q == 'Q':
        return os.path.join(sar_dirname, "SAR_Q" + str(m) + str(n) + "j.txt")
    else:
        return None

def rename_sar(sar_file_directory: str) -> None:
    """Return list of files

    """
    sarmmre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)\].*.txt")
    sarmnre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)_([0-9]+)\].*.txt")
    sarmnqre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)_([0-9]+)Q\].*.txt")
    sar_mm = []
    sar_mn = []
    sar_mnq = []
    for file in os.listdir(sar_file_directory):
            if sarmmre.match(file):
                sar_mm.append(os.path.join(sar_file_directory, file))
            elif sarmnre.match(file):
                sar_mn.append(os.path.join(sar_file_directory, file))
            elif sarmnqre.match(file):
                sar_mnq.append(os.path.join(sar_file_directory, file))
            else:
                pass
    for (src, dst) in  zip(sar_mm, map(new_sar_name, sar_mm)):
        os.rename(src, dst)

    for (src, dst) in zip(sar_mn, map(new_sar_name, sar_mn)):
        os.rename(src, dst)
    
    for (src, dst) in zip(sar_mnq, map(new_sar_name, sar_mnq)):
        os.rename(src, dst)

if __name__ == "__main__":
    sar_dir = os.path.join("/home", "whitney2-raid1", "jerahmie", "workspace",
                           "coil_array_eval", "Test_Data", "Q_matrix")
    rename_sar(sar_dir)