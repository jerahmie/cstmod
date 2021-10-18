"""resultreaderdll.py
   Use the CST result reader dll to load and save field and mesh data.
"""

import sys
import ctypes

if sys.platform == "win32":
    from cstmod.cstutil import CSTRegInfo
else:
    sys.exit("ResultReaderDLL is only compatible with Windows.")


class ResultReaderDLL:
    """Python interface to ResultReaderDLL dynamic library.
    """
    def __init__(self):
        self._readerdll = ctypes.WinDLL()
