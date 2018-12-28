import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import lsq_linear


# formula
# cpV(T^(k+1)-T^(k))/dt=(T^(out)-T^(k))/R+Qm+W

# nominal cooling capacity
Q=-2*3.517

# zone information
area=55.1844
heigh=3
volume=area*heigh
c=volume*1.225*1

print c

# the data is down_sampled to 15 minute level
dt=15*60.

train=pd.read_csv('train15.csv')

# check the time when nobody is in the room 
# by assuming the internal heat gain is zero during
# that period 
gp=train.groupby('hour')

i=1
for name,group in gp:
    if i==1:
         unoccupied=group
    if float(name)<6:
            unoccupied=unoccupied.merge(group,how='outer')
    i=i+1

unoccupied.to_csv('unoccupied15.csv')

# at this time, cpV(T^(k+1)-T^(k))/dt=(T^(out)-T^(k))/R

right=unoccupied['tout']-unoccupied['t_pre']
left=(unoccupied['t']-unoccupied['t_pre'])*c/dt

z=left/right

R=1/z.mean()

print R

# now it is the time to check the internal heat gain and the solar stuff 
i=1
for name,group in gp:
    if i==6:
         occupied=group
    if float(name)>=6:
            occupied=occupied.merge(group,how='outer')
    i=i+1


gp1=occupied.groupby('weekday')
w1=[0,0,0,0,0]
for name,group in gp1:
#    print name
    if name==3:
       gp=group.groupby('hour')
       for name,group in gp:

# at this time, W=cpV(T^(k+1)-T^(k))/dt-(T^(out)-T^(k))/R-Qm
             y=((group['t']-group['t_pre'])*c/dt-(group['tout']-group['t_pre'])/R)/9.*5.-group['on']*Q
             w1.append(max(y.mean(),0))
test=pd.read_csv('test15.csv')

y_real=test['t']
y_prediction=[]

x1=test['tout'].iloc[0]
x2=test['on'].iloc[0]
t1=test['t_pre'].iloc[0]
for i in range(len(test)):
  
     t1=((x1-t1)/R/9.*5.+x2*Q+w1[int(test['hour'].iloc[i])])*dt/c*9./5.+t1
     y_prediction.append(t1)
     x1=test['tout'].iloc[i]
     x2=test['on'].iloc[i]

output=pd.DataFrame()
output['real']=y_real
output['prediction']=y_prediction
output.to_csv('graybox.csv')
xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60/4)
	 xlab.append(str(i)+':00')

for i in range(0,24,2):
	 xtic.append(i*60/4+1440/4)
	 xlab.append(str(i)+':00')

xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
plt.plot(xx,y_prediction,label='predict')
#plt.xticks(xtic,xlab,rotation=45)
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('graybox_with_varying_internal_load.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()
