import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import lsq_linear

cc=-2*3.517
#cc=1
train=pd.read_csv('train.csv')

x=zip(train['tout']-train['t_pre'],train['on']*cc,[1]*len(train))

y=(train['t']-train['t_pre'])

res = lsq_linear(x,y,bounds=([0,0,0], [100., 100.,100.]), lsmr_tol='auto', verbose=1)
print res
x=res['x']

xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60)
	 xlab.append(str(i+7)+':00')


for i in range(0,24,2):
	 xtic.append(i*60+1440)
	 xlab.append(str(i)+':00')


test=pd.read_csv('test.csv')
test=test[60*7:18*60]
y_real=test['t']
y_prediction=[]

x1=test['tout'].iloc[0]
x2=test['on'].iloc[0]
t1=test['t_pre'].iloc[0]
for i in range(len(test)):
     t1=(x[0]*(x1-t1)+x[1]*x2*cc+x[2])+t1
    
     y_prediction.append(t1)
     x1=test['tout'].iloc[i]
     x2=test['on'].iloc[i]

output=pd.DataFrame()
output['real']=y_real
output['prediction']=y_prediction
output.to_csv('graybox.csv')

xx=np.arange(len(y_real))
fig, ax1 = plt.subplots()
ax1.plot(xx,y_real,label='real',color='r')
ax1.plot(xx,y_prediction,label='predict')
#ax1.plot(xx,test['tout'],label='outdoor')
#ax1.plot(xx,test['tdis'],color='green')
plt.xticks(xtic,xlab,rotation=45)
plt.xlim(xx[0],xx[-1])
ax1.set_ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
#ax2 = ax1.twinx()
#ax2.plot(xx,test['on'],label='real')
#ax2.set_ylabel('On_OFF')
plt.legend(loc='best')
plt.savefig('graybox.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()