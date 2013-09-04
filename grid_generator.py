from geography_helper import convert_arrays_of_geocos_to_kml
from shapely.geometry.multipolygon import MultiPolygon
from equal_area_globe_grid import EqualAreaGlobeGrid
from geography_helper import USABoundsReference
from shapely.geometry.polygon import Polygon
import json

class GridGenerator(object):
    """
    This class subdivides the geographical extent of the United States into an equal area grid.

        Dependencies:

            /geography_helper.py
            /equal_area_globe_grid.py
            /united_states_border.json

        Usage:

            Let X be the desired area in square miles of each equal area cell

            >> GridGenerator(sqrt(X)).run()

        Output:

            /beautiful_grid.kml

    """


    def __init__(self, cell_size_miles):

        # input is desired square of each equal area cell, in miles
        self._cell_size_miles = cell_size_miles

        # ecapsulating longitude/latitude boxes for Mainland, Alaska, Hawaii, Puerto Rico
        self._geo_reference = USABoundsReference().Geographies

        # we'll store each cell's shape array here
        self._shape_arrays = []

        # a calculator that converts grid (row, column) to (longitude, latitude) and vice versa.
        # see class doc-string for citations and more info
        self._proj_calc = EqualAreaGlobeGrid(self._cell_size_miles)


    def run(self):
        """
        Public run method - generates an equal area grid for the United States
        """
        self._load_US_boundary()
        self._create_equal_area_grid()
        self._save_to_kml()


    def _load_US_boundary(self):
        """
        Loads a GEOJson multipolygon created separately by merging the polygons provided here:
            https://developers.google.com/kml/documentation/us_states.kml
        """
        geojson_multipolygon_file = open("united_states_border.json", "r")
        geojson_multipolygon = json.loads(geojson_multipolygon_file.read())
        geojson_multipolygon_file.close()

        # create a shapely multipolygon - this will be used to determine if a generated grid cell lies within the USA
        self._US_boundary = MultiPolygon(geojson_multipolygon["coordinates"], context_type = "geojson")


    def _create_equal_area_grid(self):
        """
        For each region in the USA, calculate all equal area cells that either intersect, or are contained within
        that region. Each cell follows the numbering convention:

            Northwest Corner: (longitude_0, latitude_0)
            Northeast Corner: (longitude_1, latitude_1)
            Southeast Corner: (longitude_2, latitude_2)
            Southwest Corner: (longitude_3, latitude_3)

        """

        # loop over all boxes bounding the separate US geographical regions (Mainland, Alaska, Hawaii, Puerto Rico)
        for region in self._geo_reference:

            # start in the northwest corner of the bounding box
            region_most_west_longitude = self._geo_reference[region]["west"]
            region_most_north_latitude = self._geo_reference[region]["north"]

            # get the starting NSIDC EASE row-column coordinate pair
            self._r_0, self._s_0 = self._proj_calc.get_grid_coordinates(region_most_west_longitude, region_most_north_latitude)

            start_longitude, start_latitude = self._proj_calc.get_longitude_latitude(self._r_0, self._s_0)

            # just renaming to keep the crawl semantically consistent
            latitude_crawl = start_latitude

            j = 0
            # crawl southward
            while latitude_crawl > self._geo_reference[region]["south"]:

                i = 0
                # reset the starting longitude (western-most of the region on the grid)
                longitude_crawl = start_longitude

                # crawl eastward
                while longitude_crawl < self._geo_reference[region]["east"]:

                    # generate a cell, and return the new starting longitude and latitude
                    longitude_crawl, latitude_crawl = self._generate_individual_cell(i, j)

                    i += 1
                j += 1


    def _generate_individual_cell(self, i, j):

        # northwest corner
        longitude_0, latitude_0 = self._proj_calc.get_longitude_latitude(self._r_0 + i, self._s_0 + j)

        # northeast corner
        longitude_1, latitude_1 = self._proj_calc.get_longitude_latitude(self._r_0 + i + 1, self._s_0 + j)

        # southeast corner
        longitude_2, latitude_2 = self._proj_calc.get_longitude_latitude(self._r_0+ i + 1, self._s_0 + j + 1)

        # southwest corner
        longitude_3, latitude_3 = self._proj_calc.get_longitude_latitude(self._r_0 + i, self._s_0 + j + 1)

        shape_array = [
            [longitude_0, latitude_0],
            [longitude_1, latitude_1],
            [longitude_2, latitude_2],
            [longitude_3, latitude_3],
            [longitude_0, latitude_0]
        ]

        # only add the shape array to the master list if it intersects or is contained within the USA
        if self._shape_is_in_US(shape_array):
            self._shape_arrays.append(shape_array)

        return longitude_3, latitude_0


    def _shape_is_in_US(self, shape_array):

        # create shapely polygon out of the shape array
        square = Polygon(shape_array)

        # true if square either intersects the border of _US_boundary, or if it is included within the boundary
        return self._US_boundary.intersects(square)


    def _save_to_kml(self):
        """
        Creates a KML file of this grid viewable in Google Maps and Google Earth.
        See https://developers.google.com/kml/documentation/
        """

        # call a helper method to convert this array of shape arrays to a KML file
        kml_text = convert_arrays_of_geocos_to_kml(self._shape_arrays)

        # save to a file in this directory
        beautiful_grid_file = open("beautiful_grid.kml", "w")
        beautiful_grid_file.write(kml_text)
        beautiful_grid_file.close()

def main():

    grid_generator = GridGenerator(10)
    grid_generator.run()

if __name__ == "__main__":
    main()