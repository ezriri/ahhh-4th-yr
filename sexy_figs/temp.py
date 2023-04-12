from netCDF4 import Dataset
import numpy as np
from matplotlib import rc
#rc('font',family='serif')
#rc('text',usetex = True)
#from svp import svp as svp
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt


nc = Dataset('/home/ezri/scm_output/no_theta/baseline.nc')

u =5 #m/s
z=nc['z'][:]
q=nc['q'][:,:,:]
time=nc['time'][:]*u/1000.*60.
var = nc['t'][:,:]
cloud = nc['q'][:,:,14]
cloud[cloud == 0] = np.nan ## makes any 0 values nan --> overlay plot

var = np.transpose(var)

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

fig, ax = plt.subplots(figsize=(12,6))

data = plt.pcolormesh(time/60,z/1000.,var,cmap='Reds',shading='gouraud')
cbar = plt.colorbar(data)
cbar.set_label('Temp (K)')
ax.add_patch(pgon)


plt.savefig('/home/ezri/scm_output/scm_hill_plot.png', bbox_inches='tight')

nc.close()
