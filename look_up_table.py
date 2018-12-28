import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

xtic=[]
xlab=[]

for i in range(0,24,2):
	 xtic.append(i*60)
	 xlab.append(str(i+7)+':00')


for i in range(0,24,2):
	 xtic.append(i*60+1440)
	 xlab.append(str(i)+':00')


train=pd.read_csv('train.csv')
dis_interval=1
train['tou_dis']=train['tout'].apply(lambda x: x // dis_interval)
train['t_pre_dis']=train['t_pre'].apply(lambda x: x // dis_interval)

gp=train.groupby(['hour','tou_dis','t_pre_dis','on'])

on=[]
hour=[]
tou_dis=[]
t_pre_dis=[]
t_value=[]
for name,group in gp:
     hour.append(name[0])
     on.append(name[3])
     t_pre_dis.append(name[2])
     tou_dis.append(name[1])
     t_value.append(float(group['t'].mean()))

look_up_tab=pd.DataFrame()

look_up_tab['on']=on
look_up_tab['hour']=hour
look_up_tab['t_pre_dis']=t_pre_dis
look_up_tab['tou_dis']=tou_dis
look_up_tab['t_value']=t_value

look_up_tab.to_csv('look_up_tab.csv',index=False)



test=pd.read_csv('test.csv')
test=test[60*7:18*60]
y_real=test['t']
y_predict=[]
t_value=test['t_pre'].iloc[0]
for i in range(len(test)):
   temp=test[i:i+1]

   temp['t_pre']=[t_value]
   temp['tou_dis']=temp['tout'].apply(lambda x: x // dis_interval)
   temp['t_pre_dis']=temp['t_pre'].apply(lambda x: x // dis_interval)
#   print temp
   result=pd.merge(temp,look_up_tab,how='left',on=['on','hour','t_pre_dis','tou_dis'])
   if not math.isnan(result['t_value'].iloc[0]):
         t_value=result['t_value'].iloc[0]
#   print t_value
   y_predict.append(t_value)


xx=np.arange(len(y_real))
plt.plot(xx,y_real,label='real',color='r')
plt.plot(xx,y_predict,label='predict')
plt.xticks(xtic,xlab,rotation=45)
plt.xlim(xx[0],xx[-1])
plt.ylabel('Zone Temp ['+'$^{o}F$'+']')
plt.xlabel('Time [hour:minute]')
plt.legend(loc='best')
plt.savefig('LookTab.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()
