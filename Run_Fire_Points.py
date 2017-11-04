#!/usr/bin/env python

import os
import numpy as np
from fnmatch import fnmatch

from Generate_Fire_Points import generate_fire_points

# Definitions
proj_path = "/Users/nathan/Documents/Projects/GOES_Fire_Growth"
img_path = os.path.join(proj_path, "Raw_Data")
out_path = os.path.join(proj_path, "Fire_Points")

# List files only if they are band 7

allfiles = [f for f in os.listdir(img_path) if os.path.isfile(os.path.join(img_path, f))] 
	#& fnmatch(
	#os.path.join(img_path, f), 'OR_ABI-L2-CMIPC-M3C07_G16*')]
b7files = [f for f in allfiles if fnmatch(f, 'OR_ABI-L2-CMIPC-M3C07_G16*')]

allfireslist = []
for b7file in b7files:
	outfires = generate_fire_points(os.path.join(img_path, b7file), 310, out_path)
	allfireslist.append(outfires)

fire_array = np.concatenate(allfireslist, axis = 0)

out_file = os.path.join(out_path, "fire_points_alldates.csv")
np.savetxt(fname = out_file, X = fire_array, 
           delimiter = ",", fmt = '%s, %s, %s', header = "Date, Lat, Lon")
