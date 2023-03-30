import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import os
import getpass
import matplotlib.pyplot as plt

## number of specif q variable of interest
n = 23

file_loc = '/home/ezri/scm_output/'
nc_files = ['baseline','no_SIP','no_wr','bam_m_2','INP_1','INP_2','warm_seed_2']
u=5 ## wind speed -m/s
## this opens up all the netcdf files interested in --> one dic
nc_dic = {}
for file in nc_files:
    data = file_loc + file + '.nc'
    nc_dic[file]= Dataset(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# give it dictionary of netcdf + q value number we want
# will return a dic with same keys, but of mean values against time
def extract_v(dic,n):
    var = {}
    for key in dic:
        b = dic[key]['q'][:,:,n]
        new_unit = b/1000 # in g/kg
        mean = np.mean(new_unit,axis=1)
        var[key] = mean
    return var
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

cloud = extract_v(nc_dic,15)

fig=plt.figure()
#plt.yscale('log')
#plt.ylim(0,0.5)
plt.xlim(0,35)

# go through and plot all 
for key in cloud:
    time = nc_dic[key]['time'][:]*u/1000.
    plt.plot(time, cloud[key], label=key)

plt.xlabel('distance (km)')
plt.ylabel('cloud mixing ratio (g/kg)')

plt.legend()

plt.savefig('/home/ezri/scm_output/mix_ratio.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##
