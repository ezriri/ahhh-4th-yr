import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
#import seaborn as sns
import os 

## so this script opens all txt files specified, gets the numbers + writes them to csv file, (collects all freezing temps of drops together)

"""
#drops = 'palma'
drops = 'pure'

num = 2  ## total number of files to cycle through
# palma has 37
# for pure: 40 has 10 // 42 has 26 // 45 has 2

temp = 45 # or 42 or 45 -- for pure only

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if drops == 'palma':
    loc = '/home/ezri/lab_things/processed/palma/'
    name = 'palma-'
    col_nam = drops

else:
    loc = '/home/ezri/lab_things/processed/pure/'
    name = 'pure-'+str(temp)+'_'
    col_nam = drops+'-'+str(temp)


"""

### actual loop for opening data + extracing it

def temp_list(num, loc, name):
    data_list = []
    for i in range(num):
        if os.path.isfile(loc + name + str(i+1)+'_data.txt'):   ### make sure is there (1 file doesn't work)
            data = np.loadtxt(loc + name + str(i+1)+'_data.txt')  ## open each file
            rows = len(data)
            for j in range(rows):
                value = data[j]
                if value < 0:
                    data_list.append(value)
    return data_list

palma_temps = temp_list(37, '/home/ezri/lab_things/processed/palma/', 'palma-')
pure_40_temps = temp_list(10, '/home/ezri/lab_things/processed/pure/', 'pure-40_')
pure_42_temps = temp_list(26, '/home/ezri/lab_things/processed/pure/', 'pure-42_')
pure_45_temps = temp_list(2, '/home/ezri/lab_things/processed/pure/', 'pure-45_')

collated_data = pd.DataFrame()
collated_data.insert(0,'palma', palma_temps)
collated_data['pure-40'] = pd.Series(pure_40_temps)
collated_data['pure-42'] = pd.Series(pure_42_temps)
collated_data['pure-45'] = pd.Series(pure_45_temps)


collated_data.to_csv('/home/ezri/lab_things/processed/freeze_temps.csv', mode='w')

## next step --> transform these numbers into inp conc for just pure + palma


    
