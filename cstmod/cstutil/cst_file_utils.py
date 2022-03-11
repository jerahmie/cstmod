"""Helper utilities for dealing with CST file naming schemes.
"""

import os
import sys
import re
if sys.platform == 'win32':
    import fnmatch
elif sys.platform == 'linux':
    import glob
else:
    import glob  # assuming a unix-like system.

def pad_square_bracket_string(string_with_brackets):
    """ Pad the square brackets in a string for pattern matching with square brackets.
    """
    f_right_bracket = string_with_brackets.split('[')
    f_padded_right_bracket = []  # storage of padded string fragments
    for fsub in f_right_bracket:
        temp = fsub.split(']')
        f_padded_right_bracket.append("[]]".join(temp))

    return "[[]".join(f_padded_right_bracket)

def find_cst_files(file_name_pattern):
    """Generate a sorted list of files that matches a provided regular expression.
    Args:
        file_name_pattern: file pattern path to list of files.
    Returns:
        list: list of files matching field pattern
    Raises: 
        Exception: if system is not 'linux' or 'win32', an exception is raised.
    """ 
    if sys.platform == 'win32':
        source_dir = os.path.dirname(file_name_pattern)
        file_base_pattern_pad = os.path.basename(pad_square_bracket_string(file_name_pattern))
        file_list = [os.path.join(source_dir, file) for file in fnmatch.filter(os.listdir(os.path.dirname(file_name_pattern)), file_base_pattern_pad)]

    elif sys.platform == 'linux':
        glob_string = pad_square_bracket_string(file_name_pattern)
        file_list = glob.glob(glob_string)

    else:
        raise Exception("Unable to process files due to unsupported system: ", 
            sys.platform)

    return file_list

def sort_cst_results_export(unsorted_files, sorting_prefix = ""):
    """Sort the exported cst results accorting to the bracketed result type (i.e [1], [AC1])

    Example: unsorted file result from os.listdir:
    unsorted_files = ['h-field (f=447) [AC11].h5' 
                     'h-field (f=447) [AC12].h5' 
                     'h-field (f=447) [AC1].h5'
                     'h-field (f=447) [AC2].h5']

    Sorting by the pattern [AC*] produces the sorted array:
    sorted_files = ['h-field (f=447) [AC1].h5' 
                   'h-field (f=447) [AC2].h5' 
                   'h-field (f=447) [AC11].h5'
                   'h-field (f=447) [AC12].h5']

    Args:
        unsorted_files: unsorted list of filenames
        sorting_prefix: prefix with bracketed results: 
    Returns:
        list of sorted files.
    """
    return sorted(unsorted_files, key=lambda fl: int(re.search(r'\['+ sorting_prefix + r'([\d]+)\]',fl).group(1)))

def sort_cst_internal_results(unsorted_files):
    """CST saves em fields in a results folder.  Feild results are stored in a
    proprietary format, with formats varying depending on the mesh type.
    """
    sorted_files = sorted(unsorted_files, key=lambda fl: int(re.search(r'^[0-9a-zA-Z:\\_\-\(\) =]*_([0-9]*),[0-9]*(.m3d|.m3t|_m3d.rex|_m3d_sct.rex)$',fl).group(1)))
    return sorted_files

def sort_by_trailing_number(unsorted_files):
    """Takes a list of files and sorts by the trailing number.
    Args:
        unsorted_files: list of unsorted file paths
    Returns: 
        list of sorted files
    """
    return sorted(unsorted_files, key=lambda fl: int(re.search(r'([\d]+).*$',os.path.basename(fl)).group(1)))