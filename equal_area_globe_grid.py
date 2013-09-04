from geography_helper import KILOMETERSOVERMILES, EARTHRADIUSKM
from math import cos, pi, sin, radians, degrees, asin

class EqualAreaGlobeGrid(object):
    """
    All calculations here are provided by the National Snow and Ice Data Center (NSIDC)

    Specifically, this is using the Equal-Area Scalable Earth Grid (EASE) Global Cylindrical Equal-Area Projection,
    described in detail here: http://nsidc.org/data/ease/ease_grid.html.

    The two main formulas are:

        r = r0 + R/C * lambda * cos(pi/6)
        s = s0 - R/C * sin(phi) / cos(pi/6)

        where

              lambda = radians(longitude)
              phi = radians(latitude)
              R = radius of the earth in kilometers
              r0 = map origin column (determined by your starting longitude)
              s0 = map origin row (determined by your starting latitude)
              C = nominal cell size

        (see http://nsidc.org/data/ease/ease_grid.html#GridSection for more information)

    Adaptations were made to generate a grid of any cell size by multiplying
    each equation's RHS by the factor (C / cell_size); a cell size 0.5*C km would double
    the resolution, 0.25*C km would quadruple, etc.

    For an implementation in C, see ftp://sidads.colorado.edu/pub/tools/easegrid/geolocation_tools/ezlhconv.c

    """

    def __init__(self, cell_size_miles):

        self._cell_size_km = cell_size_miles * KILOMETERSOVERMILES

        # scales are made in the formulas relative to 25km
        self._reference_scale_km = 25.067525

        self._grid_scale = self._reference_scale_km / self._cell_size_km

        # r0 defines 0.0 degrees longitude (http://nsidc.org/data/ease/ease_grid.html#GridSection)
        self._r0 = 691.0 * self._grid_scale

        # s0 defines 0.0 degrees latitude (http://nsidc.org/data/ease/ease_grid.html#GridSection)
        self._s0 = 292.5 * self._grid_scale

        # rg provides a scale factor to transform the grid to different cell sizes
        self._rg = EARTHRADIUSKM / self._cell_size_km

        # cache cos(pi/6)
        self._cos_pi_6 = cos(pi/6)

    def get_grid_coordinates(self, longitude, latitude):
        """
        r = r0 + R/C * lambda * cos(pi/6)
        s = s0 - R/C * sin(phi) / cos(pi/6)
        """

        phi = radians(latitude)

        # _ to not overshadow the built-in
        _lambda = radians(longitude)

        r = self._r0 + self._rg * _lambda * self._cos_pi_6
        s = (self._s0 - self._rg * sin(phi) / self._cos_pi_6)

        return r, s

    def get_longitude_latitude(self, r, s):
        """
        We can back-solve the formulas above in get_grid_coordinates
        for the (longitude, latitude) given grid coordinate (r, s)
        """

        y = -1*(s - self._s0)
        phi = asin((y*self._cos_pi_6)/self._rg)

        # _ to not overshadow the built-in
        _lambda = (r - self._r0) / (self._cos_pi_6*self._rg)

        latitude = degrees(phi)
        longitude = degrees(_lambda)

        return longitude, latitude
