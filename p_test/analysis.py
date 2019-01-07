import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr
import sys

tab=pd.read_csv('train1.csv')

num=int(sys.argv[1])
on=[]
t=[]
tout=[]
t_pre=[]

for i in range(num,len(tab)-num):
    on.append(tab['on'].iloc[i-num])
    tout.append(tab['tout'].iloc[i-num])
    t_pre.append(tab['t_pre'].iloc[i-num])
    t.append(tab['t_pre'].iloc[i])    

print pearsonr(t,tout)[0]
print pearsonr(t,on)[0]
print pearsonr(t,t_pre)[0]
                        


