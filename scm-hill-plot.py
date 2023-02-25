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
   
nc = Dataset('/home/ezri/scm_output/output.nc')

u=2.5 # m/s
time=nc['time'][:]*u/1000.*60.
z=nc['z'][:]
q=nc['q'][:,:,:]

m1=np.max(q[0,:,14]/1.e6)

tau=6000.
rt=tau
t=np.linspace(0,rt,100)
hill=tau*0.6/(2.*np.pi)*(1.-np.cos(2.*np.pi/tau*t))/1000.
t=(t+10)*u/1000.
t=np.append(t,t[::-1])
hill=np.append(hill,np.zeros((len(hill),1)))  
l1=len(t)
pgon=np.zeros((l1,2))
pgon[:,0]=t
pgon[:,1]=hill    
pgon=plt.Polygon(pgon,color='r',alpha=1)

## conversion to ax ## 

fig, ax = plt.subplots(figsize=(12,6))

#ax.pcolormesh(time/60,z/1000.,q[:,:,14].T/1.e6,vmin=0.0, vmax= m1,cmap='Purples', shading='gouraud')
ax.pcolormesh(time/60,z/1000.,q[:,:,14].T/1.e6,vmin=0.0, vmax= m1,shading='gouraud')
ax.set_xlabel('distance (km)')
ax.set_ylabel('z (km)')

#data = plt.pcolormesh(time/60,z/1000.,q[:,:,14].T/1.e6,vmin=0.0, vmax= m1,cmap='Purples', shading='gouraud')
data = plt.pcolormesh(time/60,z/1000.,q[:,:,14].T/1.e6,vmin=0.0, vmax= m1,shading='gouraud')
cbar = plt.colorbar(data)
cbar.set_clim((0,m1))
cbar.set_label('number of cloud drops (cm$^{-3}$)')
ax.add_patch(pgon)

nc.close()
plt.savefig('/home/ezri/scm_output/scm_hill_plot.png', bbox_inches='tight')


 
