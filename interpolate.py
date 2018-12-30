vars=['FirstStageCooling','SupplyFanStatus','CompressorCommand','OutdoorAirTemperature','ZoneTemperature','UnoccupiedCoolingTemperatureSetPoint','CoolingTemperatureSetPoint','DischargeAirTemperature']
timestring='%Y-%m-%d %H:%M:%S'
import pandas as pd
import time
from datetime import datetime
from dateutil import tz
import holidays
import numpy as np
import os
if not os.path.exists('temp'):
    os.makedirs('temp')

source='source_data'

us_holidays = holidays.UnitedStates()

for var in vars:
       print var
       tab=pd.read_csv(source+'/'+var+'.csv')
       tab.columns = ['time',var]
       tab['timestamp']=tab['time'].apply(lambda x:time.mktime(datetime.strptime(x.split('.')[0], timestring).timetuple()))
       print tab['timestamp'].iloc[-1] 
       timerange=np.arange(tab['timestamp'].iloc[0],tab['timestamp'].iloc[-1]+60,60)
       print timerange[-1] 
       temp=pd.DataFrame()
       temp['timestamp']=timerange
       temp['times']=temp['timestamp'].apply(lambda x:datetime.fromtimestamp(int(x)).strftime(timestring))
       tab=tab.merge(temp,how='outer',on=['timestamp'])
       temp=pd.DataFrame()
       temp['timestamp']=timerange
       tab=tab.merge(temp,how='inner',on=['timestamp'])

       tab=tab.sort_values('timestamp')
       tab[var]=tab[var].interpolate()
       tab[var]=tab[var].apply(lambda x:0 if x<1 else x)
       tab=tab.drop(['time','timestamp'], axis=1)
       tab.to_csv('temp/'+var+'.csv',index=False)



       
