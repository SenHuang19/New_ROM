import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import sys

index=int(sys.argv[1])
num=int(sys.argv[2])

reg = linear_model.LinearRegression(fit_intercept=True)

train=pd.read_csv('p_test/train'+str(index)+'.csv')
#train['on']=train['on']*(100-train['tout'])/40
train['on']=train['on'].shift(num)
#train['tout']=train['tout'].shift(num)

train=train.dropna()
gp=train.groupby('hour')

c1=[]
c2=[]
c3=[]
c4=[]
c5=[]
for name, group in gp:
        if int(name)<7 or int(name)>16:
           reg = linear_model.LinearRegression(fit_intercept=False)
           x=zip(group['on'],group['tout']-group['t_pre'])
           y=group['t']-group['t_pre']
           reg.fit(x, y)
           c3.append(0)
        else:
           reg = linear_model.LinearRegression(fit_intercept=True)
           x=zip(group['on'],group['tout'],group['t_pre'])
           y=group['t']
           reg.fit(x, y)
           c3.append(reg.coef_[2])
        c1.append(reg.coef_[0])
        c2.append(reg.coef_[1])
        

        c5.append(reg.intercept_)

#     print reg.coef_
xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60/index)
	 xlab.append(str(i)+':00')



for i in range(0,24,2):
	 xtic.append(i*60/index)
	 xlab.append(str(i)+':00')




test=pd.read_csv('p_test/test'+str(index)+'.csv')
#test['on']=test['on']*(100-test['tout'])/40
#test['tout']=test['tout'].shift(num)
test['on']=test['on'].shift(num)


test=test.dropna()

y_real=test['t']
y_prediction=[]

t=test['t_pre'].iloc[0]

for i in range(len(test)):
     time_index=int(test['hour'].iloc[i])
     print time_index
     if time_index<7 or time_index>16:
         x1=test['on'].iloc[i]
         x2=test['tout'].iloc[i]-t
#     x3=test['fanstatus'].iloc[i]	 
         t=c1[time_index]*x1+c2[time_index]*x2+c5[time_index]+t   
     else:

         x1=test['on'].iloc[i]
         x2=test['tout'].iloc[i] 
         t=c1[time_index]*x1+c2[time_index]*x2+c3[time_index]*t+c5[time_index]		 

     y_prediction.append(t)
output=pd.DataFrame()

output['real']=y_real
output['prediction']=y_prediction
output.to_csv('gray'+str(index)+'.csv')
xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
#plt.plot(xx,test['tout'],label='outdoorT')
plt.plot(xx,y_prediction,label='predict')
plt.xticks(xtic,xlab,rotation=45)
#print xx
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('gray'+str(index)+'_'+str(num)+'_final.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()




