import pandas as pd
import os

if not os.path.exists('holidays'):
    os.makedirs('holidays')

if not os.path.exists('weekdays'):
    os.makedirs('weekdays')

tab=pd.read_csv('temp/raw_data.csv')

names=list(tab.columns.values)

gp=tab.groupby('holiday')

for name,group in gp:
    if name:
        group.to_csv('holidays/'+'raw_data.csv')
    else:
        tab=group

gp2=tab.groupby('weekday')
for name,group in gp2:
    if int(name)==0:
        temp=group
    if int(name)<5:
        temp=temp.merge(group,how='outer',on=names)
temp=temp.sort_values('times')
temp.to_csv('weekdays/'+'raw_data.csv',index=False)