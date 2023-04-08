import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd
import os
import getpass
import matplotlib.pyplot as plt

## we are looking at the actual results
# give the row numbers of interest + sd
n_row = 8
sd_row = 11
#title_n = 'mean ice mixing ratio'
#y_lab = 'ice mixing ratio (g/kg)'
title_n = 'mean ice water content'
#y_lab = 'ice number conc (kg$^{-1}$)'
#title_n = 'cumulative rain'
#y_lab = 'cumulative rain (mm/hr)'
#y_lab = 'number of cloud drops (cm$^{-3}$)'
y_lab = 'ice water content (gm$^{-3}$)'

#var = 'c_mr' # c_mr / r_mr / i_mr / c_c / r_c / i_c / r_r / r_c
#files =  ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']
files =  ['baseline','INP_1','INP_2','hygro_1','hygro_2']
names = ['Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2']
#files = ['baseline','no_SIP','no_wr']
#names = ['Control', 'No SIP', 'No WR']
nc_numbers = pd.read_csv('/home/ezri/scm_output/final_numbers.csv')

bar_numbs = []
sd = []

for i in range(len(files)):
    bar_numbs.append(nc_numbers[files[i]][n_row])
    sd.append(nc_numbers[files[i]][sd_row])

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.bar(names,bar_numbs,yerr=sd)
#ax.bar(names,bar_numbs)
ax.set_title(title_n)
ax.set_ylabel(y_lab)

# Save the figure and show
plt.tight_layout()
plt.savefig('/home/ezri/scm_output/bars.png')

