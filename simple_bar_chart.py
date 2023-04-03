import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd
import os
import getpass
import matplotlib.pyplot as plt

## we are looking at the actual results
# give the row numbers of interest + sd
n_row = 4 
sd_row = 7
title_n = 'mean rain mixing ratio'


#var = 'c_mr' # c_mr / r_mr / i_mr / c_c / r_c / i_c / r_r / r_c

files =  ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']
nc_numbers = pd.read_csv('/home/ezri/scm_output/nc_numbers.csv')

bar_numbs = []
sd = []

for i in range(len(files)):
    bar_numbs.append(nc_numbers[files[i]][n_row])
    sd.append(nc_numbers[files[i]][sd_row])

fig, ax = plt.subplots()

ax.bar(files,bar_numbs,yerr=sd)
ax.set_title(title_n)

# Save the figure and show
plt.tight_layout()
plt.savefig('/home/ezri/scm_output/bars.png')

