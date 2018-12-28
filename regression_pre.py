import pandas as pd
import itertools

train=pd.read_csv('train_raw.csv')



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
        tset=group['weekday'][:-1].values
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
print on
tab=pd.DataFrame()
tab['on']=list(on)
tab['t']=list(t)
tab['tout']=list(tout)
tab['tdis']=list(tdis)
tab['t_pre']=list(t_pre)
tab['hour']=list(hour)
tab['weekday']=list(weekday)
tab.to_csv('train.csv',index=False)


test=pd.read_csv('test_raw.csv')



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
        tdis=group['DischargeAirTemperature'][:-1].values
    else:
        on=itertools.chain(on,group['CompressorCommand'][:-1].values)
        t=itertools.chain(t,group['ZoneTemperature'][1:].values)     
        tout=itertools.chain(tout,group['OutdoorAirTemperature'][:-1].values)
        t_pre=itertools.chain(t_pre,group['ZoneTemperature'][:-1].values)
        hour=itertools.chain(hour,group['hour'][:-1].values)
        weekday=itertools.chain(weekday,group['weekday'][:-1].values)
        times=itertools.chain(times,group['times'][:-1].values)
        tdis=itertools.chain(tdis,group['DischargeAirTemperature'][:-1].values)
    i=i+1
print on
tab=pd.DataFrame()
tab['on']=list(on)
tab['t']=list(t)
tab['tout']=list(tout)
tab['t_pre']=list(t_pre)
tab['hour']=list(hour)
tab['weekday']=list(weekday)
tab['times']=list(times)
tab['tdis']=list(tdis)
tab.to_csv('test.csv',index=False)
  
