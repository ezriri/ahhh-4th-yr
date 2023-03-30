## paul wrote this - i just adapted it into more useful for me

import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import os
import getpass
import matplotlib.pyplot as plt

file_loc = '/home/ezri/scm_output/'
nc_files = ['baseline','no_SIP','no_wr','bam_m_2','INP_1','INP_2','warm_seed_2']

## this opens up all the netcdf files interested in --> one dic
nc_dic = {}
for file in nc_files:
    data = file_loc + file + '.nc'
    nc_dic[file]= Dataset(data)

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
time=nc_dic['baseline']['time'][:]*u/1000. # although called "time" this is actually distance in km
dt = nc_dic['baseline']['time'][1]-nc_dic['baseline']['time'][0]
z=nc_dic['baseline']['z'][:]/1000. # height in km 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### function for giving rate + cumulative precip along the described hill
## e.g. specif_nc == nc_dic['baseline']
def precip(specif_nc):
    q=specif_nc['precip'][:,:,0] # precipitation rate defined on time x height grid 
    f_interp_precip = []
    # create a 1-d interpolant for precipitation field for every time level
    for i in range(len(time)):
    # this is z vs precip for every time level
        f_interp_precip.append(sci.interp1d(z,q[i,:],fill_value='extrapolate')) 

    # we need to know the height of the hill on the time grid
    # create the interpolant
    f_hill_interp = sci.interp1d(t[0:int(l1/2)],hill[0:int(l1/2)],fill_value='extrapolate')

    # use interpolant
    hill1 = np.maximum(f_hill_interp(time), 0.) # limit so can't go below ground as extrapolation sometimes does
    
    # now we have the interpolant, use it to get the precipitation on every time level on 
    # the contour of the hill
    rain1=np.zeros(len(time))
    for i in range(len(time)):
        rain1[i]=f_interp_precip[i](hill1[i])
    
    rate = rain1
    cumulative = np.cumsum(rain1*dt/3600)
    return rate, cumulative
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
## loop through all nc files to get rate + cumulative --> seperate dics
rate_d = {}
cumulative_d = {}

#for i in range(len(nc_files)):
#    rate, cumulative = precip(nc_dic[nc_files[i]])

for key in nc_dic:
    rate, cumulative = precip(nc_dic[key])
    rate_d[key]= rate
    cumulative_d[key] = cumulative

fig=plt.figure()

for key in cumulative_d:
    plt.plot(time, cumulative_d[key])

"""
#plt.subplot(211)
plt.plot(time,rain1)
plt.xlabel('distance (km)')
plt.ylabel('Precipitation rate (mm/hr)')
"""

#plt.subplot(212)
#plt.plot(time,)
plt.xlabel('distance (km)')
plt.ylabel('Precipitation total (mm)')

plt.savefig('/home/ezri/scm_output/scm_cumul.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##