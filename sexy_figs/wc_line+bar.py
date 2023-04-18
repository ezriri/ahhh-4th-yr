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

############ which data ?? ####################
data = 'main' ## sensitivity / main / all
u = 5 ## windspeed
###############################################


font = {'family': 'serif', 'size'   : 10} 
mpl.rc('font', **font)

nc_num = pd.read_csv('/home/ezri/scm_output/og_runs_numbers.csv')
nc_per = pd.read_csv('/home/ezri/scm_output/og_runs_per.csv')

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
# this is bar chart stuff (copy + paste)
var = ('cloud','rain','ice')
hatch_l = [None,'x','..']

nc_dic_2 = {}
b = nc_num['baseline']
ctrl_t = (b[0] + b[4] + b[8]) ## this is sum of baseline mix rat (to find %)

x = 0 
for j in range(0,9,4):
    list = []
    for file in nc_files:
        num = nc_num[file][j]
        list.append((num/ctrl_t)*100) # % value of total mix ratio it takes up
    nc_dic_2[var[x]] = list
    x += 1

wc = [0,4,8]
conc = [12,16,20]

wc_bars = []
other_bars = []
for file in nc_files:
    wc_list = []
    conc_list = []
    for j in range(3):
        w_n = nc_num[file][wc[j]]
        wc_list.append(num)
    other_bars.append(sum(list))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wc_dic, key_names = water_cont(nc_dic)

y_label =['LWC (g m$^{-3}$)','RWC (g m$^{-3}$)','IWC (g m$^{-3}$)']
abc_lab = ['a)','b)','c)']

##  make a graph
#fig, axs = plt.subplots(3,1,figsize=(5, 7))
fig, axd = plt.subplot_mosaic([['LWC', 'bars'], ['RWC', 'bars'],['IWC', 'bars']], width_ratios=[2,1], constrained_layout=True, figsize=(8, 8))
#plt.tight_layout() # 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## line plot

mx_ax = ['LWC','RWC','IWC']

n = 0 
for ax in range(3):
    for i in range(len(nc_files)):
        time = nc_dic[nc_files[i]]['time'][:]*u/1000.
        axd[mx_ax[ax]].plot(time,wc_dic[key_names[i][ax]],color = line_colours[i], label = names[i])

    axd[mx_ax[ax]].set_xlim(0,30)
    axd[mx_ax[ax]].set_ylabel(y_label[ax])
    axd[mx_ax[ax]].text(0.04,0.85,abc_lab[ax],fontsize=12,transform=axd[mx_ax[ax]].transAxes)

axd['LWC'].legend(loc='upper right')

#for ax in axd.flat:
#    ax.set(xlabel='Distance (km)')
#    ax.label_outer()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## bar plot
ax_wc_lab = axd['bars'].twinx()
bottom = np.zeros(5)
ax_wc_lab.bar(names,other_bars, alpha = 0)


# , color = stack_colours[i]
i = 0
for bar_lab, values in nc_dic_2.items():
     axd['bars'].bar(names, values, label=bar_lab, bottom=bottom, fill=False, hatch = hatch_l[i]) ## this is plottling the stacked bars interested in
     bottom += values
     i += 1

axd['bars'].set_ylabel('Water content distribution (%)')
ax_wc_lab.set_ylabel('Average water content (g m$^{-3}$)')

## remove colours color='skyblue', color='royalblue',color='silver',
cloud_patch = patches.Patch(fill=False, label='LWC')
rain_patch = patches.Patch(hatch ='xx',fill=False, label='RWC')
ice_patch = patches.Patch(hatch = '..',fill=False, label='IWC')

# fancybox=True, shadow=True 
axd['bars'].legend(handles=[cloud_patch,rain_patch,ice_patch], bbox_to_anchor=(0.5, 1.1), ncol =3,  loc = 'upper right',fancybox=True, shadow=True)
plt.tight_layout()
# print to a file
plt.savefig('/home/ezri/scm_output/figs/mx_queen.png', bbox_inches='tight')


## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##


