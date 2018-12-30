import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import sys

index=int(sys.argv[1])

reg = linear_model.LinearRegression(fit_intercept=True)

train=pd.read_csv('p_test/train'+str(index)+'.csv')

x=zip(train['on'],train['tout'],train['t_pre'])

y=train['t']

reg.fit(x, y)
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
x=zip(test['on'][0:1],test['tout'][0:1],test['t_pre'][0:1])
for i in range(len(test)):
     t_tmp=reg.predict(x)
    
     y_prediction.append(t_tmp[0])
     x=zip(test['on'][i+1:i+2],test['tout'][i+1:i+2],t_tmp)
output=pd.DataFrame()
output['real']=y_real
output['prediction']=y_prediction
output.to_csv('lse.csv')
xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
plt.plot(xx,y_prediction,label='predict')
plt.xticks(xtic,xlab,rotation=45)
print xx
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('lse'+str(index)+'.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()

