import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import lsq_linear

cc=-2*3.517



train=pd.read_csv('train_5.csv')
gp=train.groupby('hour')
x=[]
for name,group in gp:
    print name
    xx=zip(group['tout']-group['t_pre'],group['on']*cc,[1]*len(group))
    y=group['t']-group['t_pre']
    res = lsq_linear(xx,y,bounds=([0, 0,0], [100., 100.,100.]))
    x.append(res['x'])
print x
xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60)
	 xlab.append(str(i)+':00')
print xtic[-1]

for i in range(0,24,2):
	 xtic.append(i*60+1440)
	 xlab.append(str(i)+':00')


test=pd.read_csv('test.csv')
y_real=test['t']
y_prediction=[y_real[0]]
print len(y_real)
x1=test['tout'].iloc[0]
x2=test['on'].iloc[0]
t1=test['t_pre'].iloc[0]
for i in range(0,len(test),5):
     hour=test['hour'].iloc[i]

     t1=x[int(hour)][0]*(x1-t1)+x[int(hour)][1]*x2*cc+x[int(hour)][2]+t1    
     y_prediction.append(t1)
     x1=test['tout'].iloc[i]
     x2=test['on'].iloc[i]
print len(y_prediction)
plt.clf()

xx=np.arange(len(y_real))
x2=np.arange(0,len(y_real)+5,5)
print len(x2)
plt.plot(xx,y_real,label='real',color='r')
plt.plot(x2,y_prediction,label='predict')
plt.xticks(xtic,xlab,rotation=45)
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('new_tot.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()

