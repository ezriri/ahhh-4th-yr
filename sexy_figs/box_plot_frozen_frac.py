import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy.interpolate import make_interp_spline, BSpline
from scipy.interpolate import interp1d
from math import trunc
import matplotlib.lines as lines
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

font = {'family': 'serif', 'size'   : 10} 
mpl.rc('font', **font)

main_data = pd.read_csv('/home/ezri/lab_things/processed/freeze_temps.csv')
extra_info = pd.read_csv('/home/ezri/lab_things/processed/extra_info.csv')
    # palma is in row 1 / pure in row 2 ^^

palma_n_values = extra_info['n_values'][0]
pure_n_values = extra_info['n_values'][1]

palma_temps = main_data['palma_re-ordered'][:palma_n_values]
pure_temps = main_data['pure_re-ordered'][:pure_n_values]

palma_froze = main_data['palma_froz_frac'][:palma_n_values]
pure_froze = main_data['pure_froz_frac'][:pure_n_values]

#plt.figure()
#fig, ax = plt.subplots() sharex=True,
fig, (ax_main, ax_hist) = plt.subplots(2, gridspec_kw={"height_ratios": (0.90, 0.1)}, tight_layout = True)
#fig.tight_layout()

#plt.xlim(-5,-45)
ax_main.set_xlim(-5,-45)
ax_hist.set_xlim(-5,-45)
ax_main.set_ylim(-0.05,1.05)
#ax_main.set_xticks([-5, -10, -15, -20,-25,-30,-35,-40,-45])

## want x = temp // y1 = frozen frac (// y2 = frequency)
#ax_main.plot(palma_temps, palma_froze,color = 'black', label = 'La Palma (n = 561)')
#ax_main.plot(pure_temps, pure_froze,color = 'grey', label = 'Pure (n = 536)')

#ax_main_new = ax_main.twinx().twiny()
ax_main_new = ax_main.twinx()

sns.histplot(data=palma_temps, ax=ax_main, color = 'white', alpha = 0.9, fill=False, bins =10, label = 'La Palma')
sns.histplot(data=pure_temps, ax=ax_main, color = 'white', alpha = 0.9, fill=False,bins=10, label = 'pure')

#ax_main_new.set_xlim(-45,-5)
ax_main_new.set_ylim(1.05,-0.05)
#ax_main_new.xaxis.set_visible(False)
ax_main_new.yaxis.set_visible(False)

sns.kdeplot(data=palma_temps, ax=ax_main_new, cumulative = True, color = 'black', fill=False, label = 'La Palma')
sns.kdeplot(data=pure_temps, ax=ax_main_new, cumulative = True, color = 'grey', fill=False, label = 'Pure')

#ax_main.plot(palma_temps, np.around(palma_froze, 3),color = 'black', label = 'La Palma (n = 561)')
#ax_main.plot(pure_temps, np.around(pure_froze, 3),color = 'grey', label = 'Pure (n = 536)')

#ax_bis.plot(base_pal, np.cumsum(values_pal)/ np.cumsum(values_pal)[-1], color='black')



ax_hist.axis('off') # showfliers=False,

outlier = dict(marker = 'x')
box = ax_hist.boxplot([pure_temps, palma_temps], vert=False, flierprops= outlier,  widths = 0.6, notch=True, patch_artist=True)
#ax_hist.boxplot(pure_temps, vert=False)


## this is to add colour to plot
for patch, color in zip(box['boxes'], ['grey','black']):
    patch.set_facecolor(color)

#ax_main.set_xticks(ax_main.get_xticks())


## ## percentiles dictionary ## ##
palma_ls = ['palma_50','palma_75','palma_25']
pure_ls = ['pure_50','pure_75','pure_25'] 
per_dic = {}
temps = [palma_temps, pure_temps]


numbs =['50','75','25']
per_num = [50,25,75]
for i in range(3):
    pal = 'palma_'+numbs[i]
    pur = 'pure_'+numbs[i]
    per_dic[pal] = np.percentile(palma_temps, per_num[i])
    per_dic[pur] = np.percentile(pure_temps, per_num[i])

## getting the percentile values: e.g. per_dic['palma_50']

"""
## this is just to print the percentiles to screen (loop through dic)
for key in per_dic:
    print(key)
    print(per_dic[key])
"""



### this is coords for where want make lines -- put into dic format
percent_coords = {}
numbs =['50','75','25']
dec = [0.5,0.75,0.25]
names = ['palma','pure']
coor_name_ls = []  ## list of all the dic key names (will be filled in loop)

for var in names:
    for i in range(len(numbs)):
        nam1 = var + '_' + numbs[i] + '_line'
        nam2 = var + '_' + numbs[i] + '_axis'
        loc = var + '_' + numbs[i]
        percent_coords[nam1] = (per_dic[loc], dec[i])
        percent_coords[nam2] = (per_dic[loc],-0.05)
        coor_name_ls.append(nam1)
        coor_name_ls.append(nam2)

### v complicated loop for connecting all the coords together 
## also plt onto graph
# so need y_axis --- line ,line -- x_axis

percent_lines = {}
y_axis_coors = [(-5,0.5),(-5, 0.75),(-5, 0.25)]
coords = ax_main.transData

"""
for var in names:
    if var == 'palma':
        c = 'black'
    else:
        c = 'grey'
    for i in range(len(numbs)):
        line = percent_coords[var + '_' + numbs[i] + '_line']
        axis = percent_coords[var + '_' + numbs[i] + '_axis']
        y_ax = y_axis_coors[i]
        line_1 = ConnectionPatch(xyA=y_ax, coordsA= coords ,xyB=line, linestyle = '--', color = c , alpha = 0.4)
        line_2 = ConnectionPatch(xyA=line, coordsA= coords ,xyB=axis, linestyle = '--', color = c , alpha = 0.4)
        ax_main.add_artist(line_1)
        ax_main.add_artist(line_2)

"""

ax_main.set_xlabel('Temperature ($^\circ$C)')
ax_main.set_ylabel('Frozen fraction')
palma_patch = patches.Patch(color='black', label='La Palma (n = 561)')
pure_patch = patches.Patch(color='grey', label='Ultrapure (n = 536)')
#ax_main_new.legend(labels=['La Palma', 'Pure'], loc = 'upper left')
ax_main_new.legend(handles=[palma_patch,pure_patch], loc = 'upper left')

plt.savefig('/home/ezri/lab_things/froze_fraction.png')


