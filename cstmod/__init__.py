"""
    cstmod
    ~~~~~~

    A collection of python utilities for reading and post-processing EM data using
    CSTResultReaderDLL.dll.
 
"""

# import the required submodules
from . import cstutil
from .cstmod_material_type import CSTMaterialType
from .cstmod_boundary_type import CSTBoundaryType
from .cstmod_field_monitor import CSTFieldMonitor, CSTPoint
from .cstmod_result_reader import CSTResultReader
