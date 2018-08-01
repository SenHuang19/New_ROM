# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 09:42:00 2018

@author: wang759
"""
from operator import itemgetter
import csv

def infoOffice(file_name):
    # read the idf file
    lines = list(open(file_name))
    
    # search the information of air distribution unit
    # ZoneHVAC:AirDistributionUnit
    ADU_data = []# record the information of ADU
    for ind,val in enumerate(lines):
        if '!' not in val and 'ZoneHVAC:AirDistributionUnit,' in val:
            ####################################################
            # search the name of the material
            # search the line index for the name of the material
            k = ind
            for i in range(ind,ind+20):
                if '!- Name' in lines[i]:
                    k = i
                    break
            ind_name = 0# index of the ',' after the name
            for ind1,val1 in enumerate(lines[k]):
                if val1 == ',' or val1 == ';':
                    ind_name = ind1
                    break
            name = lines[k][2:ind_name]
            ####################################################
            # search the roughness
            # search the line index for the roughness
            k = ind
            for i in range(ind,ind+20):
                if '!- Air Distribution Unit Outlet Node Name' in lines[i]:
                    k = i
                    break
            ind_node = 0# index of the ',' after the roughness
            for ind2,val2 in enumerate(lines[k]):
                if val2 == ',' or val2 == ';':
                    ind_node = ind2
                    break
            node = lines[k][2:ind_node]
            ####################################################

            ADU_data.append([name,node])    
            
    # search the information of reheat coil
    # Coil:Heating:Water
    RHT_data = []# record the information of RHT coil
    for ind,val in enumerate(lines):
        if '!' not in val and 'Coil:Heating:Water,' in val:
            ####################################################
            # search the name of the material
            # search the line index for the name of the material
            k = ind
            for i in range(ind,ind+20):
                if '!- Name' in lines[i]:
                    k = i
                    break
            ind_name = 0# index of the ',' after the name
            for ind1,val1 in enumerate(lines[k]):
                if val1 == ',' or val1 == ';':
                    ind_name = ind1
                    break
            name = lines[k][2:ind_name]
            ####################################################
            # search the roughness
            # search the line index for the roughness
            k = ind
            for i in range(ind,ind+20):
                if '!- Water Inlet Node Name' in lines[i]:
                    k = i
                    break
            ind_node = 0# index of the ',' after the roughness
            for ind2,val2 in enumerate(lines[k]):
                if val2 == ',' or val2 == ';':
                    ind_node = ind2
                    break
            inlet_node = lines[k][2:ind_node]
            ####################################################
            # search the roughness
            # search the line index for the roughness
            k = ind
            for i in range(ind,ind+20):
                if '!- Water Outlet Node Name' in lines[i]:
                    k = i
                    break
            ind_node = 0# index of the ',' after the roughness
            for ind2,val2 in enumerate(lines[k]):
                if val2 == ',' or val2 == ';':
                    ind_node = ind2
                    break
            outlet_node = lines[k][2:ind_node]
            ####################################################

            RHT_data.append([name,outlet_node,inlet_node])    
            
    # search the information of plenum
    # Coil:Heating:Water
    PLE_data = []# record the information of RHT coil
    for ind,val in enumerate(lines):
        if '!' not in val and 'AirLoopHVAC:ReturnPlenum,' in val:
            ####################################################
            # search the name of the material
            # search the line index for the name of the material
            k = ind
            for i in range(ind,ind+20):
                if '!- Zone Name' in lines[i]:
                    k = i
                    break
            ind_name = 0# index of the ',' after the name
            for ind1,val1 in enumerate(lines[k]):
                if val1 == ',' or val1 == ';':
                    ind_name = ind1
                    break
            name = lines[k][2:ind_name]
            ####################################################
            # search the roughness
            # search the line index for the roughness
            k = ind
            for i in range(ind,ind+20):
                if '!- Outlet Node Name' in lines[i]:
                    k = i
                    break
            ind_node = 0# index of the ',' after the roughness
            for ind2,val2 in enumerate(lines[k]):
                if val2 == ',' or val2 == ';':
                    ind_node = ind2
                    break
            outlet_node = lines[k][2:ind_node]
            ####################################################

            PLE_data.append([name,outlet_node])    
    

    ADU_data.extend(RHT_data)
    ADU_data.extend(PLE_data)
    return ADU_data

# test
# get the surface data from the two files calculated by EnergyPlus and OpenStudio 
office_data = infoOffice('./B_Office_20180716.idf')

    
# record the results into csv file
with open('office_data.csv','wb') as csvfile:
    data = csv.writer(csvfile, delimiter=',')
    data.writerow(['component_name','outlet_node_name','inlet_node_name'])
    for row in office_data:
        data.writerow(row)
