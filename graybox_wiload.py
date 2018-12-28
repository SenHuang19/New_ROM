import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import lsq_linear

cc=-2*3.517



train=pd.read_csv('train.csv')
gp1=train.groupby('weekday')
for name,group in gp1:
#    print name
    if name==3:
       gp=group.groupby('hour')
       x=[]
       for name,group in gp:
#    print name
             xx=zip(group['tout']-group['t_pre'],group['on']*cc,[1]*len(group))
             y=group['t']-group['t_pre']
             res = lsq_linear(xx,y,bounds=([0,0,0], [100., 100.,100.]))
             x.append(res['x'])
print x
print x[0]
xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60)
	 xlab.append(str(i)+':00')

for i in range(0,24,2):
	 xtic.append(i*60+1440)
	 xlab.append(str(i)+':00')


test=pd.read_csv('test.csv')
y_real=test['t']
y_prediction=[]

x1=test['tout'].iloc[0]
x2=test['on'].iloc[0]
t1=test['t_pre'].iloc[0]
for i in range(len(test)):
     hour=test['hour'].iloc[i]

     t1=x[int(hour)][0]*(x1-t1)+x[int(hour)][1]*x2*cc+x[int(hour)][2]+t1
    
     y_prediction.append(t1)
     x1=test['tout'].iloc[i]
     x2=test['on'].iloc[i]

plt.clf()

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

