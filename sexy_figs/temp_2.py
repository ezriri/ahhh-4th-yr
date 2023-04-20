## hopefully make it possible to overlay maps

from netCDF4 import Dataset
import numpy as np
from matplotlib import rc
#rc('font',family='serif')
#rc('text',usetex = True)
#from svp import svp as svp
import matplotlib as mpl
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

nc = Dataset('/home/ezri/scm_output/no_theta/baseline.nc')
#nc = Dataset('/home/ezri/scm_output/no_theta/INP_1.nc')

u =5 #m/s
z=nc['z'][:]
q=nc['q'][:,:,:]
time=nc['time'][:]*u/1000.*60.
var = nc['t'][:,:]
cloud = nc['q'][:,:,14]

#cloud[cloud == 0] = np.nan ## makes any 0 values nan --> overlay plot
var = np.transpose(var)
#cloud =np.transpose(cloud)
m1=np.max(q[:,:,14]/1.e6)

## ~~~~~~~~~~~~~~~~~~~~ hill ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
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

## ~~~~~~~~~~~~~~~~~~~~ plot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ## 
# making special colourmaps --> for overlay (code is stolen)
cmap = pl.cm.Blues
my_cmap = cmap(np.arange(cmap.N))
my_cmap[:,-1] = np.linspace(0,1,cmap.N)
my_cmap = ListedColormap(my_cmap)

##### font ##
font = {'family': 'serif', 'size'   : 10} 
mpl.rc('font', **font)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#fig, ax = plt.subplots(figsize=(12,6))
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)

ax.set_ylim((0,6))
ax.set_xlim((0,30))
ax.set_xlabel('distance (km)')
ax.set_ylabel('z (km)')
temp_plt = ax.pcolormesh(time/60,z/1000.,var,cmap='Reds',shading='gouraud')
cloud_plt = ax.pcolormesh(time/60,z/1000.,cloud.T/1.e6,vmin=0.0,cmap= my_cmap ,shading='gouraud')
t_cbar = plt.colorbar(temp_plt)
#cax = divider.append_axes("left", size="5%", pad=0.05)
c_cbar = plt.colorbar(cloud_plt) #,cax=ax) #, ax = ax, location = 'left'
t_cbar.set_label('Temp (K)')
c_cbar.set_label('N$_{cloud}$')
ax.add_patch(pgon)
#plt.title('ctrl')

nc.close()

plt.savefig('/home/ezri/scm_output/figs/hill_temp.png', bbox_inches='tight')

nc.close()
