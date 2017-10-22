## Importing
from netCDF4 import Dataset
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Read in Level 2 NetCDF
C_file = Dataset("OR_ABI-L2-CMIPC-M3C07_G16_s20172830932227_e20172830935012_c20172830935048.nc", 'r')
ref_ch7 = C_file.variables['CMI'][:]
C_file.close()
C_file = None

B_file = Dataset("OR_ABI-L2-CMIPC-M3C03_G16_s20172830932227_e20172830935000_c20172830935066.nc", 'r')
ref_ch3 = B_file.variables['CMI'][:]
B_file.close()
B_file = None

A_file = Dataset("OR_ABI-L2-CMIPC-M3C06_G16_s20172830932227_e20172830935006_c20172830935057.nc", 'r')
ref_ch6 = A_file.variables['CMI'][:]
A_file.close()
A_file = None

# Make ch6 match shape of ch3
ref_ch6_resample = np.repeat(np.repeat(ref_ch6, 2, axis = 0), 2, axis = 1)

ratio = np.divide(ref_ch6_resample, ref_ch3)

fig = plt.figure(figsize=(6,6),dpi=200)
im = plt.imshow(ratio, vmin=0, vmax=100, cmap='Greys_r')
plt.show()

fig = plt.figure(figsize=(6,6),dpi=200)
im = plt.imshow(ref_ch7, vmin=250, vmax=350, cmap='Greys_r')
plt.show()

fig = plt.figure(figsize=(6,6),dpi=200)
im = plt.imshow(ref_ch3, vmin=250, vmax=350, cmap='Greys_r')
plt.show()

fig = plt.figure(figsize=(6,6),dpi=200)
im = plt.imshow(ref_ch6, vmin=0.003, vmax=0.02, cmap='Greys_r')
plt.show()

fig = plt.figure(figsize=(6,6),dpi=200)
im = plt.imshow(diff, vmin=-10, vmax=100, cmap='Greys_r')
cb = fig.colorbar(im, orientation='horizontal')
cb.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
cb.set_label('Level 2 Reflectance')
plt.show()
