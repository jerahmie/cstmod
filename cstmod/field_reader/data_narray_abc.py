"""Class to manage a collection of exported 1D data from CST 2019.b
"""

from abc import ABC, abstractmethod, abstractproperty, ABCMeta

class DataNArrayABC(ABC):
    """Abstract base class to represent a collection of 1-D x N-Channel data.
    """
    @abstractmethod
    def load_data_one_d(self, filename_pattern):
        """Construct the data array from files with given filename
        regular expression.
        """
        pass

    @abstractmethod
    def nchannel_data_at_val(self, val0, eval_type):
        """Returns the nchannels of data at the value of interest.
        Args:
            val0      (float): value of interest that is exported.
            eval_type (str)  : evaluation type ('nearest_neighbor', 'linear', etc.)

        Returns:
            data_at_val (array): Returns n-channels of data at val0. 
        """

    @abstractproperty
    def data_shape(self):
        """Return the overall shape of the 1-d by n-channel data
        """
        pass

    @abstractproperty
    def data_length(self):
        """Returns the dimension of 1-d data.
        """
        pass

    @abstractproperty
    def nchannels(self):
        """Returns the number of channels in the 1-d by n-channel array.
        """
        pass
