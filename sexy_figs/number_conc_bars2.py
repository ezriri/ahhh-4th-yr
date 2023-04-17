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
names = ['Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2']
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
        sd_dic[dic_n[j]].append(nc_num[file][conc_sd[j]])
        if conc[j] == 20:
            conc_dic[dic_n[j]].append(nc_num[file][conc[j]]*1000) ## just ice is put into L-1  
        else:
            conc_dic[dic_n[j]].append(nc_num[file][conc[j]]) ## in cc

    #cl.append(nc_num[file][12]) # per cc
    #ra.append(nc_num[file][16]) # per cc
    #ic.append(nc_num[file][20]*1000) # per L

#conc_dic = {'cloud':cl,'rain':ra,'ice':ic}   # each key --> all values of each run
#conc_dic = {'N$_{Cloud}$':cl,'N$_{Rain}$':ra,'N$_{Ice}$':ic} 

#print(conc_dic)

fig, ax = plt.subplots()
ax_ice = ax.twinx() # need differnt axis for ice conc
ax_ice.set_yscale('log')
ax.set_yscale('log')

x = np.arange(len(names))
width = 0.25
multiplier = 0 

for attribute, measurement in conc_dic.items():
    offset = width * multiplier

#attribute = cloud / rain / ice
#measurement = [5 x cloud numbers] , [5 x rain numbers], [5 x ice numbers]
b_colour = ['skyblue', 'royalblue','silver']

#c = 0
for attribute, measurement in conc_dic.items():
    offset = width * multiplier 
    ## this is to make sure plot on right axis
    if attribute == 'ice':
        ax = ax_ice
    else:
        ax = ax
    ### 
    bars = ax.bar(x+offset,measurement,width, label = attribute, color=b_colour[multiplier])
    """
    bars
    if attribute == 'N$_{Ice}$':
        bars = ax_ice.bar(x+offset,measurement,width, label = attribute, color='silver') ## want to make sure ice has seperate axis
    elif attribute == 'N$_{Rain}$':
        bars = ax.bar(x+offset,measurement,width, label = attribute, color='royalblue') # rain
    else:
        bars = ax.bar(x+offset,measurement,width, label = attribute, color='skyblue') # cloud
    """
    multiplier += 1
 

ax.set_xticks(x+width) # set location of x tick
ax.set_xticklabels(names) # set names of x ticks
ax.set_ylabel('Cloud and Rain concentration (cm$^{-3}$)')
ax_ice.set_ylabel('Ice concentration (L$^{-1}$)')
ax.legend(loc='upper right')

"""
i = 0
for bar_lab, values in nc_dic.items():
     ax.bar(names, values, label=bar_lab, bottom=bottom, color = stack_colours[i], hatch = hatch_l[i]) ## this is plottling the stacked bars interested in
     bottom += values
     i += 1

ax.set_ylabel('Water content distribution (%)')
#ax_wc_lab.set_ylabel('Average water content (gm$^{-3}$)')
"""
cloud_patch = patches.Patch(color='skyblue', label='N$_{cloud}$')
rain_patch = patches.Patch(color='royalblue',label='N$_{rain}$')
ice_patch = patches.Patch(color='silver', label='N$_{ice}$')


## fancybox=True, shadow=True bbox_to_anchor=(0.5, 1.1),
ax.legend(handles=[cloud_patch,rain_patch,ice_patch], ncol =3, bbox_to_anchor=(0.95, 1.1),  loc = 'upper right',fancybox=True, shadow=True)


plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/nconc_sbars.png')



