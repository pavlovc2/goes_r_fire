#!/usr/bin/env python

"""Generate_Fire_Points.py: Calculate nighttime fire pixels using band 7 threshold"""

from netCDF4 import Dataset
#import matplotlib
#import matplotlib.pyplot as plt
import numpy as np
import os 
from pyproj import Proj
import datetime
#from mpl_toolkits.basemap import Basemap
#from osgeo import gdal
import itertools
import re

__author__ = "Nathan Pavlovic"
__email__ = "npavlovic@sonomatech.com"
__status__ = "Prototype"
__date__ = "2017-10-22"
__version__ = "0.0.1"

# List files

def generate_fire_points(infile, thresh, outdir):
	C_file = Dataset(infile, 'r')
	ref_ch7 = C_file.variables['CMI'][:]
	dims = C_file.dimensions.keys()

	# Data are stored as seconds since 2000-01-01 12:00:00
	secs = int(round(C_file.variables['t'][0], 0)) # Round to nearest second
	img_date = datetime.datetime(2000, 1, 1, 12) + datetime.timedelta(seconds = secs)

	b = C_file.variables['CMI']
	
	sh = C_file.variables['goes_imager_projection'].perspective_point_height
	slon = C_file.variables['goes_imager_projection'].longitude_of_projection_origin
	ssweep = C_file.variables['goes_imager_projection'].sweep_angle_axis

	# Get coordinates
	xcoords = C_file.variables['x'][:] * sh
	ycoords = C_file.variables['y'][:] * sh

	# Convert to lat lon
	p = Proj(proj = "geos", h = sh, lon_0 = slon, sweep = ssweep)
	Xs, Ys = np.meshgrid(xcoords, ycoords)
	lons, lats = p(Xs, Ys, inverse = True)

	# Subset to North Bay
	nbb = b[325:475, 30:120]
	nblons = lons[325:475, 30:120]
	nblats = lats[325:475, 30:120]

	# Get logical raster of fire/no fire
	nbbt = nbb > thresh	

	# Get locations
	firelat = nblats[nbbt]
	firelon = nblons[nbbt]

	# Join to array
	dates_str = list(itertools.repeat(str(img_date), len(firelat)))
	outarray = np.column_stack((dates_str, 
	                            firelat, firelon))

	# Write to csv
	out_file = os.path.join(outdir, "fire_points_" + re.sub(" ", "-",
	    re.sub(":", "-", str(img_date))) + ".csv")
	np.savetxt(fname = out_file, X = outarray, 
	           delimiter = ",", fmt = '%s, %s, %s', header = "Date, Lat, Lon")
	return outarray
