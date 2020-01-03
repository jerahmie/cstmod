"""
EM field readers for various EM simulation tools.
"""

from abc import ABC, abstractmethod, abstractproperty, ABCMeta

class FieldReaderABC(ABC):
    """Field Reader abstract base class. EM fields calculated
    by a generic EM solver must be read and converted into a 
    format that can be utilized to extract material properties.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def _read_fields(self, file_name):
        """
        Reads E, B field values from a file on disk.
        """
        pass

    @abstractmethod
    def write_vopgen(self, file_name):
        """Create vopgen output files for e-field and b-field, masks, etc.
        Args:
            output_dir: Output directory.  Default is export directory within
                        the source directory.
        """
        pass

    #@abstractproperty
    #def ex(self):
    #    return self._ex

    #@abstractproperty
    #def ey(self):
    #    return self._ey

    #@abstractproperty
    #def ez(self):
    #    return self._ez

    #@abstractproperty
    #def hx(self):
    #    return self._bx

    #@abstractproperty
    #def hy(self):
    #    return self._by

    #@abstractproperty
    #def hz(self):
    #    return self._bz


