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

#palma_temps =pd.Series(main_data['palma_re-ordered'][:palma_n_values].sort_values(ascending=True)).array
#palma_temps = pd.Series(main_data['palma_re-ordered'][:palma_n_values]).array
palma_temps = main_data['palma_re-ordered'][:palma_n_values]
pure_temps = main_data['pure_re-ordered'][:pure_n_values]

#palma_froze = pd.Series(main_data['palma_froz_frac'][:palma_n_values]).array
#palma_froze = pd.Series(main_data['palma_froz_frac'][:palma_n_values].sort_values(ascending=False)).array

palma_froze = main_data['palma_froz_frac'][:palma_n_values]
pure_froze = main_data['pure_froz_frac'][:pure_n_values]

#print(palma_temps.ndim)
#print(palma_froze.ndim)

#print(palma_temps)
#print(palma_froze)


#x_palma = np.linspace(np.min(palma_temps), np.max(palma_temps), palma_n_values)
#f_cubic = interp1d(palma_temps, palma_froze, kind='cubic')



## make numbers bit nicer
#palma_temps = np.around(palma_temps, 3)
#palma_froze = np.around(palma_froze, 3)



#print(palma_temps)

#print(palma_temps.ndim)
#print(np.any(palma_temps[1:] <= palma_temps[:-1]))

plt.figure()
plt.xlim(-5,-45)
#plt.ylim(0,1)

#print(type(palma_temps))
#print(palma_temps)

## want x = temp // y = frozen frac
plt.plot(palma_temps, palma_froze,color = 'black', label = 'La Palma')
plt.plot(pure_temps, pure_froze,color = 'grey', label = 'Pure')

#


#gfg = make_interp_spline(palma_temps, palma_froze, k=3)
#y_palma = gfg(x_palma)
  
#plt.plot(x_palma, y_palma)
#plt.plot(x_palma, f_cubic(x_palma))

#plt.show()


plt.xlabel('Temperature ($^\circ$C)')
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


