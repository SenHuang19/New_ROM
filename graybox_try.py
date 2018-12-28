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

# the data is downsampled to 15 minute level
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
    if float(name)<6 or float(name)>23:
            unoccupied=unoccupied.merge(group,how='outer')
    i=i+1

unoccupied.to_csv('unoccupied15.csv')

# at this time, cpV(T^(k+1)-T^(k))/dt=(T^(out)-T^(k))/R

xx=zip(unoccupied['tout']-unoccupied['t_pre'])
y=(unoccupied['t']-unoccupied['t_pre'])*c/dt
res = lsq_linear(xx,y,bounds=([0], [100.]))
print res['x'][0]
R=1/res['x'][0]


# now it is the time to check the internal heat gain and the solar stuff 
i=1
for name,group in gp:
    if i==6:
         occupied=group
    if float(name)>=6 and float(name)<=23:
            occupied=occupied.merge(group,how='outer')
    i=i+1

# at this time, cpV(T^(k+1)-T^(k))/dt-(T^(out)-T^(k))/R-Qm=W
gp1=occupied.groupby('weekday')
for name,group in gp1:
#    print name
    if name>=0:
       gp=group.groupby('hour')
       x=[]
       for name,group in gp:
#    print name
             xx=zip(group['on']*Q,[1]*len(group))
             y=((group['t']-group['t_pre'])*c/dt-(group['tout']-group['t_pre'])/R)/9*5
             res = lsq_linear(xx,y,bounds=([0,0], [100., 100.]))
             x.append(res['x'])
print len(x)
print x[0]
xtic=[]
xlab=[]


test=pd.read_csv('test15.csv')
test=test[4*7:18*4]
y_real=test['t']
y_prediction=[]

x1=test['tout'].iloc[0]
x2=test['on'].iloc[0]
t1=test['t_pre'].iloc[0]
for i in range(len(test)):
     if int(test['hour'].iloc[i])<6 or int(test['hour'].iloc[i])>23:
            t1=((x1-t1)/R)*dt/c+t1
     else:     
            t1=((x1-t1)/R/9.*5.+x2*Q*x[int(test['hour'].iloc[i])-5][0]+x[int(test['hour'].iloc[i])-5][1])*dt/c*9./5.+t1
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
	 xtic.append(i*4)
	 xlab.append(str(i+7)+':00')

for i in range(0,24,2):
	 xtic.append(i*4+4*24)
	 xlab.append(str(i)+':00')

xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
plt.plot(xx,y_prediction,label='predict')
plt.xticks(xtic,xlab,rotation=45)
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('graybox_with_varying_internal_load.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()