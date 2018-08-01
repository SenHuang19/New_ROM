import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import sys
import numpy as np
regr = linear_model.LinearRegression()
import json
import collections
from collections import OrderedDict
import itertools as it
import math


#read data
filename='zone5'
info = json.load(open(filename))

tab=pd.read_csv(filename+'rawdata.csv')

zones=[]
for key in sorted(info["inputs"]["zones"]):
    zones.append(info["inputs"]["zones"][key])
    
adjzones=[]
for key in sorted(info["inputs"]["adjzones"]):
    adjzones.append(info["inputs"]["adjzones"][key])


#training data
tab_train=tab.loc[:7000]
tab_train.to_csv(filename+'train.csv')

#testing data
tab_test=tab.loc[7000:]

tab_test.to_csv(filename+'validation.csv')

#train the model
tab=pd.read_csv(filename+'train.csv')

#tabx=tab.loc[tab['gas'] >0]

#x=zip(tab['tout'],tab['PLRs'],tab['hourindex']) 

z=[]
z.append(tab['tout'][:-1])
z.append(tab['s'][:-1])
z.append(tab['i'][:-1])
z.append(tab['t1'][:-1])
z.append(tab['t2'][:-1])
z.append(tab['t3'][:-1])
z.append(tab['m'][:-1])      
#z.append(tab['tret'][:-1])


y=it.izip_longest(*z)

x=[]
for item in y:
   x.append(item)


#x=zip(tab['tout'][1:],tab['s'][1:],tab['i'][1:],tab['t1'][:-1],tab['w1'][1:],tab['hsp'][1:],tab['csp0'][1:],tab['csp1'][1:],tab['csp2'][1:],tab['csp3'][1:],tab['csp4'][1:],tab['m0'][1:],tab['m1'][1:],tab['m2'][1:],tab['m3'][1:],tab['m4'][1:],tab['rh0'][1:],tab['rh1'][1:],tab['rh2'][1:],tab['rh3'][1:],tab['rh4'][1:]) 
y=tab['t1'][1:]
regr.fit(x, y)
y_pre1=regr.predict(x)

tab2=pd.DataFrame()
tab2['prediction']=y_pre1
tab2['real']=y
tab2.to_csv(filename+'comparison.csv')

#validate the model

tab=pd.read_csv(filename+'validation.csv')
pred=[]
test=[]
t=[tab['t1'][0]]
for i in range(len(tab)-1):
    z=[]
    x=[]
    
    z.append(tab['tout'][i:i+1])
    z.append(tab['s'][i:i+1])
    z.append(tab['i'][i:i+1])
    z.append(t)
    z.append(tab['t2'][i:i+1])
    z.append(tab['t3'][i:i+1])
    z.append(tab['m'][i:i+1])
#    z.append(tab['tret'][i:i+1])
    """
    z.append(tab['tout'][i+1:i+2])
    z.append(tab['s'][i+1:i+2])
    z.append(tab['i'][i+1:i+2])
    z.append(t)
    for j in range(len(adjzones)):
        z.append(tab['t'+str(j+2)][i+1:i+2])
    z.append(tab['sp0'][i+1:i+2])
    z.append(tab['m'][i+1:i+2])
    z.append(tab['rh'][i+1:i+2])
    """
    k=it.izip_longest(*z)
    for item in k:
        x.append(item)
    #x=zip(tab['tout'][i+1:i+2],tab['s'][i+1:i+2],tab['i'][i+1:i+2],t,tab['w1'][i+1:i+2],tab['hsp'][1:],tab['csp'][i+1:i+2],m,rh)
    y_pre2=regr.predict(x)
    t=y_pre2
    pred.append(y_pre2[0])	
    test.append(tab['t1'][i+1])


tab3=pd.DataFrame()

tab3['prediction']=pred

tab3['real']=test

tab3.to_csv(filename+'validation_result.csv')

coefs=collections.OrderedDict()
coefs['a0']=regr.intercept_ 
for i in range(len(regr.coef_)):
   coefs['a'+str(i+1)]=regr.coef_[i]
print coefs

with open(filename+'_result','w') as outfile:
      json.dump(coefs,outfile) 
      
# plotting the results
def rmse(x,y):
   sum=0
   for i in range(len(x)):
        sum=sum+(x.iloc[i]-y.iloc[i])*(x[i]-y[i])
   return math.sqrt(sum/len(x))


tab2=pd.read_csv(filename+'validation_result.csv')


x=np.arange(20,tab2['real'].max()+1)


plt.scatter(tab2['real'],tab2['prediction'],color='y')


plt.plot(x,x+2.0/9*5,label='2degF(RMSE:'+str(round(rmse(tab2['real'],tab2['prediction']), 3))+')',color='r')
plt.plot(x,x-2.0/9*5,color='r')

#plt.plot(x[7000:],tab[tout][7000:],label='testing data')

plt.xlabel('Real [degC]',fontsize=10)
plt.ylabel('Prediction [degC]',fontsize=10)
#plt.xticks(xnum,xlab)
plt.xlim(20,x[-1])
plt.ylim(20,x[-1])
plt.legend()
plt.savefig(filename+'validation.png',bbox_inches = 'tight',pad_inches = 1)
plt.show()
      
      
      
      