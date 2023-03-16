import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

main_data = pd.read_csv('/home/ezri/lab_things/processed/freeze_temps.csv')
extra_info = pd.read_csv('/home/ezri/lab_things/processed/extra_info.csv')
    # palma is in row 1 / pure in row 2 ^^

palma_temps = main_data['palma_clean']
pure_temps = main_data['pure_clean']

#plt.figure()
fig, axs = plt.subplots(1,2)

sns.histplot(ax=axs[0],data=palma_temps, kde=True, color = 'black', alpha = 0.9, fill=False, bins =10, label = 'East')
sns.histplot(ax=axs[1],data=pure_temps, kde=True, color = 'grey', alpha = 0.9, fill=False,bins=10, label = 'West')

#axs[0].set_ylim(0,30)
#axs[1].set_ylim(0,30)

axs[0].legend()
axs[1].legend()


plt.savefig('temp_histogram.png')