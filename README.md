Generating the grid depends on Shapely (https://pypi.python.org/pypi/Shapely)
     
Usage:

Let X be the desired area in square miles of each equal area cell

From the command-line:
    
    $ python grid_generator.py X
    
From the interpeter:

    >> from grid_generator import GridGenerator
    >> GridGenerator(sqrt(X)).run()

Output:

    /beautiful_grid.kml

The output is readily viewable in either Google Maps or Google Earth