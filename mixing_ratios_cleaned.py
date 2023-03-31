import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import os
import getpass
import matplotlib.pyplot as plt

## number of specif q variable of interest
n = 23

file_loc = '/home/ezri/scm_output/'
nc_files = ['baseline','no_SIP','no_wr','no_theta','bam_m_2','INP_1','INP_2','warm_seed_2']
u=5 ## wind speed -m/s
## this opens up all the netcdf files interested in --> one dic
nc_dic = {}
for file in nc_files:
    data = file_loc + file + '.nc'
    nc_dic[file]= Dataset(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# give it dictionary of netcdf + q value number we want
# will return a dic with same keys, but of mean values against time
## have added in cleaning bit --> all data within 3 SD
def extract_v(dic,n):
    var = {}
    for key in dic:
        b = dic[key]['q'][:,:,n]
        new_unit = b/1000 # in g/kg
        mean_axis = np.mean(new_unit,axis=1)
        sd = np.std(mean_axis[:])
        mean = np.mean(mean_axis[:])
        upper = mean + sd*3
        lower = mean - sd*3
        clean_list = []
        for i in range(len(mean_axis)):
                num = mean_axis[i]
                if num < upper and num > lower:
                        clean_list.append(num)
                else:
                        clean_list.append(None)
        var[key] = clean_list
    return var
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

cloud = extract_v(nc_dic,15)
rain = extract_v(nc_dic,23)
ice = extract_v(nc_dic,31)

fig=plt.figure()
plt.yscale('log')
#plt.ylim(0,1e-10)
plt.xlim(0,35)

# go through and plot all 
for key in ice:
    time = nc_dic[key]['time'][:]*u/1000.
    plt.plot(time, ice[key], label=key)

plt.xlabel('distance (km)')
plt.ylabel('ice mixing ratio (g/kg)')

plt.legend()

plt.savefig('/home/ezri/scm_output/mix_ratio.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##
