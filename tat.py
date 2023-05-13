import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd


nc = Dataset('/home/ezri/scm_output/no_theta/baseline.nc')

rain = (nc['q'][:,:,15])*1000

q = nc['t'][:,:]
print(q.shape)
## [time, level]
#print(q[1,20])

##       20 = 2km height

#z=nc['z'][:]
#print(len(z))


#mean = np.max(rain)
#mean_0 = np.amax(rain,axis=0)
#mean_1 = np.amax(rain,axis=1)
#mean = np.mean(rain)
#print(rain.shape)
# (7200, 100)  (rows,columns)
#print(mean)
#print(mean_0)
#print(mean_1)
#print(mean)

#nc_numbers = pd.read_csv('/home/ezri/scm_output/nc_numbers.csv')

#print(nc_numbers['INP_2'][0])

#print(np.nanmean(q))
#print(np.nanmax(q))
#print(np.nanmin(q))
#print(np.nanstd(q))




nc.close()
