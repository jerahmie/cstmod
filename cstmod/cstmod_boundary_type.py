"""
CST boundary conditions.
"""

from enum import Enum

class CSTBoundaryType(Enum):
    """Enumeration to encapsulate CST boundary conditions.
    """
    Electric = 10
    Magnetic = 11
    PML = 12
    PML_expanded = 13
    Periodic = 14
    Tangential = 15
    Normal = 16
    No_boundary = 17
    Impedance = 18
    Unitcell = 19
    Open_low_frequency = 21
