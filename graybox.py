import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn import datasets, linear_model



index=int(sys.argv[1])

# formula for the gray box model
# c(T^(k+1)-T^(k))/dt=(T^(out)-T^(k))/R+Q'm+W
# nominal cooling capacity
Q=-2*3.517

# zone information
area=55.1844
heigh=3
volume=area*heigh
c=volume*1.225*1
#print c

# the data is downsampled to index minute level
dt=index*60.

train=pd.read_csv('p_test/train'+str(index)+'.csv')
# check the time when nobody is in the room 
# by assuming the internal heat gain is zero during
# that period 
gp=train.groupby('hour')

for name,group in gp:
    if int(name)<1:
            unoccupied=group
    if float(name)<6:
            unoccupied=unoccupied.merge(group,how='outer')

unoccupied.to_csv('unoccupied'+str(index)+'.csv')


# at this time, c(T^(k+1)-T^(k))/dt=(T^(out)-T^(k))/R
reg = linear_model.LinearRegression(fit_intercept=False)
x=zip(unoccupied['tout']-unoccupied['t_pre'])
y=(unoccupied['t']-unoccupied['t_pre'])*c/dt
reg.fit(x, y)
R=1/reg.coef_[0] 
#print reg.intercept_

# now it is the time to check the internal heat gain and the solar stuff 

for name,group in gp:
    if int(name)==6:
         occupied=group
    if float(name)>=6:
            occupied=occupied.merge(group,how='outer')


# at this time, cpV(T^(k+1)-T^(k))/dt-(T^(out)-T^(k))/R-Q'm=W
reg = linear_model.LinearRegression(fit_intercept=True)
#gp=occupied.groupby('hour')
# Q'/Q=eta
#eta=[]
#w=[]

print occupied['hour'].iloc[0]
x=zip(occupied['on']*Q)
y=((occupied['t']-occupied['t_pre'])*c/dt-(occupied['tout']-occupied['t_pre'])/R)
reg.fit(x, y)
w=reg.intercept_
eta=reg.coef_[0]
print eta
gp=train.groupby('weekday')
# use the last day data to calibrate the output
for name,group in gp:
    if int(name)==2:
       occupied=group
#test=pd.read_csv('p_test/test'+str(index)+'.csv')
#occupied=test
occupied['il']=occupied['t']-occupied['t_pre']-((occupied['tout']-occupied['t_pre'])/R+occupied['on']*Q*eta+w)*dt/c
occupied.to_csv('occupied'+str(index)+'.csv')
gp=occupied.groupby('hour')
il=[]
for name,group in gp:
              print name
              il.append(float(group['il'].mean()))
#             print group['hour'].iloc[0]
#             x=zip(group['on']*Q)
#             y=((group['t']-group['t_pre'])*c/dt-(group['tout']-group['t_pre'])/R)
#             reg.fit(x, y)
#             w.append(reg.intercept_)
#             eta.append(reg.coef_[0])
print il
#print w[:11]
xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60/index)
	 xlab.append(str(i+7)+':00')



for i in range(0,24,2):
	 xtic.append(i*60/index+1440/index)
	 xlab.append(str(i)+':00')

test=pd.read_csv('p_test/test'+str(index)+'.csv')

test=test[60/index*7:60/index*18]

y_real=test['t']
y_prediction=[]

print eta
tout=test['tout'].iloc[0]
on=test['on'].iloc[0]
t=test['t_pre'].iloc[0]
for i in range(len(test)):
#     print test['hour'].iloc[i]
     if int(test['hour'].iloc[i])<6:
            t=((tout-t)/R)*dt/c+t
     else:     
#            t=((tout-t)/R+on*Q*eta[int(test['hour'].iloc[i])-6]+w[int(test['hour'].iloc[i])-6])*dt/c+t
            t=((tout-t)/R+on*Q*eta+w)*dt/c+t+il[int(test['hour'].iloc[i])]
     y_prediction.append(t)
     tout=test['tout'].iloc[i]

     on=test['on'].iloc[i]


xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
plt.plot(xx,y_prediction,label='predict')
#plt.plot(xx,test['tout'],label='tout')
plt.xticks(xtic,xlab,rotation=45)
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('graybox'+str(index)+'.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()

