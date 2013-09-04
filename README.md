This package subdivides the USA territory into an equal-area grid. Grid generation relies on formulas given by the Equal-Area Scalable Earth Grid (EASE), which was created by the National Snow and Ice Data Center (NSIDC) in 1992. This specific implementation uses the Global Cylindrical Equal-Area Projection. Please see http://nsidc.org/data/ease/ease_grid.html for more information.

Generating the grid depends on Shapely (https://pypi.python.org/pypi/Shapely)

Usage:

Let X be the desired area in square miles of each equal area cell, and Y = sqrt(X). From the command-line:
    
    $ python grid_generator.py Y
    
From the interpeter:

    >> from grid_generator import GridGenerator
    >> GridGenerator(Y).run()

Output:

    /beautiful_grid.kml

The output is readily viewable in either Google Maps or Google Earth