import numpy as np
import matplotlib.pyplot as plt

ttr=273.15
ra=8.314/29e-3
rv=8.314/18e-3
def svp(t):
   svp_ice = 100.*6.1115*np.exp((23.036 - (t-ttr)/ 333.7)*(t-ttr)/(279.82 + (t-ttr)))
   return svp_ice

f=open('mean_profile.txt','r')

str1=f.readlines() 
imin=7

for i in range(len(str1)):
    if(str1[i] == 'Station information and sounding indices\n' ):
        break
        
imax=i-2


lenarr=imax-imin+1

press=np.zeros((lenarr))
hght =np.zeros((lenarr))
temp =np.zeros((lenarr))
dwpt =np.zeros((lenarr))
relh =np.zeros((lenarr))
mixr =np.zeros((lenarr))
theta=np.zeros((lenarr))
u=np.zeros((lenarr))
v=np.zeros((lenarr))

j=0
for i in range(imin,imax+1,1):
    sp=str1[i].split()
    press[j]=float(sp[0])*100.
    hght[j] =float(sp[1])
    temp[j] =float(sp[2])+273.15
    dwpt[j] =float(sp[3])+273.15
    relh[j] =float(sp[4])
    mixr[j] =float(sp[5])/1000.
    mixr[j] =relh[j]/100.*svp(temp[j])*ra/rv/(press[j]-svp(temp[j]))
    #mixr[j] = svp(dwpt[j])*ra/rv/(press[j]-svp(dwpt[j]))
    theta[j]=float(sp[8])
    
    direct=float(sp[6])*np.pi/180.
    speed=float(sp[7])*0.514444
    u[j]=speed*np.sin(direct)
    v[j]=speed*np.cos(direct)
    j=j+1


f.close()


# ind,=np.where(hght<2500)
# mixr[ind]=mixr[ind]*0.8
ind,=np.where((hght > 800) & (hght <= 2100))
mixr[ind]=mixr[ind]*1.5      ### this is where alter water mixing ratio

# ind,=np.where((hght > 2300) & (hght <= 3700))
# mixr[ind]=0.6*svp(temp[ind[0]])*ra/rv/(press[ind[0]]-svp(temp[ind[0]]))
# 
# ind,=np.where((hght > 2500) & (hght <= 3700))
# theta[ind]=theta[ind[0]]


# calculate the humidity and plot
for i in ind:
    relh[i] = 100.*mixr[i] 
    relh[i] /= svp(temp[i])*ra/rv/(press[i]-svp(temp[i]))


plt.ion()
plt.plot(relh,hght-hght[0])

top_level_m=10000

ind,=np.where(hght<top_level_m)
print('nm1%psurf = ' + str(press[0]) +',') 
print('nm1%tsurf = ' + str(temp[0]) +',') 

print('nm1%n_levels = ' + str(len(ind)) +',') 
print('q_read(1,1:' + str(len(ind)) + ')   = ')
str2=''
for i in range(len(ind)):
    str2 = str2 + str(mixr[i]) + ', '
print(str2)

print('theta_read(1:' + str(len(ind)) + ')   = ')    
str2=''
for i in range(len(ind)):
    str2 = str2 + str(theta[i]) + ', '
print(str2)

print('u_read(1:' + str(len(ind)) + ')   = ')    
str2=''
for i in range(len(ind)):
    str2 = str2 + str(u[i]) + ', '
print(str2)

print('v_read(1:' + str(len(ind)) + ')   = ')    
str2=''
for i in range(len(ind)):
    str2 = str2 + str(v[i]) + ', '
print(str2)

print('z_read(1:' + str(len(ind)) + ')   = ')    
str2=''
for i in range(len(ind)):
    str2 = str2 + str(hght[i]-hght[0]) + ', '
print(str2)


