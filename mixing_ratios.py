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

nc_files =  ['baseline','INP_1','INP_2','hygro_1','hygro_2']
#nc_files =  ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']
names = ['Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2']
#nc_files = ['baseline','no_SIP','no_wr']
#names = ['Control', 'No SIP', 'No WR']

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
        pr = dic[key]['p'][:,:]
        temp = dic[key]['t'][:,:]
        rho = pr/(287*temp) # density
        b = dic[key]['q'][:,:,n]
        new_unit = b*1000*rho # in g/m3
        mean = np.mean(new_unit,axis=1)
        var[key] = mean
    return var
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if mr == 'cloud':
    var = extract_v(nc_dic,15)
elif mr == 'rain':
    var = extract_v(nc_dic,23)
else:
    var = extract_v(nc_dic,31)

fig=plt.figure()
plt.yscale('log')
#plt.ylim(1e-8,1)
plt.xlim(0,35)

# go through and plot all 
i =0
for key in var:
    time = nc_dic[key]['time'][:]*u/1000.
    plt.plot(time, var[key], label=names[i])
    i = i+1

plt.xlabel('distance (km)')
plt.ylabel(mr + ' water content (gm$^{-3}$)')

plt.legend()

plt.savefig('/home/ezri/scm_output/mix_ratio.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##
