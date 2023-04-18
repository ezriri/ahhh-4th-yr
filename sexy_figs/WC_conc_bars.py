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


nc_num = pd.read_csv('/home/ezri/scm_output/og_runs_numbers.csv')
nc_per = pd.read_csv('/home/ezri/scm_output/og_runs_per.csv')
nc_names = ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']

font = {'family': 'serif', 'size'   : 10} 
mpl.rc('font', **font)

#files =  ['ctrl','INP_1','INP_2','hygro_1','hygro_2']
var = ('LWC','RWC','IWC')
var = ('cloud','rain','ice')
names = ('Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2')
#stack_colours = ['skyblue', 'royalblue', 'silver'] ## correlate with different variables
hatch_l = [None,'x','..']

# make dic of values - % water distribution, in relation to ctrl
nc_dic = {}
wc_dic = {}
b = nc_num['baseline']
ctrl_t = (b[0] + b[4] + b[8]) ## this is sum of baseline mix rat (to find %)

x = 0 
for j in range(0,9,4):
    list_per = []
    list_wc = []
    for file in nc_names:
        num = nc_num[file][j]
        list_wc.append(num)
        list_per.append((num/ctrl_t)*100) # % value of total mix ratio it takes up
    nc_dic[var[x]] = list_per
    wc_dic[var[x]] = list_wc
    x += 1
## have dictionary of 3 keys (cloud / rain / ice)
## that has list of values for percentage - for stacked bar

fig, ax = plt.subplots()
bottom = np.zeros(5)
ax_wc_lab = ax.twinx()


#ax_wc_lab.bar(names,other_bars, alpha = 0)
i = 0
for bar_lab, values in wc_dic.items():
     ax_wc_lab.bar(names, values,alpha =0) ## this is plottling the stacked bars interested in
     bottom += values
     i += 1

# , color = stack_colours[i]
i = 0
for bar_lab, values in nc_dic.items():
     ax.bar(names, values, label=bar_lab, bottom=bottom, fill=False, hatch = hatch_l[i]) ## this is plottling the stacked bars interested in
     bottom += values
     i += 1

ax.set_ylabel('Water content distribution (%)')
ax_wc_lab.set_ylabel('Average water content (g m$^{-3}$)')

## remove colours color='skyblue', color='royalblue',color='silver',
cloud_patch = patches.Patch(fill=False, label='Cloud')
rain_patch = patches.Patch(hatch ='xx',fill=False, label='Rain')
ice_patch = patches.Patch(hatch = '..',fill=False, label='Ice')

# fancybox=True, shadow=True 
ax.legend(handles=[cloud_patch,rain_patch,ice_patch], bbox_to_anchor=(0.5, 1.1), ncol =3,  loc = 'upper right',fancybox=True, shadow=True)
plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/stacked_bars.png')

