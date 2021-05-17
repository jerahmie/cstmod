"""
Python module with utility and helper functions for cstmod.
"""

import sys

# conditional imports for Windows platform
if sys.platform == 'win32':
    from .cst_reg_info import CSTRegInfo

from .cst_file_utils import pad_square_bracket_string, \
                            find_cst_files, \
                            sort_cst_results_export, \
                            sort_cst_internal_results


