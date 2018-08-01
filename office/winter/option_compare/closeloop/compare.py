# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 23:19:59 2018

@author: wang759
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

tab=pd.read_csv('compare.csv')
tab2=pd.read_csv('zone4validation.csv')

option1=tab['option1']

option3=[0]*len(tab['option1'])
for i in range(len(tab['option1'])):
    option3[i]=(tab['option3-1'][i]*tab['m1'][i]+tab['option3-2'][i]*tab['m2'][i]+tab['option3-3'][i]*tab['m3'][i]+tab['option3-4'][i]*tab['m4'][i]+tab['option3-5'][i]*tab['m5'][i])/(tab['m1'][i]+tab['m2'][i]+tab['m3'][i]+tab['m4'][i]+tab['m5'][i])
    
option4=[0]*len(tab['option1'])
for i in range(len(tab['option1'])):
    option4[i]=(tab['option4-1'][i]*(tab['m1'][i]+tab['m2'][i]+tab['m3'][i]+tab['m4'][i])+tab['option4-2'][i]*tab['m5'][i])/(tab['m1'][i]+tab['m2'][i]+tab['m3'][i]+tab['m4'][i]+tab['m5'][i])
        
    
x=np.arange(len(tab2['t1']))   

plt.plot(x,tab2['t1'],label='real',color='r') 
plt.plot(x,option1,label='option1',color='b')   
plt.plot(x,option4,label='option4',color='g')   
plt.plot(x,option3,label='option3',color='y') 

  
plt.legend()
plt.xlabel('Timestep',fontsize=10)
plt.ylabel('Predicted Temperature [degC]',fontsize=10)   
plt.savefig('timestep_cl.png',bbox_inches = 'tight',pad_inches = 1)   
plt.show()


# RMSE
# plotting the results
def rmse(x,y):
   sum=0
   for i in range(len(x)-1):
        sum=sum+(x[i]-y[i])*(x[i]-y[i])
   return math.sqrt(sum/(len(x)-1))

x=np.arange(20,tab2['t1'].max()+1)

plt.scatter(tab2['t1'],option1,label='option1 RMSE:'+str(round(rmse(tab2['t1'],option1), 3))+')',color='b')
plt.scatter(tab2['t1'],option4,label='option4 RMSE:'+str(round(rmse(tab2['t1'],option4), 3))+')',color='g')
plt.scatter(tab2['t1'],option3,label='option3 RMSE:'+str(round(rmse(tab2['t1'],option3), 3))+')',color='y')


plt.plot(x,x+2.0/9*5,color='r')
plt.plot(x,x-2.0/9*5,color='r')


plt.xlabel('Real [degC]',fontsize=10)
plt.ylabel('Prediction [degC]',fontsize=10)
plt.xlim(20,x[-1])
plt.ylim(20,x[-1])
plt.legend()
plt.savefig('validation_cl.png',bbox_inches = 'tight',pad_inches = 1)   
