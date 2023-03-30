## paul wrote this - i just adapted it into more useful for me

import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import os
import getpass
import matplotlib.pyplot as plt

nc_name = 'INP_2'
file_loc = '/home/ezri/scm_output/'
#nc_files = ['baseline','no_SIP','no_wr','bam_m_2','INP_1','INP_2','warm_seed_2']

nc = Dataset(file_loc+nc_name+'.nc')

# assume 2.5 m/s e.g. 
u=5 # m/s

# the hill
tau=6000.
rt=tau
t=np.linspace(0,rt,100)
hill=tau*1.9452/(2.*np.pi)*(1.-np.cos(2.*np.pi/tau*t))/1000.
t=(t+10)*u/1000.
t=np.append(t,t[::-1])
hill=np.append(hill,np.zeros((len(hill),1)))
l1=len(t)
# note the top of the hill is t[0:l1/2] and hill[0:l1/2]

## we will just use the baseline for basic stuff
time=nc['time'][:]*u/1000. # although called "time" this is actually distance in km
dt = nc['time'][1]-nc['time'][0]
z=nc['z'][:]/1000. # height in km 
q=nc['precip'][:,:,0] # precipitation rate defined on time x height grid 


# we need to know the height of the hill on the time grid
# create the interpolant
f_hill_interp = sci.interp1d(t[0:int(l1/2)],hill[0:int(l1/2)],fill_value='extrapolate')

# use interpolant
hill1 = np.maximum(f_hill_interp(time), 0.) # limit so can't go below ground as extrapolation sometimes does


# create a 1-d interpolant for precipitation field for every time level
f_interp_precip = []
for i in range(len(time)):
    # this is z vs precip for every time level
    f_interp_precip.append(sci.interp1d(z,q[i,:],fill_value='extrapolate')) 
    
# now we have the interpolant, use it to get the precipitation on every time level on 
# the contour of the hill
rain1=np.zeros(len(time))
for i in range(len(time)):
    rain1[i]=f_interp_precip[i](hill1[i])


fig, axs = plt.subplots(2,1)
fig.suptitle(nc_name)
axs[0].plot(time,rain1)
axs[0].get_xaxis().set_visible(False)
axs[0].set_ylabel('Precipitation rate (mm/hr)')


rain1[rain1<0] = 0

axs[1].plot(time,np.cumsum(rain1*dt/3600))
axs[1].set_xlabel('distance (km)')
axs[1].set_ylabel('Precipitation total (mm)')


plt.savefig('/home/ezri/scm_output/scm_hill_pre.png', bbox_inches='tight')

nc.close()
##
