"""
Calculate SAR mask from CST field data.
3D bitmask with dimensions 
export to file: sarmask_aligned.mat
    XDim: XDim x 1
    YDim: YDim x 1
    ZDim: ZDim x 1
    sarmask_new  (XDim, YDim, ZDim)


"""
import numpy as np
import hdf5storage
#from rfutils import xmat
#from cstmod.field_reader import FieldReaderCST2019


class SARMaskCST2019(object):
    """Calculate the SAR mask based on dielectric material properties.
    """
    def __init__(self, frequency0, xdim, ydim, zdim, epsr, sigma):
        self._frequency0 = frequency0 
        self._xdim = xdim
        self._ydim = ydim 
        self._zdim = zdim
        self._sigma = sigma
        self._epsr = epsr
        self._sigma_min = 0.1 
        self._sigma_max = 1.0 # S/m
        self._epsr_min = 2.0
        self._epsr_max = 100.0 # S/m
        self._sarmask = None

    @property
    def sigma_min(self):
        """Minimum conductivity for SAR mask.
        """
        return self._sigma_min

    @sigma_min.setter
    def sigma_min(self, new_sigma_min):
        """Update minimum conductivity for SAR mask.
        """
        if new_sigma_min < self._sigma_max:
            self._sigma_min = new_sigma_min
        else:
            print("sigma_min must be less than sigma_max (", self._sigma_max, ")")

    @property
    def sigma_max(self):
        """Maximum conductivity for SAR mask.
        """
        return self._sigma_max

    @sigma_max.setter
    def sigma_max(self, new_sigma_max):
        """Update maximum conductivity for SAR mask.
        """
        if new_sigma_max > self._sigma_min:
            self._sigma_max = new_sigma_max
        else:
            print("sigma_max must be greater than sigma_min (", self._sigma_min,")")

    @property
    def epsr_min(self):
        """Minimum relative permittivity for SAR mask.
        """
        return self._epsr_min

    @epsr_min.setter
    def epsr_min(self, new_epsr_min):
        """Update minimum epsr for SAR mask.
        """
        if new_epsr_min < self._epsr_max:
            self._epsr_min = new_epsr_min
        else:
            print("epsr_min must be less than epsr_max (", self._epsr_max,")")
    
    @property
    def epsr_max(self):
        """Maximum relative permittivity for SAR mask.
        """
        return self._epsr_max

    @epsr_max.setter
    def epsr_max(self, new_epsr_max):
        """Update maximum epsr for SAR mask.
        """
        if new_epsr_max > self._epsr_min:
            self._epsr_max = new_epsr_max
        else:
            print("epsr_max must be greater than epsr_min(", self._epsr_min,")")

    def _generate_mask(self):
        """Generate mask from desired range of conductivity and permittivity
        """
        sigma_mask_ind = np.where((self._sigma_min < self._sigma) & 
                                  (self._sigma_max > self._sigma))
        sigma_mask = np.zeros((len(self._xdim),
                               len(self._ydim),
                               len(self._zdim)),
                              dtype = np.int)
        sigma_mask[sigma_mask_ind] = 1
        epsr_mask_ind = np.where((self._epsr_min < self._epsr) &
                                 (self._epsr_max > self._epsr))
        epsr_mask = np.zeros((len(self._xdim),
                              len(self._ydim),
                              len(self._zdim)),
                                 dtype = np.int)
        epsr_mask[epsr_mask_ind] = 1
        self._sarmask = np.multiply(epsr_mask, sigma_mask)
        
    @property
    def sarmask(self):
        """Updates and returns sarmask with given permitivitty 
        and conductivity limits.
        """
        self._generate_mask()
        return self._sarmask

    def write_sarmask(self, filename):
        """Save sarmask info to file.
        """
        print('write_sarmask filename: ', filename)
        self._generate_mask()
        export_dict = dict()
        export_dict[u'XDim'] = self._xdim
        export_dict[u'YDim'] = self._ydim
        export_dict[u'ZDim'] = self._zdim
        export_dict[u'sarmask_new'] = self._sarmask
        hdf5storage.savemat(filename, export_dict, oned_as = 'column')

