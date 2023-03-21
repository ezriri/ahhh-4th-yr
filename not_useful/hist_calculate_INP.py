import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy.interpolate import make_interp_spline, BSpline
from scipy.interpolate import interp1d
from math import trunc

main_data = pd.read_csv('/home/ezri/lab_things/processed/freeze_temps.csv')
extra_info = pd.read_csv('/home/ezri/lab_things/processed/extra_info.csv')
    # palma is in row 1 / pure in row 2 ^^

palma_n_values = extra_info['n_values'][0]
pure_n_values = extra_info['n_values'][1]

#palma_temps = main_data['palma_re-ordered'][:palma_n_values]
palma_temps = main_data['palma_clean'][:palma_n_values]
pure_temps = main_data['pure_re-ordered'][:pure_n_values]

palma_froze = main_data['palma_froz_frac'][:palma_n_values]
pure_froze = main_data['pure_froz_frac'][:pure_n_values]

#palma_temps =pd.Series(main_data['palma_re-ordered'][:palma_n_values].sort_values(ascending=True)).array
#palma_temps = pd.Series(main_data['palma_re-ordered'][:palma_n_values]).array
#palma_froze = pd.Series(main_data['palma_froz_frac'][:palma_n_values]).array
#palma_froze = pd.Series(main_data['palma_froz_frac'][:palma_n_values].sort_values(ascending=False)).array

#pos use https://matplotlib.org/stable/gallery/statistics/histogram_cumulative.html 


#plt.figure()
fig, ax = plt.subplots()

# plot the cumulative histogram  
# density=True,
n, bins, patches = ax.hist(palma_temps, 100, kde=True,  histtype='step',cumulative=-1, label='Empirical')
#sns.histplot(data=palma_temps, kde=True, color = 'black',cumulative= -1, histtype='step', alpha = 0.9, fill=False, bins =100, label = 'Palma')
#sns.histplot(data=pure_temps, kde=True, color = 'grey',density=True, cumulative=True,alpha = 0.9, fill=False,bins=10, label = 'pure')


plt.xlim(-5,-45)

#plt.xticks(np.arange(6), ['-10', '', 'Sue'])
plt.xlabel('Temp (C)')
plt.ylabel('Frozen fraction')
#plt.legend()


"""
plt.figure()
sns.histplot(data=palma_temps, kde=True, color = 'black', alpha = 0.9, fill=False, bins =10, label = 'Palma')
sns.histplot(data=pure_temps, kde=True, color = 'grey', alpha = 0.9, fill=False,bins=10, label = 'pure')

plt.legend()
plt.xlabel('Temp (C)')
plt.ylabel('Frequency')
"""


plt.savefig('/home/ezri/lab_things/froze_fraction.png')


