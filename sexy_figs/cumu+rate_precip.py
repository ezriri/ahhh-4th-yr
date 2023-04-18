## paul wrote this - i just adapted it into more useful for me

import numpy as np
import scipy.interpolate as sci
from netCDF4 import Dataset
import os
import getpass
import matplotlib.pyplot as plt
import matplotlib as mpl

font = {'family': 'serif', 'size'   : 10} 
mpl.rc('font', **font)

file_loc = '/home/ezri/scm_output/no_theta/'
#nc_files = ['baseline','no_SIP','no_wr','bam_m_2']
#line_colours = ['black','forestgreen','darkmagenta']

nc_files = ['baseline','INP_1','INP_2','warm_seed_2','warm_seed_3']
names = ['Control', 'INP 1', 'INP 2', 'Hygro 1','Hygro 2']
line_colours = ['black','turquoise','royalblue','firebrick','coral']

## this opens up all the netcdf files interested in --> one dic
nc_dic = {}
for file in nc_files:
    data = file_loc + file + '.nc'
    nc_dic[file]= Dataset(data)

# assume 2.5 m/s e.g. 
u=5 # m/s

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
        f_interp_precip.append(sci.interp1d(z,q[i,:],fill_value='extrapolate')) 
    f_hill_interp = sci.interp1d(t[0:int(l1/2)],hill[0:int(l1/2)],fill_value='extrapolate')

    hill1 = np.maximum(f_hill_interp(time), 0.)    
    rain1=np.zeros(len(time))
    #SD = np.zeros(len(time))
    st_div = np.std(q[:])
    mean = np.mean(q[:])
    upper = mean + st_div*3
    lower = mean - st_div*3
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
    return rate, cumulative, st_div
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## loop through all nc files to get rate + cumulative --> seperate dics
rate_d = {}
cumulative_d = {}
sd_d = {}

for key in nc_dic:
    rate, cumulative, st_div = precip(nc_dic[key])
    rate_d[key]= rate
    cumulative_d[key] = cumulative
    sd_d[key] = st_div


fig, axs = plt.subplots(2,1) ## this is for 2 subplots
#plt.yscale('log')
#plt.ylim(0,0.5)
#plt.xlim(0,35)

x = 0 
for key in cumulative_d:
    time = nc_dic[key]['time'][:]*u/1000. 
    axs[0].plot(time, cumulative_d[key], label=names[x], color = line_colours[x])
    #axs[0].fill_between(time,cumulative_d[key]-sd_d[key],cumulative_d[key]+sd_d[key],color = line_colours[x],alpha=0.1) ##### oi oi oi this is for plotting SD in cumulative 
    axs[1].plot(time, rate_d[key], label=names[x], color = line_colours[x])
    x += 1

lab = ('Precip. total (mm)','Precip. rate (mm/hr)')
abc_lab = ['a)','b)']
for i in range(2):
    axs[i].set_xlim(0,10)
    axs[i].set_ylabel(lab[i])
    axs[i].text(0.04,0.85,abc_lab[i],transform=axs[i].transAxes, fontsize=12)

for ax in axs.flat:
    ax.set(xlabel='Distance (km)')
    ax.label_outer()
   
axs[1].legend(fancybox=True, shadow=True, loc = 'upper left', bbox_to_anchor=(0.1,1.2))
plt.tight_layout()
plt.savefig('/home/ezri/scm_output/figs/precips.png', bbox_inches='tight')

## close netcdf files 
for key in nc_dic:
    nc_dic[key].close()
##
