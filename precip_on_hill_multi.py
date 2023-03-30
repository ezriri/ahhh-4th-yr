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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### function for giving rate + cumulative precip along the described hill
## e.g. specif_nc == nc_dic['baseline']
def precip(specif_nc):
    time=specif_nc['time'][:]*u/1000. # although called "time" this is actually distance in km
    dt = specif_nc['time'][1]-specif_nc['time'][0]
    z=specif_nc['z'][:]/1000. # height in km 
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
    ## this bit is supposed to make all negative values = 0
    rain1[rain1<0] = 0

    ## pos want cumulative of only positive numbers
    cumulative = np.cumsum(rain1*dt/3600)
    return rate, cumulative
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
  
## loop through all nc files to get rate + cumulative --> seperate dics
rate_d = {}
cumulative_d = {}

for key in nc_dic:
    rate, cumulative = precip(nc_dic[key])
    rate_d[key]= rate
    cumulative_d[key] = cumulative

fig=plt.figure()
plt.yscale('log')
#plt.ylim(0,0.5)


for key in cumulative_d:
    plt.plot(time, cumulative_d[key], label=key)

plt.xlabel('distance (km)')
plt.ylabel('Precipitation total (mm)')

"""

for key in rate_d:
    plt.plot(time, rate_d[key], label=key)

plt.xlabel('distance (km)')
plt.ylabel('Precipitation rate (mm/hr)')
"""
plt.legend()

plt.savefig('/home/ezri/scm_output/scm_cumul.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##
