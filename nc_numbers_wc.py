## this script gets SD / mean / max / min of nc data set + write to csv
## have remembered that mixing ratio --> water content
## number conc in n/cc

import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import os
import getpass
import matplotlib.pyplot as plt
import pandas as pd

## !! homemade function (paul wrote)
from precip_on_hill_multi import precip
## !!

# precip rate + cumulative will be here too
# what q's looking at?
q_mix_rat = [15,23,31] ## currently kg/kg
q_num_conc = [14,22,30] ## currently n/kg
prec = ['p_r','p_c']
########
file_loc = '/home/ezri/scm_output/no_theta/'
nc_files = ['baseline','no_SIP','no_wr','bam_m_2','INP_1','INP_2','warm_seed_2','warm_seed_3'] ## these will each be their own columns

nc_dic = {}
for file in nc_files: ## this opens up all the netcdf files interested in --> one dic
    data = file_loc + file + '.nc'
    nc_dic[file]= Dataset(data)


all_var = q_mix_rat + q_num_conc + prec
lables = ['mean', 'max','min','SD']
all_labs = []

## make list of all things will be put --> csv
for num in all_var:
    for variable in lables:
        all_labs.append(str(num)+'_'+variable)


############################ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
new_nc_values = {} ## keys --> nc_files

def calc(q,list):
    list.append(np.nanmean(q))
    list.append(np.nanmax(q))
    list.append(np.nanmin(q))
    list.append(np.nanstd(q))
    return list


for key in nc_dic:
    key_list =[]
    nc = nc_dic[key]
    pr = nc['p'][:,:]
    temp = nc['t'][:,:]
    rho = pr/(287*temp) # density
    for i in q_mix_rat: ##( we want to make --> g/kg )
        q = (nc['q'][:,:,i])*1000 # g/kg
        q = q * rho ## g/m3
        q[q == 0] = np.nan ## we want to get mean mixing ratio of just cloud, not empty space
        key_list = calc(q,key_list)

    for j in q_num_conc:
        q = (nc['q'][:,:,j])/1.e6 ## n/cm3
        q[q == 0] = np.nan ## we want to get mean mixing ratio of just cloud, not empty space
        key_list = calc(q,key_list)

    rate, cumulative = precip(nc_dic[key])
    key_list = calc(rate,key_list)
    key_list = calc(cumulative,key_list)

    new_nc_values[key] = key_list
############################ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



######################## write it to csv ####################
collated_data = pd.DataFrame(index = all_labs)

for i in range(len(nc_files)):
    name = nc_files[i]
    collated_data.insert(i,name,new_nc_values[name])

collated_data.to_csv('/home/ezri/scm_output/nc_numbers_wc.csv', mode='w')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
#
