vars=['FirstStageCooling','SupplyFanStatus','CompressorCommand','OutdoorAirTemperature','ZoneTemperature','UnoccupiedCoolingTemperatureSetPoint','CoolingTemperatureSetPoint','DischargeAirTemperature']
timestring='%Y-%m-%d %H:%M:%S'
import pandas as pd
import time
from datetime import datetime
from dateutil import tz
import holidays

us_holidays = holidays.UnitedStates()

to_zone = tz.tzlocal()
from_zone = tz.tzutc()
 
i=0
for var in vars:
   if i==0:
       tab=pd.read_csv('temp/'+var+'.csv')

       print tab
#       tab['timestring']=tab['time'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone))
       tab['year']=tab['times'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone).year)
       tab['month']=tab['times'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone).month)
       tab['day']=tab['times'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone).day)
       tab['hour']=tab['times'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone).hour)
       tab['weekday']=tab['times'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone).weekday())
       tab['holiday']=tab['times'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone) in us_holidays)
       tab['times']=tab['times'].apply(lambda x:time.mktime(datetime.strptime(x.split('.')[0], timestring).timetuple()))
   else:
       tab2=pd.read_csv('temp/'+var+'.csv')

#       tab2['timestring']=tab2['time'].apply(lambda x:datetime.strptime(x.split('.')[0], timestring).replace(tzinfo=from_zone).astimezone(to_zone))
       tab2['times']=tab2['times'].apply(lambda x:time.mktime(datetime.strptime(x.split('.')[0], timestring).timetuple()))
       tab=tab.merge(tab2,how='inner',on=['times'])
   i=i+1
tab.to_csv('temp/raw_data.csv',index=False)
       
