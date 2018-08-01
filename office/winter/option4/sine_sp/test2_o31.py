# -*- coding: utf-8 -*-
import numpy as np
import linsolver as lin
import pandas as pd
import json
import math
import matplotlib.pyplot as plt


coe1=json.load(open('zone1_result'))
coe2=json.load(open('zone2_result'))
coe5=json.load(open('zone5_result'))

A=np.array([[1,-coe1['a5'],-coe1['a6']],
            [-coe2['a5'],1,-coe2['a6']],
            [-coe5['a5'],-coe5['a6'],1]])

b0=np.array([coe1['a4'],coe2['a4'],coe5['a4']])



#dt = 60
whole=pd.read_csv('b.csv')
print len(whole)
#tab1=whole.loc[:1026]
#tab2=whole.loc[1026:]
#num1=len(tab1)-1
#print num1
#num2=len(tab2)-1
#print num2

result=''

#initialization: temperatures at last time step
initial=pd.read_csv('x0.csv')

"""
for j in range(0,1928,288):
    print "simulation starts at day " + str(j/288+1)
    tab=whole.loc[j:j+288]
    num=len(tab)-1
    print num
    x0=np.array([initial['t1'].iloc[j],initial['t2'].iloc[j],initial['t3'].iloc[j],initial['t4'].iloc[j],initial['w1-2'].iloc[j],initial['w1-3'].iloc[j],initial['w1-4'].iloc[j],initial['w2-3'].iloc[j],initial['w2-4'].iloc[j]])
    print x0
    b=np.array([[tab['b1'].iloc[1],tab['b2'].iloc[1],tab['b3'].iloc[1],tab['b4'].iloc[1],tab['b5'].iloc[1],tab['b6'].iloc[1],tab['b7'].iloc[1],tab['b8'].iloc[1],tab['b9'].iloc[1]]])
    
    for i in range(2,len(tab)):
        temp=np.array([[tab['b1'].iloc[i],tab['b2'].iloc[i],tab['b3'].iloc[i],tab['b4'].iloc[i],tab['b5'].iloc[i],tab['b6'].iloc[i],tab['b7'].iloc[i],tab['b8'].iloc[i],tab['b9'].iloc[i]]])
        b=np.concatenate((b, temp))

    equation = lin.solveDynamic(A,b,b0,num,x0=x0)
    equation.Dysolve()
    result = result + equation.result

"""
#reinitialization
tab2=pd.read_csv('b.csv')
b=np.array([[tab2['b1'].iloc[0],tab2['b2'].iloc[0],tab2['b5'].iloc[0]]])
x0=np.array([initial['t1'].iloc[0],initial['t2'].iloc[0],initial['t5'].iloc[0]])
for i in range(1,len(tab2)):
     temp=np.array([[tab2['b1'].iloc[i],tab2['b2'].iloc[i],tab2['b5'].iloc[i]]])
     #print temp
     b=np.concatenate((b, temp))

num=len(tab2)
equation2 = lin.solveDynamic(A,b,b0,num, x0=x0)

equation2.Dysolve()
result = result+equation2.result


f=open('result.csv','w')
f.writelines(result)
f.close()


# RMSE
# plotting the results
def rmse(x,y):
   sum=0
   for i in range(len(x)-1):
        sum=sum+(x[i]-y[i])*(x[i]-y[i])
   return math.sqrt(sum/(len(x)-1))

colnames=['t1','t2','t5'] 
tab = pd.read_csv('result.csv',index_col=False,names=colnames, header=None)

x=np.arange(len(tab['t1']))   

for i in range(2):
    plt.plot(x,initial['t'+str(i+1)],label='Zone4-'+str(i+1)+'real',color='r')   
    plt.plot(x,tab['t'+str(i+1)],label='Zone4-'+str(i+1)+' predicted',color='b')   

    plt.legend()
    plt.xlabel('Timestep',fontsize=10)
    plt.ylabel('Predicted Temperature [degC]',fontsize=10) 
    plt.savefig('zone4-'+str(i+1)+'timestep_cl.png',bbox_inches = 'tight',pad_inches = 1)     
    plt.show()


x=np.arange(20,initial['t1'].max()+1)

for i in range(2):
    plt.scatter(initial['t'+str(i+1)],tab['t'+str(i+1)],label='Zone4-'+str(i+1)+' close loop RMSE:'+str(round(rmse(initial['t'+str(i+1)],tab['t'+str(i+1)]), 3))+')',color='y')
#plt.scatter(initial['t5'],tab['t5'],label='option3 RMSE:'+str(round(rmse(tab2['t1'],option3), 3))+')',color='y')

    plt.plot(x,x+2.0/9*5,color='r')
    plt.plot(x,x-2.0/9*5,color='r')

    plt.xlabel('Real [degC]',fontsize=10)
    plt.ylabel('Prediction [degC]',fontsize=10)
    plt.xlim(20,x[-1])
    plt.ylim(20,x[-1])
    plt.legend()
    plt.savefig('zone4-'+str(i+1)+'validation_cl.png',bbox_inches = 'tight',pad_inches = 1)  
    plt.show()

