import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd
import os
import getpass
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

############ which data ?? ####################
data = 'main' ## sensitivity / main / all
u = 5 ## windspeed
###############################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if data == 'main':
    nc_files = ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']
    names = ['Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2']
    line_colours = ['black','turquoise','royalblue','firebrick','coral']

elif data == 'sensitivity':
    nc_files = ['baseline','no_SIP','no_wr']
    names = ['Control', 'No SIP', 'No WR']
    line_colours = ['black','forestgreen','darkmagenta']


else:
    nc_files = ['baseline','no_SIP','no_wr','INP_1','INP_2','warm_seed_2','warm_seed_3']
    names = ['Control', 'No SIP', 'No WR', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2']
    line_colours = ['black','forestgreen','darkmagenta','turquoise','royalblue','firebrick','coral']


## this opens up all the netcdf files interested in --> one dic
file_loc = '/home/ezri/scm_output/no_theta/'
nc_dic = {}
for file in nc_files:
    data = file_loc + file + '.nc'
    nc_dic[file]= Dataset(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# function to make water content --> right unit (new set of keys for new dic)
# nc data is in 1 d 
# pass the dic of nc files
# 15 = cloud water mixing ratio // 23 = rain water mixing ratio // 31 = ice mixing ratio
def water_cont(dic):
    mx = ['_cloud','_rain','_ice']
    mx_num = [15,23,31]
    wc_dic = {}
    new_keys = []
    for key in dic:  ## each sim 
        inv_keys = []
        x = 0
        for n in mx_num: ## each q variable
            inv_keys.append(key+mx[x])
            pr = dic[key]['p'][:,:]
            temp = dic[key]['t'][:,:]
            rho = pr/(287*temp) # density
            b = dic[key]['q'][:,:,n]
            new_unit = b*1000*rho # in g/m3
            mean = np.mean(new_unit,axis=1)
            wc_dic[key+mx[x]] = mean
            x += 1
        new_keys.append(inv_keys)
    return wc_dic, new_keys
# keys = [['b_cloud','b_rain','b_ice'],[no_SIP_cloud, no_SIP_rain,no_SIP,ice] etc]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wc_dic, key_names = water_cont(nc_dic)

y_label =['LWC (g m$^{-3}$)','RWC (g m$^{-3}$)','IWC (g m$^{-3}$)']
abc_lab = ['a)','b)','c)']

##  make a graph
fig, axs = plt.subplots(3,1,figsize=(5, 7))
#plt.tight_layout() # 

n = 0 
for ax in range(3):
    for i in range(len(nc_files)):
        time = nc_dic[nc_files[i]]['time'][:]*u/1000.
        axs[ax].plot(time,wc_dic[key_names[i][ax]],color = line_colours[i], label = names[i])

    axs[ax].set_xlim(0,30)
    axs[ax].set_ylabel(y_label[ax])
    axs[ax].text(0.04,0.85,abc_lab[ax],fontsize=12,transform=axs[ax].transAxes)

axs[0].legend(loc='upper right')

for ax in axs.flat:
    ax.set(xlabel='Distance (km)')
    ax.label_outer()

# print to a file
plt.savefig('/home/ezri/scm_output/figs/mx_line.png', bbox_inches='tight')


## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##


