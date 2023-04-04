import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import os
import getpass
import matplotlib.pyplot as plt

## mixing ratio of interest
mr = 'cloud' # cloud / ice / rain

file_loc = '/home/ezri/scm_output/no_theta/'
#nc_files = ['baseline','no_SIP','no_wr','bam_m_2','INP_1','INP_2','warm_seed_2','warm_seed_3']
#nc_files = ['baseline','no_SIP','no_wr','bam_m_2']
nc_files = ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']
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
        
        mean = np.mean(b,axis=1)
        var[key] = mean
    return var
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if mr == 'cloud':
    var = extract_v(nc_dic,14)
elif mr == 'rain':
    var = extract_v(nc_dic,22)
else:
    var = extract_v(nc_dic,30)

fig=plt.figure()
plt.yscale('log')
#plt.ylim(0,0.5)
plt.xlim(0,35)

# go through and plot all 
for key in var:
    time = nc_dic[key]['time'][:]*u/1000.
    plt.plot(time, var[key], label=key)

plt.xlabel('distance (km)')
plt.ylabel(mr + ' number concentration (kg$^{-1}$)')

plt.legend()

plt.savefig('/home/ezri/scm_output/num_conc.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##
