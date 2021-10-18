"""Unit testing file for cst_file_utils.
    Requires pytest module
"""

import os
import tempfile
from cstmod.cstutil import *
import functools


cstmod_test_data_dir = os.path.normpath(os.path.join(os.path.realpath(__file__),
                                              r'..', r'..', r'test_data'))
cst_hex_mesh_project = os.path.join('D:\\', 'Temp_CST', 'KU_Ten_128_Rx_v2_test4_2')

def test_data_dir_exists():
    assert os.path.exists(cstmod_test_data_dir) == True

def test_pad_brackets():
    """ Test bracket padding for regex processing.
    """
    assert pad_square_bracket_string(r'file_without_brackets.txt') == \
        r'file_without_brackets.txt'
    assert pad_square_bracket_string(r'file_with [1] bracket.txt') == \
        r'file_with [[]1[]] bracket.txt'
    assert pad_square_bracket_string(r'file_with[1]_bracket_and[2].txt') == \
        r'file_with[[]1[]]_bracket_and[[]2[]].txt'


def test_sort_cst_exported_files():
    """ Process the file list matching the file name pattern. 
    """
    h_field_files = [os.path.join(cstmod_test_data_dir, r'h-field (f=447) [AC' + str(i) + r'].h5') for i in range(1,5+1)]
    for i in range(11,13):
        h_field_files.append(os.path.join(cstmod_test_data_dir, r'h-field (f=447) [AC' + str(i) + r'].h5'))
    print("h_field_files: ", h_field_files)
    unsorted_files = find_cst_files(os.path.join(cstmod_test_data_dir, 'h-field*[AC*].h5'))
    assert sort_cst_results_export(unsorted_files, 'AC') == h_field_files

def test_sort_cst_result_files():
    """CST saves em fields in a results folder.  Field results are stored in a
    proprietary format, with formats varying depending on the mesh type.
    """
    cst_internal_results_target = [os.path.join(cst_hex_mesh_project, 'Result',
                                   'e-field (f=447)_' + str(i+1) + ',1.m3d') for i in range(14)]
        
    cst_internal_results_unsorted = find_cst_files(os.path.join(cst_hex_mesh_project, 'Result', 'e-field*.m3d'))
    pretty_print_files(cst_internal_results_unsorted)
    cst_internal_results_sorted = sort_cst_internal_results(cst_internal_results_unsorted)
    pretty_print_files(cst_internal_results_sorted)
    assert  cst_internal_results_sorted == cst_internal_results_target

def pretty_print_files(file_list):
    """print the files in the list of files:
    """
    file_count = 0
    print("Pretty print")
    print("File Number: File Name")
    for file in file_list:
        print(file_count, file)
        file_count += 1

def test_sort_by_trailing_number():
    """Test sort of many files by trailing number
    e.g. /path/to/results/AC* get sorted by trailing number in numerical order
    such that AC1 is followed by AC2 not AC10, etc
    """
    sorted_files = []
    with tempfile.TemporaryDirectory() as tempdir:
        for i in range(15):
            path = os.path.join(tempdir,r'AC'+str(i+1))
            os.mkdir(path)
            sorted_files.append(path)
        
        unsorted_files = [os.path.join(tempdir, ac) for ac in os.listdir(tempdir)]
        assert os.path.exists(os.path.join(tempdir,r'AC1'))
        assert os.path.exists(os.path.join(tempdir,r'AC15'))

        assert functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, sorted_files, sort_by_trailing_number(unsorted_files)),True)
