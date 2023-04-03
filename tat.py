import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd

nc = Dataset('/home/ezri/scm_output/baseline.nc')

rain = (nc['q'][:,:,15])*1000

mean = np.max(rain)
mean_0 = np.amax(rain,axis=0)
mean_1 = np.amax(rain,axis=1)
#mean = np.mean(rain)
#print(rain.shape)
# (7200, 100)  (rows,columns)
#print(mean)
#print(mean_0)
#print(mean_1)
#print(mean)

nc_numbers = pd.read_csv('/home/ezri/scm_output/nc_numbers.csv')

print(nc_numbers['INP_2'][6])
