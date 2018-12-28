import pandas as pd
import itertools

train=pd.read_csv('train_raw.csv')
interval=5


gp=train.groupby('day')
i=1
for name,group in gp:
    if i==1:
        on=group['CompressorCommand'][:-interval].values
        t=group['ZoneTemperature'][interval:].values     
        tout=group['OutdoorAirTemperature'][:-interval].values
        t_pre=group['ZoneTemperature'][:-interval].values
        hour=group['hour'][:-interval].values
    else:
        on=itertools.chain(on,group['CompressorCommand'][:-interval].values)
        t=itertools.chain(t,group['ZoneTemperature'][interval:].values)     
        tout=itertools.chain(tout,group['OutdoorAirTemperature'][:-interval].values)
        t_pre=itertools.chain(t_pre,group['ZoneTemperature'][:-interval].values)
        hour=itertools.chain(hour,group['hour'][:-interval].values)
    i=i+1
print on
tab=pd.DataFrame()
tab['on']=list(on)
tab['t']=list(t)
tab['tout']=list(tout)
tab['t_pre']=list(t_pre)
tab['hour']=list(hour)
tab.to_csv('train_'+str(interval)+'.csv',index=False)



  

