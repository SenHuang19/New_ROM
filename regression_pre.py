import pandas as pd
import itertools
import os
import numpy as np
from scipy.stats.stats import pearsonr
import sys

if not os.path.exists('p_test'):
    os.makedirs('p_test')


num=int(sys.argv[1])

train=pd.read_csv('train_raw.csv')

train=train.groupby(np.arange(len(train))//num).mean()

gp=train.groupby('day')
i=1
for name,group in gp:
    if i==1:
        on=group['CompressorCommand'][:-1].values
        t=group['ZoneTemperature'][1:].values     
        tout=group['OutdoorAirTemperature'][:-1].values
        tdis=group['DischargeAirTemperature'][:-1].values
        t_pre=group['ZoneTemperature'][:-1].values
        weekday=group['weekday'][:-1].values
        hour=group['hour'][:-1].values
    else:
        on=itertools.chain(on,group['CompressorCommand'][:-1].values)
        t=itertools.chain(t,group['ZoneTemperature'][1:].values)     
        tout=itertools.chain(tout,group['OutdoorAirTemperature'][:-1].values)
        tdis=itertools.chain(tdis,group['DischargeAirTemperature'][:-1].values)
        t_pre=itertools.chain(t_pre,group['ZoneTemperature'][:-1].values)
        weekday=itertools.chain(weekday,group['weekday'][:-1].values)
        hour=itertools.chain(hour,group['hour'][:-1].values)
    i=i+1

tab=pd.DataFrame()
tab['on']=list(on)
tab['t']=list(t)
tab['tout']=list(tout)
tab['tdis']=list(tdis)
tab['t_pre']=list(t_pre)
tab['hour']=list(hour)
tab['weekday']=list(weekday)
p_out=pearsonr(tab['t'],tab['tout'])[0]
p_hvac=pearsonr(tab['t'],tab['on'])[0]
p_t=pearsonr(tab['t'],tab['t_pre'])[0]

f=open('p_test/p_train.csv','a')
f.writelines(str(num)+','+str(p_out)+','+str(p_hvac)+','+str(p_t)+'\n')
f.close()

tab.to_csv('p_test/train'+str(num)+'.csv',index=False)


test=pd.read_csv('test_raw.csv')
print len(test)
test=test.groupby(np.arange(len(test))//num).mean()
print len(test)

gp=test.groupby('day')
i=1

for name,group in gp:
    if i==1:
        on=group['CompressorCommand'][:-1].values
        t=group['ZoneTemperature'][1:].values     
        tout=group['OutdoorAirTemperature'][:-1].values
        t_pre=group['ZoneTemperature'][:-1].values
        hour=group['hour'][:-1].values
        weekday=group['weekday'][:-1].values
        times=group['times'][:-1].values
    else:
        on=itertools.chain(on,group['CompressorCommand'][:-1].values)
        t=itertools.chain(t,group['ZoneTemperature'][1:].values)     
        tout=itertools.chain(tout,group['OutdoorAirTemperature'][:-1].values)
        t_pre=itertools.chain(t_pre,group['ZoneTemperature'][:-1].values)
        hour=itertools.chain(hour,group['hour'][:-1].values)
        weekday=itertools.chain(weekday,group['weekday'][:-1].values)
        times=itertools.chain(times,group['times'][:-1].values)
    i=i+1

tab=pd.DataFrame()
tab['on']=list(on)
tab['t']=list(t)
tab['tout']=list(tout)
tab['t_pre']=list(t_pre)
tab['hour']=list(hour)
tab['weekday']=list(weekday)
tab['times']=list(times)
p_out=pearsonr(tab['t'],tab['tout'])[0]
p_hvac=pearsonr(tab['t'],tab['on'])[0]
p_t=pearsonr(tab['t'],tab['t_pre'])[0]

p_out=pearsonr(tab['t'],tab['tout'])[0]
p_hvac=pearsonr(tab['t'],tab['on'])[0]
p_t=pearsonr(tab['t'],tab['t_pre'])[0]

f=open('p_test/p_test.csv','a')
f.writelines(str(num)+','+str(p_out)+','+str(p_hvac)+','+str(p_t)+'\n')
f.close()
tab.to_csv('p_test/test'+str(num)+'.csv',index=False)
  

