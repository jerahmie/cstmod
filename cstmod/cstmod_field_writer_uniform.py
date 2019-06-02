"""
Field exporter that exports fields on a uniformly-sampled subregion
of the simulation domain.
"""

import numpy as np
import scipy.io as spio
from cstmod import CSTFieldWriter

class CSTFieldWriterUniform(CSTFieldWriter):
    """
    Derives from FieldWriter
    """