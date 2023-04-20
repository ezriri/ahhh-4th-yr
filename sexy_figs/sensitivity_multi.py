import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import pandas as pd
import os
import getpass
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

font = {'family': 'serif', 'size'   : 10} 
mpl.rc('font', **font)

nc_files = ['baseline','no_SIP','no_wr']
names = ['Control', 'No SIP', 'No WR']
line_colours = ['black','forestgreen','darkmagenta'] 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
## this is all for precip xoxo

u = 5 ## windspeed

## this opens up all the netcdf files interested in --> one dic
file_loc = '/home/ezri/scm_output/no_theta/'
nc_dic = {}
for file in nc_files:
    data = file_loc + file + '.nc'
    nc_dic[file]= Dataset(data)

# the hill
tau=6000.
rt=tau
t=np.linspace(0,rt,100)
hill=tau*1.9452/(2.*np.pi)*(1.-np.cos(2.*np.pi/tau*t))/1000.
t=(t+10)*u/1000.
t=np.append(t,t[::-1])
hill=np.append(hill,np.zeros((len(hill),1)))
l1=len(t)
# note the top of the hill is t[0:l1/2] and hill[0:l1/2]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### function for giving rate + cumulative precip along the described hill
## e.g. specif_nc == nc_dic['baseline']
def precip(specif_nc):
    time=specif_nc['time'][:]*u/1000. # although called "time" this is actually distance in km
    dt = specif_nc['time'][1]-specif_nc['time'][0]
    z=specif_nc['z'][:]/1000. # height in km 
    q=specif_nc['precip'][:,:,0] # precipitation rate defined on time x height grid 
    f_interp_precip = []
    # create a 1-d interpolant for precipitation field for every time level
    for i in range(len(time)):
    # this is z vs precip for every time level
        f_interp_precip.append(sci.interp1d(z,q[i,:],fill_value='extrapolate')) 

    # we need to know the height of the hill on the time grid
    # create the interpolant
    f_hill_interp = sci.interp1d(t[0:int(l1/2)],hill[0:int(l1/2)],fill_value='extrapolate')

    # use interpolant
    hill1 = np.maximum(f_hill_interp(time), 0.) # limit so can't go below ground as extrapolation sometimes does
    
    # now we have the interpolant, use it to get the precipitation on every time level on 
    # the contour of the hill
    rain1=np.zeros(len(time))
    #print(f_hill_interp.ndim)
    sd = np.std(q[:])
    mean = np.mean(q[:])
    upper = mean + sd*3
    lower = mean - sd*3
    for i in range(len(time)):
        rain1[i]=f_interp_precip[i](hill1[i])
	## adding in cleaning bit
        #precip = f_interp_precip[i](hill1[i])
        #if precip < upper and precip > lower:
        #    rain1[i]= precip
	
    rate = rain1
    ## this bit is supposed to make all negative values = 0
    rain1[rain1<0] = 0
    cumulative = np.cumsum(rain1*dt/3600)
    return rate, cumulative

rate_d = {}
cumulative_d = {} # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! precip values

for key in nc_dic:
    rate, cumulative = precip(nc_dic[key])
    rate_d[key]= rate
    cumulative_d[key] = cumulative


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
## this is for number conc / water mixing ratio
dic_n = ['cloud','rain','ice']
conc_dic = {'cloud':[],'rain':[],'ice':[]} 
mix_dic = {'cloud':[],'rain':[],'ice':[]}

nc_num = pd.read_csv('/home/ezri/scm_output/og_runs_numbers.csv')
nc_per = pd.read_csv('/home/ezri/scm_output/og_runs_per.csv')

conc_nums = [12,16,20]
mix_nums = [0,4,8]

for file in nc_files:
    for j in range(3):
        #sd_dic[dic_n[j]].append(nc_num[file][conc_sd[j]])
        if conc_nums[j] == 20:
            conc_dic[dic_n[j]].append(nc_num[file][conc_nums[j]]*1000) ## just ice is put into L-1
            mix_dic[dic_n[j]].append(nc_num[file][mix_nums[j]])  # still g/m3
        else:
            conc_dic[dic_n[j]].append(nc_num[file][conc_nums[j]]) ## in cc
            mix_dic[dic_n[j]].append(nc_num[file][mix_nums[j]]) # still g/m3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### plot babe
fig = plt.figure(figsize=(12,9))

## precip first
#precip_ax = plt.subplot2grid((2,3),(0,0),colspan=2, rowspan = 2)
precip_ax = plt.subplot2grid((2,3),(0,0),colspan=2)
rate_ax = plt.subplot2grid((2,3),(1,0),colspan=2)

abc_lab = ['a)','b)']
rain_ax = (precip_ax,rate_ax)
lab = ('Precip. total (mm)','Precip. rate (mm/hr)')
for i in range(2):
    rain_ax[i].set_xlim(0,10)
    rain_ax[i].set_ylabel(lab[i])
    rain_ax[i].text(0.04,0.9,abc_lab[i],transform=rain_ax[i].transAxes, fontsize=12) 

precip_ax.axes.xaxis.set_ticklabels([]) ## get rid of x tick lables
rate_ax.set_xlabel('Distance (km)')

x = 0 
for key in cumulative_d:
    time = nc_dic[key]['time'][:]*u/1000. 
    precip_ax.plot(time, cumulative_d[key], label=names[x], color = line_colours[x])
    rate_ax.plot(time, rate_d[key], label=names[x], color = line_colours[x])
    x += 1


#precip_ax.set_xlim(0,30)
#precip_ax.set_ylabel('Precip. total (mm)')
#precip_ax.set_xlabel('Distance (km)')
rate_ax.legend(fancybox=True, shadow=True,loc="upper right", bbox_to_anchor=(0.9,1.1))

## now mix ratio #################################################
mx_ax = plt.subplot2grid((2,3),(0,2))

x = np.arange(len(names))
width = 0.25
multiplier = 0 
hatch_l = [None,'x','..']

for attribute, measurement in mix_dic.items():
    offset = width * multiplier
    bars = mx_ax.bar(x+offset,measurement,width, label = attribute, fill=False,hatch=hatch_l[multiplier])
    multiplier += 1

mx_ax.set_xticks(x+width) # set location of x tick
mx_ax.set_xticklabels(names) # set names of x ticks
mx_ax.set_ylabel('Average water content (g m$^{-3}$)')

cloud_patch = patches.Patch(fill=False, label='LWC')
rain_patch = patches.Patch(hatch ='xx',fill=False, label='RWC')
ice_patch = patches.Patch(hatch = '..',fill=False, label='IWC')

mx_ax.legend(handles=[cloud_patch,rain_patch,ice_patch],loc="upper center", bbox_to_anchor=(0.5,1.1), ncol =3,fancybox=True, shadow=True) # bbox_to_anchor=(0.95, 1.1),, bbox_to_anchor=(1, 1.1)

## now number conc ##########################################
conc_ax = plt.subplot2grid((2,3),(1,2))
ax_ice = conc_ax.twinx()

mx_ax.text(0.05,0.9,'c)',transform=mx_ax.transAxes, fontsize=12)
conc_ax.text(0.05,0.9,'d)',transform=conc_ax.transAxes, fontsize=12)

conc_ax.set_yscale('log')
mx_ax.set_yscale('log')

ax_ice.xaxis.set_visible(False)
conc_ax.set_xticks(x+width) # set location of x tick
conc_ax.set_xticklabels(names) # set names of x ticks

#conc_ax.invert_yaxis()
#ax_ice.invert_yaxis()

b_colour = ['skyblue', 'royalblue','silver']
multiplier = 0

for attribute, measurement in conc_dic.items():
    offset = width * multiplier 
    ## this is to make sure plot on right axis
    if attribute == 'ice':
        axs = ax_ice
    else:
        axs = conc_ax
    ### 
    bars = axs.bar(x+offset,measurement,width, label = attribute, color=b_colour[multiplier])
    multiplier += 1

conc_ax.set_xticks(x+width) # set location of x tick
conc_ax.set_ylabel('Cloud and Rain concentration (cm$^{-3}$)')
ax_ice.set_ylabel('Ice concentration (L$^{-1}$)')

cloud_patch = patches.Patch(color='skyblue', label='N$_{cloud}$')
rain_patch = patches.Patch(color='royalblue',label='N$_{rain}$')
ice_patch = patches.Patch(color='silver', label='N$_{ice}$')

conc_ax.legend(handles=[cloud_patch,rain_patch,ice_patch],loc="upper center", bbox_to_anchor=(0.5,1.1), ncol =3,fancybox=True, shadow=True)
#conc_ax.legend(handles=[cloud_patch,rain_patch,ice_patch],loc="lower center", bbox_to_anchor=(0.5,-0.1), ncol =3,fancybox=True, shadow=True)#,  loc = 'lower right' , bbox_to_anchor=(1, -0.1)

plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/sens_plot.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##
