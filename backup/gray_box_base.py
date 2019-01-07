import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import sys

index=int(sys.argv[1])



reg = linear_model.LinearRegression(fit_intercept=True)

train=pd.read_csv('p_test/train'+str(index)+'.csv')

gp=train.groupby('hour')
c1=[]
c2=[]
c3=[]
c4=[]
for name, group in gp:
     x=zip(group['on'],group['tout'],group['t_pre'])
     y=group['t']
     reg.fit(x, y)
     c1.append(reg.coef_[0])
     c2.append(reg.coef_[1])
     c3.append(reg.coef_[2])
     c4.append(reg.intercept_)
     
xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60/index)
	 xlab.append(str(i)+':00')



for i in range(0,24,2):
	 xtic.append(i*60/index+1440/index)
	 xlab.append(str(i)+':00')


test=pd.read_csv('p_test/test'+str(index)+'.csv')

#test=test[60/index*7:60/index*18]

y_real=test['t']
y_prediction=[]
x1=test['on'].iloc[0]
x2=test['tout'].iloc[0]
x3=test['t_pre'].iloc[0]
for i in range(len(test)):
     time_index=int(test['hour'].iloc[i])
     x3=c1[time_index]*x1+c2[time_index]*x2+c3[time_index]*x3+c4[time_index]
     y_prediction.append(x3)
     x1=test['on'].iloc[i]
     x2=test['tout'].iloc[i]
output=pd.DataFrame()
output['real']=y_real
output['prediction']=y_prediction
output.to_csv('gray_box_base'+'.csv')
xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
plt.plot(xx,y_prediction,label='predict')
plt.xticks(xtic,xlab,rotation=45)
print xx
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('gray_box_base'+str(index)+'.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()

