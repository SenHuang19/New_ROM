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

# the data is down-sampled to index minute level
dt=index*60.

train=pd.read_csv('p_try/train'+str(index)+'.csv')

reg = linear_model.LinearRegression(fit_intercept=True)

gp=train.groupby('hour')
c1=[]
c2=[]
c3=[]
for name,group in gp:
#    offs=group.loc[group['on']<1]
#    reg = linear_model.LinearRegression(fit_intercept=False)
#    x=zip(offs['tout']-offs['t_pre'])

#    y=(offs['t']-offs['t_pre'])

#    reg.fit(x, y)
#    print reg.coef_
#
    x=zip(group['tout']-group['t_pre'],group['on']*Q)

    y=(group['t']-group['t_pre'])*c/dt


    reg.fit(x, y)

    c1.append(reg.coef_[0])
    c2.append(reg.coef_[1])
    c3.append(reg.intercept_)
    print reg.coef_[0]

test=pd.read_csv('p_try/test'+str(index)+'.csv')
y_real=test['t']
tout=test['tout'].iloc[0]
on=test['on'].iloc[0]
t=test['t_pre'].iloc[0]
y_prediction=[]
for i in range(len(test)):
     hourindex=int(test['hour'].iloc[i])
#     print hourindex
     t=((tout-t)*c1[hourindex]+on*Q*c2[hourindex]+c3[hourindex])*dt/c+t
     y_prediction.append(t)
     tout=test['tout'].iloc[i]

     on=test['on'].iloc[i]
xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60/index)
	 xlab.append(str(i)+':00')



for i in range(0,24,2):
	 xtic.append(i*60/index)
	 xlab.append(str(i)+':00') 

xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
plt.plot(xx,y_prediction,label='predict')
#plt.plot(xx,test['tout'],label='tout')
plt.xticks(xtic,xlab,rotation=45)
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('try'+str(index)+'.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()