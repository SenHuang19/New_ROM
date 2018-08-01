import numpy as np
import pandas as pd
import json


#coe1=json.load(open('zone1_result'))
#coe2=json.load(open('zone2_result'))
#coe3=json.load(open('zone3_result'))
coe4=json.load(open('zone4_result'))
coe5=json.load(open('zone5_result'))
#coe6=json.load(open('zone6_result'))
#coe7=json.load(open('zone7_result'))

    
c1=['constant','tout','s','i','t1','t2','sp0','m','rh']

print len(coe4)
print len(coe5)
print len(c1)

"""
tab1=pd.read_csv('zone4-1validation.csv')

sum1=[0]*len(tab1)
for i in range(len(coe1)-1):
    sum1=sum1+coe1['a'+str(i+1)]*tab1[c1[i+1]]
sum1=sum1+coe1['a0']*len(tab1)


#c2=['Tout','s','i','hsp','csp0','csp1','csp2','csp3','csp4','csp5','m0','m1','m2','m3','m4','m5','rh0','rh1','rh2','rh3','rh4','rh5']
tab2=pd.read_csv('zone4-2validation.csv')

sum2=[0]*len(tab2)
for i in range(len(coe2)-1):
    sum2=sum2+coe2['a'+str(i+1)]*tab2[c1[i+1]]
sum2=sum2+coe2['a0']*len(tab2)


#c3=['Tout','s','i','hsp','csp0','csp1','csp2','m0','m1','m2','rh0','rh1','rh2']
tab3=pd.read_csv('zone4-3validation.csv')

sum3=[0]*len(tab3)
for i in range(len(coe3)-1):
    sum3=sum3+coe3['a'+str(i+1)]*tab3[c1[i+1]]
sum3=sum3+coe3['a0']*len(tab3)
"""

#c4=['Tout','s','i','hsp','csp0','m0','rh0']
tab4=pd.read_csv('zone4validation.csv')

sum4=[0]*len(tab4)
sum4=coe4['a0']+coe4['a1']*tab4['tout']+coe4['a2']*tab4['s']+coe4['a3']*tab4['i']+coe4['a6']*tab4['sp']+coe4['a7']*tab4['m']+coe4['a8']*tab4['rh']
#for i in range(len(coe4)-1):
#    sum4=sum4+coe4['a'+str(i+1)]*tab4[c1[i+1]]
#sum4=sum4+coe4['a0']*len(tab4)


tab5=pd.read_csv('zone5validation.csv')

sum5=[0]*len(tab5)
sum5=coe5['a0']+coe5['a1']*tab5['tout']+coe5['a2']*tab5['s']+coe5['a3']*tab5['i']+coe5['a6']*tab5['m']
#sum5=[0]*len(tab5)
#for i in range(len(coe5)-1):
#    sum5=sum5+coe5['a'+str(i+1)]*tab5[c1[i+1]]
#sum5=sum5+coe5['a0']*len(tab5)




tab=pd.DataFrame()
"""    
tab['b1']=sum1

tab['b2']=sum2

tab['b3']=sum3
"""
tab['b4']=sum4

tab['b5']=sum5


tab.to_csv('b.csv')


tab2=pd.DataFrame()

#tab2['t1']=tab1['t1']
#tab2['t2']=tab2['t1']
#tab2['t3']=tab3['t1']
tab2['t4']=tab4['t1']
tab2['t5']=tab5['t1']


tab2.to_csv('x0.csv')

