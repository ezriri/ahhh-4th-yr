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


nc_num = pd.read_csv('/home/ezri/scm_output/og_runs_numbers.csv')
nc_per = pd.read_csv('/home/ezri/scm_output/og_runs_per.csv')
nc_names = ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']

#files =  ['ctrl','INP_1','INP_2','hygro_1','hygro_2']
var = ('cloud','rain','ice')
names = ('Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2')
stack_colours = ['skyblue', 'royalblue', 'silver'] ## correlate with different variables
hatch_l = ['\\','x','o']

# make dic of values - % water distribution, in relation to ctrl
nc_dic = {}
b = nc_num['baseline']
ctrl_t = (b[0] + b[4] + b[8]) ## this is sum of baseline mix rat (to find %)

x = 0 
for j in range(0,9,4):
    list = []
    for file in nc_names:
        num = nc_num[file][j]
        list.append((num/ctrl_t)*100) # % value of total mix ratio it takes up
    nc_dic[var[x]] = list
    x += 1
## have dictionary of 3 keys (cloud / rain / ice)
## that has list of values for percentage - for stacked bar


fig, ax = plt.subplots()
bottom = np.zeros(5)
ax_wc_lab = ax.twinx()

other_bars = []
for file in nc_names:
    list = []
    for j in range(0,9,4):
        num = nc_num[file][j]
        list.append(num)
    other_bars.append(sum(list))

ax_wc_lab.bar(names,other_bars, alpha = 0)


i = 0
for bar_lab, values in nc_dic.items():
     ax.bar(names, values, label=bar_lab, bottom=bottom, color = stack_colours[i], hatch = hatch_l[i]) ## this is plottling the stacked bars interested in
     bottom += values
     i += 1

ax.set_ylabel('Water content distribution (%)')
ax_wc_lab.set_ylabel('Average water content (gm$^{-3}$)')

cloud_patch = patches.Patch(color='skyblue',hatch ='\\' , label='LWC')
rain_patch = patches.Patch(color='royalblue', hatch ='x',label='RWC')
ice_patch = patches.Patch(color='silver',hatch = 'o', label='IWC')

# fancybox=True, shadow=True 
ax.legend(handles=[cloud_patch,rain_patch,ice_patch], bbox_to_anchor=(0.5, 1.1), ncol =3,  loc = 'upper right',fancybox=True, shadow=True)
plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/stacked_bars.png')

