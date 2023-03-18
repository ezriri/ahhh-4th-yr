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

### function for extracing data from vid processed script

def temp_list(num, loc, name):
    data_list = []
    for i in range(num):
        if os.path.isfile(loc + name + str(i+1)+'_data.txt'):   ### make sure is there (1 file doesn't work)
            data = np.loadtxt(loc + name + str(i+1)+'_data.txt')  ## open each file
            rows = len(data)
            for j in range(rows):
                #value = data[j]
                #if value < 0:
                data_list.append(data[j])
    return data_list

## this is just raw list of values (not cleaned)
palma_temps = temp_list(37, '/home/ezri/lab_things/processed/palma/', 'palma-')
pure_40_temps = temp_list(10, '/home/ezri/lab_things/processed/pure/', 'pure-40_')
pure_42_temps = temp_list(26, '/home/ezri/lab_things/processed/pure/', 'pure-42_')
pure_45_temps = temp_list(2, '/home/ezri/lab_things/processed/pure/', 'pure-45_')

collated_data = pd.DataFrame()
collated_data['palma'] = pd.Series(palma_temps)   # just add columns individually
collated_data['pure-40'] = pd.Series(pure_40_temps)   # in this format as they are different lengths
collated_data['pure-42'] = pd.Series(pure_42_temps)
collated_data['pure-45'] = pd.Series(pure_45_temps)

pure_temps = pure_40_temps + pure_42_temps + pure_45_temps

#  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ # 
# new function for cleaning data, giving us: sd / mean / median / cleaned list
def cleaning_list(raw_list):
    sd = np.std(raw_list)
    mean = np.mean(raw_list)
    med = np.median(raw_list)
    clean_list = []
    upper = mean + sd*3
    lower = mean - sd*3
    for i in range(len(raw_list)):
        num = raw_list[i]
        if num < upper and num > lower:
            clean_list.append(num)
    return sd , mean , med, clean_list

palma_sd, palma_mean, palma_med, palma_cleaned = cleaning_list(palma_temps)
pure_sd, pure_mean, pure_med , pure_cleaned = cleaning_list(pure_temps)

#index = ['palma','pure']
extra_info = pd.DataFrame(index = ['palma','pure'])
extra_info.insert(0,'sd',[palma_sd, pure_sd])
extra_info.insert(1,'mean',[palma_mean, pure_mean])
extra_info.insert(2,'median',[palma_med, pure_med])
extra_info.insert(3,'n_values',[len(palma_cleaned), len(pure_cleaned)])

collated_data['palma_clean'] = pd.Series(palma_cleaned)
collated_data['pure_clean'] = pd.Series(pure_cleaned)

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ # 
#have added in this function, tackle freezing fraction too 

def froze_frac(temp_list, n_values):
    new_list = -np.sort(-temp_list)  ## so list is least --> most negative 
    froz_number = []
    min_t = np.min(temp_list)  ## coolest temp needed to freeze drops
    for i in range(n_values):
        #print((i+1)/n_values)
        temp = new_list[i]
        froz_number.append((temp/min_t)*((i+1)/n_values))  ## need the brackets around (i+1), doesnt work otherwise
    return new_list, froz_number   ## temps in desending order, the frozen frac number


x_palma , y_palma = froze_frac(collated_data['palma_clean'],len(palma_cleaned))
x_pure , y_pure = froze_frac(collated_data['pure_clean'],len(pure_cleaned))

#~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ # 

collated_data['palma_re-ordered'] = pd.Series(x_palma)
collated_data['pure_re-ordered'] = pd.Series(x_pure)
collated_data['palma_froz_frac'] = pd.Series(y_palma)
collated_data['pure_froz_frac'] = pd.Series(y_pure)

collated_data.to_csv('/home/ezri/lab_things/processed/freeze_temps.csv', mode='w')
#extra_info.to_csv('/home/ezri/lab_things/processed/extra_info.csv', mode='w')

## next step --> transform these numbers into inp conc for just pure + palma

## want other csv file of mean / median / standard deviation
    
