import pandas as pd

tab=pd.read_csv('weekdays/'+'raw_data.csv')

names=list(tab.columns.values)

gp=tab.groupby('day')

num= len(gp)

i=1

for name,group in gp:
    print name
    if i==1:
        train=group
    if i==num-2:
        test=group

    if i<num-1:
        train=train.merge(group,how='outer',on=names)
    if i>=num-2 and i<num-1:
        test=test.merge(group,how='outer',on=names)
    i=i+1
train.to_csv('train_raw.csv',index=False)
test.to_csv('test_raw.csv',index=False)