import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
#import seaborn as sns
import os 

## so this script opens all txt files specified, gets the numbers + writes them to csv file, (collects all freezing temps of drops together)
## ~~~~~~~~~~~~~~~~~~~~ edit this u hoe ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#drops = 'palma'
drops = 'pure'

num = 2  ## total number of files to cycle through
# palma has 32
# for pure: 40 has 10 // 42 has 20 // 45 has 2

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


data_list = []

### actual loop for opening data + extracing it
for i in range(num):
    if os.path.isfile(loc + name + str(i+1)+'_data.txt'):   ### make sure is there (1 file doesn't work)
        data = np.loadtxt(loc + name + str(i+1)+'_data.txt')  ## open each file
        rows = len(data)
        for j in range(rows):
            value = data[j]
            if value not >0:  ### little bit of cleaning here
                data_list.append(value)


collated_data = pd.DataFrame()
collated_data.insert(0,col_nam,data_list)

collated_data.to_csv('/home/ezri/lab_things/processed/freeze_temps_45.csv', mode='a')
#print(len(data_list)) 

    ### so need to get data (may be 15 / 16 points), then add to list ? and append to csv file 
    # may want all data in same csv file, just for ease ---> but different columns
    
