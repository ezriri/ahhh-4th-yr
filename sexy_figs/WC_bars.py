import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd
import os
import getpass
import matplotlib.pyplot as plt

nc_num = pd.read_csv('/home/ezri/scm_output/og_runs_numbers.csv')
nc_per = pd.read_csv('/home/ezri/scm_output/og_runs_per.csv')
nc_names = ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']

#files =  ['ctrl','INP_1','INP_2','hygro_1','hygro_2']
var = ['cloud','rain','ice']
names = ('Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2')

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

for bar_lab, values in nc_dic.items():
     ax.bar(names, values, label=bar_lab, bottom=bottom)
     bottom += values

plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/stacked_bars.png')

