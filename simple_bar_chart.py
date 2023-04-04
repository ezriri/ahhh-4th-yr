import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd
import os
import getpass
import matplotlib.pyplot as plt

## we are looking at the actual results
# give the row numbers of interest + sd
n_row = 28
sd_row = 31
#title_n = 'mean ice mixing ratio'
#y_lab = 'ice mixing ratio (g/kg)'
#title_n = 'mean ice number conc'
#y_lab = 'ice number conc (kg$^{-1}$)'
title_n = 'cumulative rain'
y_lab = 'cumulative rain (mm/hr)'

#var = 'c_mr' # c_mr / r_mr / i_mr / c_c / r_c / i_c / r_r / r_c

#files =  ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']
files = ['baseline','no_SIP','no_wr','bam_m_2']
nc_numbers = pd.read_csv('/home/ezri/scm_output/nc_numbers.csv')

bar_numbs = []
sd = []

for i in range(len(files)):
    bar_numbs.append(nc_numbers[files[i]][n_row])
    sd.append(nc_numbers[files[i]][sd_row])

fig, ax = plt.subplots()
ax.set_yscale('log')
#ax.bar(files,bar_numbs,yerr=sd)
ax.bar(files,bar_numbs)
ax.set_title(title_n)
ax.set_ylabel(y_lab)

# Save the figure and show
plt.tight_layout()
plt.savefig('/home/ezri/scm_output/bars.png')

