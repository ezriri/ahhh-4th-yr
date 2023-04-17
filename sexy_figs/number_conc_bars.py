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
names = ('Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2')
stack_colours = ['skyblue', 'royalblue', 'silver'] ## correlate with different variables
hatch_l = ['\\','x','o']

nc_dic = {}

wc = [0,4,8]
conc = [12,16,20]

x = 0 
for j in range(3):
    list = []
    for file in nc_names:
        num = nc_num[file][conc[j]]
        list.append(num)
    nc_dic[var[x]] = list
    x += 1
## have dictionary of 3 keys (cloud / rain / ice)
## that has list of values for percentage - for stacked bar


fig, ax = plt.subplots()
bottom = np.zeros(5)
#ax_wc_lab = ax.twinx()


### this wont work -- need to make new dic opening up csv file
wc_bars = []
conc_bars = []
for file in nc_names:
    wc_list = []
    conc_list = []
    for j in range(3):
        w_n = nc_num[file][wc[j]]
        wc_list.append(w_n)
        c_n = nc_num[file][conc[j]]
        conc_bars.append(c_n)

    wc_bars.append(sum(wc_list))
    conc_bars.append(sum(conc_bars))

#ax_wc_lab.bar(names,wc_bars, alpha = 0) ## this is to make the second axis

print(conc_bars)

"""
i = 0
for bar_lab, values in nc_dic.items():
     ax.bar(names, values, label=bar_lab, bottom=bottom, color = stack_colours[i], hatch = hatch_l[i]) ## this is plottling the stacked bars interested in
     bottom += values
     i += 1

ax.set_ylabel('Water content distribution (%)')
#ax_wc_lab.set_ylabel('Average water content (gm$^{-3}$)')

cloud_patch = patches.Patch(color='skyblue',hatch ='\\' , label='N$_{cloud}$')
rain_patch = patches.Patch(color='royalblue', hatch ='x',label='N$_{rain}$')
ice_patch = patches.Patch(color='silver',hatch = 'o', label='N$_{ice}$')

# fancybox=True, shadow=True 
ax.legend(handles=[cloud_patch,rain_patch,ice_patch], bbox_to_anchor=(0.5, 1.1), ncol =3,  loc = 'upper right',fancybox=True, shadow=True)
plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/nconc_sbars.png')
"""


