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

palma_temps = main_data['palma_re-ordered'][:palma_n_values]
pure_temps = main_data['pure_re-ordered'][:pure_n_values]

palma_froze = main_data['palma_froz_frac'][:palma_n_values]
pure_froze = main_data['pure_froz_frac'][:pure_n_values]

def calc_INP(froze_frac, n_value):
    INP_conc = []
    for i in range(len(froze_frac)):
        f_ice = froze_frac[i]
        # 2 equations, not sure which is correct ## may even be wrong 
        
        # account for total volume ??
        #cumulative = (-np.log(1-f_ice))/(n_value * 0.001)
        
        # just 1 ul
        cumulative = (-np.log(1-f_ice))/(0.001)
        
        ## alter this to calculate: INP / kg air 
        #cumulative = cumulative/1.293E-6  ## as density of air ~ 1.293 kg/m3 
        ## or INP / L of water 
        #cumulative = cumulative / 1E-6

        INP_conc.append(cumulative)
    return INP_conc


palma_INP = calc_INP(palma_froze, palma_n_values)
pure_INP = calc_INP(pure_froze, pure_n_values)


## also want a palma that takes into account pure as background values
# i.e. palma - pure INP conc = actual INP 
## need to align temps / or would be fine just with same frozen frac

plt.figure()
plt.xlim(-5,-45)
#plt.yscale('log')

plt.plot(palma_temps, palma_INP,color = 'black', label = 'La Palma')
plt.plot(pure_temps, pure_INP,color = 'grey', label = 'Pure')

plt.xlabel('Temperature ($^\circ$C)')
plt.ylabel('Cumulative INP conc. (cm $^{-3}$)')
#plt.ylabel('Cumulative INP conc. (kg $^{-1}$)')
#plt.ylabel('Cumulative INP conc. (L $^{-1}$)')
plt.legend()


plt.savefig('/home/ezri/lab_things/INP_vs_temp.png')

