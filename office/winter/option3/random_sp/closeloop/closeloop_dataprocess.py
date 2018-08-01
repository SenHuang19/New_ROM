import numpy as np
import pandas as pd
import json


    
#c1=['constant','tout','s','i','t1','t2','sp','m','rh']

#print len(c1)

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
tab=pd.read_csv('zone4-1validation.csv')
sum = [[0 for x in range(len(tab))] for y in range(5)] 
for i in range(4):
    coe=json.load(open('zone4-'+str(i+1)+'_result'))
    print(len(coe))
    tab=pd.read_csv('zone4-'+str(i+1)+'validation.csv')
    sum[i]=coe['a0']+coe['a1']*tab['tout']+coe['a2']*tab['s']+coe['a3']*tab['i']+coe['a9']*tab['sp']+coe['a10']*tab['m']+coe['a11']*tab['rh']

coe=json.load(open('zone4-5_result'))
print(len(coe))
tab=pd.read_csv('zone4-5validation.csv')
sum[4]=coe['a0']+coe['a1']*tab['tout']+coe['a2']*tab['s']+coe['a3']*tab['i']+coe['a10']*tab['sp']+coe['a11']*tab['m']+coe['a12']*tab['rh']


#sum41=coe41['a0']+coe41['a1']*tab['tout']+coe41['a2']*tab['s']+coe41['a3']*tab['i']+coe41['a9']*tab['sp']+coe41['a10']*tab['m']+coe41['a11']*tab['rh']
#for i in range(len(coe4)-1):
#    sum4=sum4+coe4['a'+str(i+1)]*tab4[c1[i+1]]
#sum4=sum4+coe4['a0']*len(tab4)


tab5=pd.read_csv('zone5validation.csv')
coe5=json.load(open('zone5_result'))
print(len(coe5))
sum5=[0]*len(tab5)
sum5=coe5['a0']+coe5['a1']*tab5['tout']+coe5['a2']*tab5['s']+coe5['a3']*tab5['i']+coe5['a10']*tab5['m']
#sum5=[0]*len(tab5)
#for i in range(len(coe5)-1):
#    sum5=sum5+coe5['a'+str(i+1)]*tab5[c1[i+1]]
#sum5=sum5+coe5['a0']*len(tab5)




tab=pd.DataFrame()
  
for i in range(5):
    tab['b'+str(i)]=sum[i]

tab['b5']=sum5


tab.to_csv('b.csv')

tab=pd.read_csv('zone4-1validation.csv')
tab1=pd.read_csv('zone4-3validation.csv')
tab2=pd.DataFrame()

tab2['t41']=tab['t1']
tab2['t42']=tab['t2']
tab2['t43']=tab1['t1']
tab2['t44']=tab['t3']
tab2['t45']=tab['t4']
tab2['t5']=tab['t5']


tab2.to_csv('x0.csv')

