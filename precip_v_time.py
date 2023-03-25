import matplotlib
#matplotlib.use('Agg')

from matplotlib import pyplot as plt

from netCDF4 import Dataset 

import numpy as np 

nc = Dataset('/home/ezri/scm_output/output.nc')

u=5
time=nc['time'][:]*u/1000.*60.
z=nc['z'][:]
q=nc['q'][:,:,:]

fig=plt.figure()
# extract needed variables

precip = nc['precip'][:,:,0]
#var =np.mean(precip,axis=1)
var =np.sum(precip,axis=1)

cumulative_precip = np.cumsum(var)

#print(precip.ndim)

plt.plot(time, cumulative_precip)

plt.savefig('/home/ezri/scm_output/rain_v_time.png', bbox_inches='tight')

nc.close()
