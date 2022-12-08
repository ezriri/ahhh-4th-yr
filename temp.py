### works ###

import matplotlib
matplotlib.use('Agg') # display not needed (if run over server)

from matplotlib import pyplot as plt

from netCDF4 import Dataset 

import numpy as np

# open file
nc = Dataset('/home/ezri/output/output_2C.nc')

tt= 40

fig=plt.figure()
# extract needed variables
y = nc['y'][:]
z = nc['z'][:]
th = nc['th'][tt,:,:,:]
tref = nc['trefn'][:]

temp = th + tref

time=nc['time'][:]

#temp =np.mean(temp,axis=1)

#plt.pcolormesh(y,z,th[0].transpose(),cmap='coolwarm',shading='gouraud')
plt.pcolormesh(y,z,temp[0].transpose(),cmap='coolwarm',shading='gouraud')
im = plt.pcolormesh(y,z,temp[0].transpose(),cmap='coolwarm',shading='gouraud')


plt.axis('off')
#plt.title('Temperature (' + str(time[tt]) + 's)')
#plt.xlabel('Distance (m)')
#plt.ylabel('Height (m)')

plt.ylim((0,4000))
plt.xlim((-3000,3000))
#plt.clim((-0.05,0.05))
cbar = plt.colorbar(im,fraction=0.046, pad=0.04)
#data,ax=, location='left'
cbar.set_label('Temp (K)')
#cbar.set_clim(0,2)

plt.gca().set_aspect('equal')
#plt.gca().autoscale(tight=True)


# print to a file
plt.savefig('/tmp/individual_plot/temp.png', bbox_inches='tight')
