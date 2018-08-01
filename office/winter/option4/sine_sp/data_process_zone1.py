import pandas as pd
import json

filename='zone1'
info = json.load(open(filename))

tab=pd.read_csv('eplusout.csv')

# solar radiation	
sol=[]
for key in info["solar"]:
    sol.append(info["solar"][key])

# zone information
zones=[]
for key in sorted(info["inputs"]["zones"]):
    zones.append(info["inputs"]["zones"][key])

adjzones=[]
for key in sorted(info["inputs"]["adjzones"]):
    adjzones.append(info["inputs"]["adjzones"][key])
    
# terminal information
termoutlet=[]
for key in sorted(info["inputs"]["termoutlet"]):
    termoutlet.append(info["inputs"]["termoutlet"][key])
    
# RHT information
rhtinlet=[]
for key in sorted(info["inputs"]["rhtinlet"]):
    rhtinlet.append(info["inputs"]["rhtinlet"][key])

rhtoutlet=[]
for key in sorted(info["inputs"]["rhtoutlet"]):
    rhtoutlet.append(info["inputs"]["rhtoutlet"][key])    



"""
# wall information
walls=[]
for key in sorted(info["inputs"]["walls"]):
    walls.append(info["inputs"]["walls"][key])

wallareas=[]
for key in info["inputs"]["wallarea"]:
    wallareas.append(info["inputs"]["wallarea"][key])

i=1
for key2 in info["inputs"]["walls"]:
    tab['w'+str(i)]=[0]*len(tab)
    temp=[]
    area=0
    for key in info["inputs"]["walls"][key2]:
          tab['w'+str(i)]=tab['w'+str(i)]+(tab[info["inputs"]["walls"][key2][key].upper()+
             ':Surface Inside Face Temperature [C](TimeStep)']+tab[info["inputs"]["walls"][key2][key].upper()+
                                               ':Surface Outside Face Temperature [C](TimeStep)'])/2*(info["inputs"]["wallarea"][key2][key])
          area=area+info["inputs"]["wallarea"][key2][key]
    tab['w'+str(i)]=tab['w'+str(i)]/area
    i=i+1
"""                            


tout=info["tout"]
#hsp=info["hsp"]


zmt=[]
adjt=[]
zmdm=[] # zone supply air flow rate
zmdt=[] # zone supply air temperature
int=[] # internal load
inlet=[] # reheat coil inlet water temperature
outlet=[] # reheat coil outlet water temperature
mrh=[] # reheat coil water mass flow rate
#rh=[]
#sol=['Environment:Site Diffuse Solar Radiation Rate per Area [W/m2](TimeStep)','Environment:Site Direct Solar Radiation Rate per Area [W/m2](TimeStep)']
for i in range(len(zones)):
    zmt.append(str(zones[i]).upper()+':Zone Mean Air Temperature [C](TimeStep)')
    int.append(str(zones[i]).upper()+':Zone Total Internal Total Heating Rate [W](TimeStep)')
    zmdm.append(str(termoutlet[i]).upper()+':System Node Mass Flow Rate [kg/s](TimeStep)')
    zmdt.append(str(termoutlet[i]).upper()+'System Node Temperature [C](TimeStep)')
    inlet.append(str(rhtinlet[i]).upper()+':System Node Temperature [C](TimeStep)')
    outlet.append(str(rhtoutlet[i]).upper()+':System Node Temperature [C](TimeStep)')
    mrh.append(str(rhtoutlet[i]).upper()+':System Node Mass Flow Rate [kg/s](TimeStep)')
    #rh.append(str(zones[i]).upper()+' RHT COIL:Heating Coil Heating Rate [W](TimeStep)')
for i in range(len(adjzones)):
    adjt.append(str(adjzones[i]).upper()+':Zone Mean Air Temperature [C](TimeStep)')

tab['t1']=[0]*len(tab)
tab['m1']=[0]*len(tab)
tab['i']=[0]*len(tab)
tab['s']=[0]*len(tab)
tab['rh']=[0]*len(tab)

for i in range(len(zones)):
    tab['t1']=tab['t1']+tab[zmt[i]]*tab[zmdm[i]]
    tab['i']=tab['i']+tab[int[i]]
    tab['m1']=tab['m1']+tab[zmdm[i]]
    tab['rh']=tab['rh']+tab[mrh[i]]*(tab[inlet[i]]-tab[outlet[i]])*4200


for i in range(len(sol)):	
    tab['s']=tab['s']+tab[sol[i]]	
	
	
tab2=pd.DataFrame()

#for j in range(len(walls)):
#    tab2['w'+str(j)]=tab['w'+str(j+1)]
tab2['tout']=tab[tout]
tab2['s']=tab['s']
tab2['i']=tab['i']
tab2['t1']=tab['t1']/tab['m1']
# for cav system
if tab['m1'][0]==0:
    tab2['t1']=tab[zmt[0]]

for i in range(len(adjzones)):
    name='t'+str(i+2)
    tab2[name]=tab[adjt[i]]

temp=[0]*len(tab)
for i in range(len(zones)):
    name='sp'+str(i)
    tab2[name]=tab[str(zones[i]).upper()+':Zone Thermostat Heating Setpoint Temperature [C](TimeStep)']
    temp=temp+tab2[name]

tab2['sp']=temp/len(zones)
tab2['m']=tab['m1']
tab2['rh']=tab['rh']


tab2.to_csv(filename+'rawdata.csv')
