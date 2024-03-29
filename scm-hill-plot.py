from netCDF4 import Dataset
import numpy as np
from matplotlib import rc
#rc('font',family='serif')
#rc('text',usetex = True)
#from svp import svp as svp
import matplotlib as mpl
import matplotlib.colors as colors
mpl.use('agg')

import os
import getpass

import matplotlib.pyplot as plt
#import pylab as plt   

nc_files = ['baseline','no_SIP','no_wr','bam_m_2','INP_1','INP_2','warm_seed_2','warm_seed_3'] 
   
#nc = Dataset('/home/ezri/scm_output/output.nc')
nc = Dataset('/home/ezri/scm_output/no_theta/baseline.nc')

u=5  # m/s
 
time=nc['time'][:]*u/1000.*60.
z=nc['z'][:]
q=nc['q'][:,:,:]

var = nc['t'][:,:]
var = np.transpose(var)

#var = nc['q'][:,:,14]
#var = nc['q'][:,:,31] ## ice 
#var = var*1000

#var = (nc['theta'][:,:])#/ 3600


m1=np.max(q[0,:,14]/1.e6)
m1 = np.max(var/1.e6)
#m1=np.max(q[0,:,14]/1.e7)

#precip = nc['precip'][:,:,0]
#precip = precip / 3600 

tau=6000.

rt=tau
t=np.linspace(0,rt,100)

hill=tau*1.9452/(2.*np.pi)*(1.-np.cos(2.*np.pi/tau*t))/1000.

t=(t+10)*u/1000.
t=np.append(t,t[::-1])
hill=np.append(hill,np.zeros((len(hill),1)))  
l1=len(t)
pgon=np.zeros((l1,2))
pgon[:,0]=t
pgon[:,1]=hill    
pgon=plt.Polygon(pgon,color='g',alpha=1)

## conversion to ax ## 

fig, ax = plt.subplots(figsize=(12,6))
#ax.set_facecolor('lightblue')

#ax.pcolormesh(time/60,z/1000.,q[:,:,14].T/1.e6,vmin=0.0, vmax= m1,shading='gouraud')

#ax.set_ylim((0,8))
#ax.set_xlim((0,100))
#ax.set_ylim((0,3))
#ax.set_xlim((0,15))
ax.set_xlabel('distance (km)')
ax.set_ylabel('z (km)')

#print(len(time))
#print(len(z))

print(var.shape)

#data = plt.pcolormesh(time/60,z/1000.,q[:,:,14].T/1.e6,vmin=0.0, vmax= m1,cmap='Blues_r',shading='gouraud')
#data = plt.pcolormesh(time/60,z/1000.,var.T/1.e6,vmin=0.0,cmap='Blues_r',shading='gouraud')
data = plt.pcolormesh(time/60,z/1000.,var,cmap='Reds',shading='gouraud')
#data = plt.pcolormesh(time/60,z/1000.,precip.T/1.e6,cmap='Purples',shading='gouraud')
cbar = plt.colorbar(data)
#cbar.set_clim((0,m1))
#cbar.set_label('number of cloud drops (cm$^{-3}$)')
cbar.set_label('Temp (K)')
#cbar.set_label('precip (mm)')
ax.add_patch(pgon)

nc.close()
plt.savefig('/home/ezri/scm_output/scm_hill_plot.png', bbox_inches='tight')


 
