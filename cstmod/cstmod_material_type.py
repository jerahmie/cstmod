"""
CST Material Types matrix.
"""
from enum import Enum

class CSTMaterialType(Enum):
    """Enumeration to encapsulate CST material types.
    EPS
    MUE
    KAPPA
    RHO
    """
    EPS = 0
    MUE = 1
    KAPPA = 2
    RHO = 3

