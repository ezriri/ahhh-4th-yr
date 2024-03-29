import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd
import os
import getpass
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

font = {'family': 'serif', 'size'   : 10} 
mpl.rc('font', **font)

nc_num = pd.read_csv('/home/ezri/scm_output/og_runs_numbers.csv')
nc_per = pd.read_csv('/home/ezri/scm_output/og_runs_per.csv')
nc_names = ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']

#files =  ['ctrl','INP_1','INP_2','hygro_1','hygro_2']
var = ('LWC','RWC','IWC')
#conc_var = ('N$_{cloud}$ (cm$^{-3}$)','N$_{rain}$ (cm$^{-3}$)','N$_{ice}$ (L$^{-1}$)')
names = ['Control', 'Glacio 1', 'Glacio 2', 'Hygro 1','Hygro 2']
stack_colours = ['skyblue', 'royalblue', 'silver'] ## correlate with different variables
hatch_l = ['\\','x','o']

dic_n = ['cloud','rain','ice']
conc_dic = {'cloud':[],'rain':[],'ice':[]}
sd_dic = {'cloud':[],'rain':[],'ice':[]}
conc = [12,16,20]
conc_sd = [15,19,23]


# go through each file (ctrl / inp 1 etc), then loop through each conc + add to dic (also make dic of SD)
for file in nc_names:
    for j in range(3):
        #sd_dic[dic_n[j]].append(nc_num[file][conc_sd[j]])
        if conc[j] == 20:
            conc_dic[dic_n[j]].append(nc_num[file][conc[j]]*1000) ## just ice is put into L-1
            sd_dic[dic_n[j]].append(nc_num[file][conc_sd[j]]*1000)  
        else:
            conc_dic[dic_n[j]].append(nc_num[file][conc[j]]) ## in cc
            sd_dic[dic_n[j]].append(nc_num[file][conc_sd[j]])



print(sd_dic)


fig, ax = plt.subplots()
ax_ice = ax.twinx() # need differnt axis for ice conc
ax_ice.set_yscale('log')
ax.set_yscale('log')

x = np.arange(len(names))
width = 0.25
multiplier = 0 

#attribute = cloud / rain / ice
#measurement = [5 x cloud numbers] , [5 x rain numbers], [5 x ice numbers]
b_colour = ['skyblue', 'royalblue','silver']

#c = 0
for attribute, measurement in conc_dic.items():
    offset = width * multiplier 
    ## this is to make sure plot on right axis
    if attribute == 'ice':
        axs = ax_ice
    else:
        axs = ax
    ### 
    bars = axs.bar(x+offset,measurement,width, label = attribute, yerr= sd_dic[attribute],error_kw=dict(alpha=0.5, capsize=5,capthick=1), color=b_colour[multiplier])
    multiplier += 1
 

ax.set_xticks(x+width) # set location of x tick
ax.set_xticklabels(names) # set names of x ticks
ax.set_ylabel('Cloud and Rain concentration (cm$^{-3}$)')
ax_ice.set_ylabel('Ice concentration (L$^{-1}$)')
ax.legend(loc='upper right')

cloud_patch = patches.Patch(color='skyblue', label='N$_{cloud}$')
rain_patch = patches.Patch(color='royalblue',label='N$_{rain}$')
ice_patch = patches.Patch(color='silver', label='N$_{ice}$')


## fancybox=True, shadow=True bbox_to_anchor=(0.5, 1.1),
ax.legend(handles=[cloud_patch,rain_patch,ice_patch], ncol =3, bbox_to_anchor=(0.95, 1.1),  loc = 'upper right',fancybox=True, shadow=True)


plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/nconc_sbars.png')



