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
fig, (ax_main, ax_hist) = plt.subplots(2, gridspec_kw={"height_ratios": (0.90, 0.1)})
#plt.xlim(-5,-45)
ax_main.set_xlim(-5,-45)
ax_main.set_ylim(-0.05,1.05)
ax_hist.set_xlim(-5,-45)
#ax_main.set_xticks([-5, -10, -15, -20,-25,-30,-35,-40,-45])

## want x = temp // y = frozen frac
ax_main.plot(palma_temps, palma_froze,color = 'black', label = 'La Palma')
ax_main.plot(pure_temps, pure_froze,color = 'grey', label = 'Pure')

ax_hist.axis('off')
box = ax_hist.boxplot([pure_temps, palma_temps], vert=False, showfliers=False, notch=True, patch_artist=True)
#ax_hist.boxplot(pure_temps, vert=False)

for patch, color in zip(box['boxes'], ['grey','black']):
    patch.set_facecolor(color)

#ax_main.set_xticks(ax_main.get_xticks())


### this is coords for where want make lines
half = (-5,0.5)
sevenfive = (-5, 0.75)
twofive = (-5, 0.25)

palma_50_line = (-26.51,0.5)
palma_50_axis = (-26.51,-0.05)
pure_50_line = (-31.96,0.5)
pure_50_axis = (-31.96,-0.05)
palma_75_line = (-28.22,0.75)
palma_75_axis = (-28.22,-0.05)
pure_75_line = (-34.84,0.75)
pure_75_axis = (-34.84,-0.05)
palma_25_line = (-24.61,0.25)
palma_25_axis = (-24.61,-0.05)
pure_25_line = (-29.35,0.25)
pure_25_axis = (-29.35,-0.05)

coords = ax_main.transData

palma_50_horiz = ConnectionPatch(xyA=half, coordsA= coords ,xyB=palma_50_line, linestyle = '--', color = 'black', alpha = 0.5)
palma_50_vert = ConnectionPatch(xyA=palma_50_line, coordsA= coords ,xyB=palma_50_axis, linestyle = '--', color = 'black', alpha = 0.5)
palma_75_horiz = ConnectionPatch(xyA=sevenfive, coordsA= coords ,xyB=palma_75_line, linestyle = '--', color = 'black', alpha = 0.5)
palma_75_vert = ConnectionPatch(xyA=palma_75_line, coordsA= coords ,xyB=palma_75_axis, linestyle = '--', color = 'black', alpha = 0.5)
palma_25_horiz = ConnectionPatch(xyA=twofive, coordsA= coords ,xyB=palma_25_line, linestyle = '--', color = 'black', alpha = 0.5)
palma_25_vert = ConnectionPatch(xyA=palma_25_line, coordsA= coords ,xyB=palma_25_axis, linestyle = '--', color = 'black', alpha = 0.5)

pure_50_horiz = ConnectionPatch(xyA=half, coordsA= coords ,xyB=pure_50_line, linestyle = '--', color = 'grey', alpha = 0.5)
pure_50_vert = ConnectionPatch(xyA=pure_50_line, coordsA= coords ,xyB=pure_50_axis, linestyle = '--', color = 'grey', alpha = 0.5)
pure_75_horiz = ConnectionPatch(xyA=sevenfive, coordsA= coords ,xyB=pure_75_line, linestyle = '--', color = 'grey', alpha = 0.5)
pure_75_vert = ConnectionPatch(xyA=pure_75_line, coordsA= coords ,xyB=pure_75_axis, linestyle = '--', color = 'grey', alpha = 0.5)
pure_25_horiz = ConnectionPatch(xyA=twofive, coordsA= coords ,xyB=pure_25_line, linestyle = '--', color = 'grey', alpha = 0.5)
pure_25_vert = ConnectionPatch(xyA=pure_25_line, coordsA= coords ,xyB=pure_25_axis, linestyle = '--', color = 'grey', alpha = 0.5)

pal_1 = ax_main.add_artist(palma_50_horiz)
pal_2 = ax_main.add_artist(palma_50_vert)
pal_3 = ax_main.add_artist(palma_75_horiz)
pal_4 = ax_main.add_artist(palma_75_vert)
pal_5 = ax_main.add_artist(palma_25_horiz)
pal_6 = ax_main.add_artist(palma_25_vert)
pu_1 = ax_main.add_artist(pure_50_horiz)
pu_2 = ax_main.add_artist(pure_50_vert)
pu_3 = ax_main.add_artist(pure_75_horiz)
pu_4 = ax_main.add_artist(pure_75_vert)
pu_5 = ax_main.add_artist(pure_25_horiz)
pu_6 = ax_main.add_artist(pure_25_vert)


ax_main.set_xlabel('Temperature ($^\circ$C)')
ax_main.set_ylabel('Frozen fraction')
ax_main.legend()
fig.tight_layout()

plt.savefig('/home/ezri/lab_things/froze_fraction.png')


