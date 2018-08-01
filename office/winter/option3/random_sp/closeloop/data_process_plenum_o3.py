import pandas as pd
import json

filename='zone5'
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
    zmdt.append(str(termoutlet[i]).upper()+':System Node Temperature [C](TimeStep)')
#    inlet.append(str(rhtinlet[i]).upper()+':System Node Temperature [C](TimeStep)')
#    outlet.append(str(rhtoutlet[i]).upper()+':System Node Temperature [C](TimeStep)')
#    mrh.append(str(rhtoutlet[i]).upper()+':System Node Mass Flow Rate [kg/s](TimeStep)')
    #rh.append(str(zones[i]).upper()+' RHT COIL:Heating Coil Heating Rate [W](TimeStep)')
for i in range(len(adjzones)):
    adjt.append(str(adjzones[i]).upper()+':Zone Mean Air Temperature [C](TimeStep)')

tab['t1']=[0]*len(tab)
tab['m1']=[0]*len(tab)
tab['i']=[0]*len(tab)
tab['s']=[0]*len(tab)
tab['adjt']=[0]*len(tab)

for i in range(len(zones)):
    tab['t1']=tab['t1']+tab[zmt[i]]*tab[zmdm[i]]
    tab['i']=tab['i']+tab[int[i]]
    tab['m1']=tab['m1']+tab[zmdm[i]]

for i in range(len(adjzones)):
    tab['adjt']=tab['adjt']+tab[adjt[i]]

for i in range(len(sol)):	
    tab['s']=tab['s']+tab[sol[i]]	
	

  

	
tab2=pd.DataFrame()

#for j in range(len(walls)):
#    tab2['w'+str(j)]=tab['w'+str(j+1)]
tab2['tout']=tab[tout]
tab2['s']=tab['s']
tab2['i']=tab['i']
tab2['t1']=tab['t1']/tab['m1']

# adjacent zone temperatures
for i in range(len(adjzones)):
    tab2['t'+str(i+2)]=tab[adjt[i]]
#tab2['t2']=tab['adjt']/5
#for i in range(len(adjzones)):
#    name='t'+str(i+2)
#    tab2[name]=tab[adjt[i]]


tab2['m']=tab[zmdm[0]]
tab2['tret']=tab[zmdt[0]]
    #name='rh'+str(i)
    #tab2[name]=tab[mrh[i]]*(tab[inlet[i]]-tab[outlet[i]])*4200
#tab2['rh']=tab['rh']



tab2.to_csv(filename+'rawdata.csv')
