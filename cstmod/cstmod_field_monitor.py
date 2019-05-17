"""
    CSTFieldMonitor
    ~~~~~~~~~~~~~~~

    A collection of tools to interrogate CST field monitor data and metadata.

"""
import numbers
import xml.etree.ElementTree as ET

class CSTPoint(object):
    """
    Point class. Encapsulates (x, y, z) point attributes.

    Args:
        x (float): x-value of point.
        y (float): y-value of point.
        z (float): z-value of point.
    """
    def __init__(self, x0=0.0, y0=0.0, z0=0.0):
        if isinstance(x0, numbers.Number):
            self._x = x0
        else:
            raise TypeError("x should be of number type, not: " + str(type(x0)))
        
        if isinstance(y0, numbers.Number):
            self._y = y0
        else:
            raise TypeError("y should be of number type, not: " + str(type(y0)))

        if isinstance(z0, numbers.Number):
            self._z = z0
        else:
            raise TypeError("z should be of number type, not: " + str(type(z0)))

    def __eq__(self, other):
        """Determine if two points are equal.
        """
        if isinstance(other, CSTPoint):
            return (self._x == other.x) and (self._y == other.y) and (self._z == other.z)

        return NotImplemented

    @property
    def x(self):
        """
        :float: X-coordinate of point.
        """
        return self._x

    @x.setter
    def x(self, x1):
        if isinstance(x1, numbers.Number):
            self._x = x1
        else:
            raise TypeError("x should be number type, not: " + str(type(x1)))

    
    @property
    def y(self):
        """
        :float: Y-coordinate of point.
        """
        return self._y

    @y.setter
    def y(self, y1):
        if isinstance(y1, numbers.Number):
            self._y = y1
        else:
            raise TypeError("y should be number type, not: " + str(type(y1)))

    @property
    def z(self):
        """
        :float: Z-coordinate of point.
        """
        return self._z

    @z.setter
    def z(self, z1):
        if isinstance(z1, numbers.Number):
            self._z = z1
        else:
            raise TypeError("z should be number type, not: " + str(type(z1)))

    # TODO: implement __eq__ operator

class CSTFieldMonitor(object):
    """
    CST field monitor data and metadata
    """
    def __init__(self, field_monitor_file_name):

        self._simulation_domain_min = CSTPoint(0.0, 0.0, 0.0)
        self._simulation_domain_max = CSTPoint(0.0, 0.0, 0.0)
        self._subvolume_min = CSTPoint(0.0, 0.0, 0.0)
        self._subvolume_max = CSTPoint(0.0, 0.0, 0.0)
        self._field_monitor_file = field_monitor_file_name
        self._field_meta_data = None
        self._parse_field_monitor()

    def _parse_field_monitor(self):
        """Parse the xml data for given field monitor 
        """
        self._field_meta_data = ET.parse(self._field_monitor_file)
        root = self._field_meta_data.getroot()
        
        sim_domain = root.find('SimulationDomain')
        sim_domain_min = [float(i) for i in sim_domain.attrib['min'].split()]
        sim_domain_max = [float(i) for i in sim_domain.attrib['max'].split()]
        self._simulation_domain_min = CSTPoint(sim_domain_min[0],
                                                sim_domain_min[1],
                                                sim_domain_min[2])
        self._simulation_domain_max = CSTPoint(sim_domain_max[0],
                                                sim_domain_max[1],
                                                sim_domain_max[2])
        subvolume = root.find('SubVolume')
        if None != subvolume:
            subvolume_min = [float(i) for i in subvolume.attrib['min_pos'].split()]
            subvolume_max = [float(i) for i in subvolume.attrib['max_pos'].split()]
            self._subvolume_min = CSTPoint(subvolume_min[0],
                                            subvolume_min[1],
                                            subvolume_min[2])
            self._subvolume_max = CSTPoint(subvolume_max[0],
                                            subvolume_max[1],
                                            subvolume_max[2])

    @property
    def simulation_domain_min(self):
        """Point (x,y,z) defining the minimum values of the simulation domain.
        """
        return self._simulation_domain_min

    @property
    def simulation_domain_max(self):
        """Point (x,y,z) defining the maximum values of the simulation domain.
        """
        return self._simulation_domain_max

    @property
    def subvolume_min(self):
        """Point (x,y,z) defining the minimum values of the subvolume of the field monitor.
        """
        return self._subvolume_min
    
    @property
    def subvolume_max(self):
        """Point (x,y,z) defining the maximum values of the subvolume of the field monitor.
        """
        return self._subvolume_max

