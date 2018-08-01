import numpy as np
import pandas as pd
import json


coe1=json.load(open('zone1_result'))
coe2=json.load(open('zone2_result'))
coe5=json.load(open('zone5_result'))


    
#c1=['constant','tout','s','i','t1','t2','sp0','m','rh']

print len(coe1)
print len(coe2)
print len(coe5)
#print len(c1)


tab=pd.read_csv('zone1validation.csv')

sum1=[0]*len(tab)
sum1=coe1['a0']+coe1['a1']*tab['tout']+coe1['a2']*tab['s']+coe1['a3']*tab['i']+coe1['a7']*tab['sp']+coe1['a8']*tab['m']+coe1['a9']*tab['rh']
#for i in range(len(coe4)-1):
#    sum4=sum4+coe4['a'+str(i+1)]*tab4[c1[i+1]]
#sum4=sum4+coe4['a0']*len(tab4)

tab=pd.read_csv('zone2validation.csv')

sum2=[0]*len(tab)
sum2=coe2['a0']+coe2['a1']*tab['tout']+coe2['a2']*tab['s']+coe2['a3']*tab['i']+coe2['a7']*tab['sp']+coe2['a8']*tab['m']+coe2['a9']*tab['rh']


tab5=pd.read_csv('zone5validation.csv')

sum5=[0]*len(tab5)
sum5=coe5['a0']+coe5['a1']*tab5['tout']+coe5['a2']*tab5['s']+coe5['a3']*tab5['i']+coe5['a7']*tab5['m']
#sum5=[0]*len(tab5)
#for i in range(len(coe5)-1):
#    sum5=sum5+coe5['a'+str(i+1)]*tab5[c1[i+1]]
#sum5=sum5+coe5['a0']*len(tab5)




tab=pd.DataFrame()
  
tab['b1']=sum1

tab['b2']=sum2

tab['b5']=sum5


tab.to_csv('b.csv')


tab2=pd.DataFrame()
tab=pd.read_csv('zone1validation.csv')

tab2['t1']=tab['t1']
tab2['t2']=tab['t2']
tab2['t5']=tab5['t1']


tab2.to_csv('x0.csv')

