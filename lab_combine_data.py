import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

## so this script opens all txt files specified, gets the numbers + writes them to csv file, (collects all freezing temps of drops together)
## ~~~~~~~~~~~~~~~~~~~~ edit this u hoe ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
drops = 'palma'
#drops = 'pure'

num = 32  ## total number of files to cycle through
# palma has 32
# for pure: 40 has 10 // 42 has 20 // 45 has 2

temp = 40 # or 42 or 45 -- for pure only
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if drops == 'palma':
    loc = '/home/ezri/lab_things/processed/palma'
    name = 'palma-'

else:
    loc = '/home/ezri/lab_things/processed/pure'
    name = 'pure-'+str(temp)+'_'



### actual loop for opening data + extracing it
for i in range(num):
    #data = np.load(loc + name + str(num+1)+'_data.txt')  ## open each file
    data = np.loadtxt(loc + name + str(num+1)+'_data.txt')  ## open each file
    
    

    ### so need to get data (may be 15 / 16 points), then add to list ? and append to csv file 
    # may want all data in same csv file, just for ease ---> but different columns
    