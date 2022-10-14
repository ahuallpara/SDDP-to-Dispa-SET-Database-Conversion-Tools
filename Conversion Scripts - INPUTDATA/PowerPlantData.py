# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 08:59:55 2022

@author: navia
"""

import numpy as np
import pandas as pd
from functools import reduce



hydro = pd.read_csv('../BaseDatos_SDDP/chidrobo.csv', encoding='cp1252', header=0)
hydro = hydro[['...Nombre...','....Pot','.VMax..','.FPMed.']]
hydro = hydro.rename({'...Nombre...':'Unit','....Pot':'PowerCapacity'}, axis=1)	

thermo = pd.read_csv('../BaseDatos_SDDP/ctermibo.csv', encoding='cp1252', header=0)
thermo = thermo[['...Nombre...','.PotIns','Comb']]
thermo = thermo.rename({'...Nombre...':'Unit','.PotIns':'PowerCapacity','Comb':'Fuel'}, axis=1)	

vres = pd.read_csv('../BaseDatos_SDDP/cgndbo.csv', encoding='cp1252', header=0)
vres = vres[['Name','PotIns','!Num']]
vres = vres.rename({'Name':'Unit','PotIns':'PowerCapacity'}, axis=1)	

dbus = pd.read_csv('../BaseDatos_SDDP/dbus.csv', encoding='cp1252', header=1)
dbus = dbus[['Name','Gen. name']]
dbus = dbus.rename({'Gen. name':'Unit','Name':'Zone'}, axis=1)

##HIDRO

plthydro = pd.merge(hydro, dbus,  how="left", on=['Unit'])
plthydro['Technology'] = 'HDAM'
plthydro['Fuel'] = 'WAT'
plthydro['STOCapacity'] = (plthydro['.VMax..'] * plthydro['.FPMed.'] * 10000)/36
plthydro = plthydro.drop(['.VMax..','.FPMed.'], axis=1)
column_to_move = plthydro.pop('STOCapacity')
plthydro.insert(5, 'STOCapacity', column_to_move)
##sumar sto de los lagos a las plantas
cond1 = [
        plthydro['Unit'] == 'SIS',
        plthydro['Unit'] == 'COR',
        plthydro['Unit'] == 'KAN',
        plthydro['Unit'] == 'MIG',
        plthydro['Unit'] == 'ANG',
        plthydro['Unit'] == 'CHO',
        plthydro['Unit'] == 'CRB',
        plthydro['Unit'] == 'ZON',
        plthydro['Unit'] == 'TIQ',
        plthydro['Unit'] == 'BOT',
        plthydro['Unit'] == 'CUT',
        plthydro['Unit'] == 'SRO01',
        plthydro['Unit'] == 'SRO02',
        plthydro['Unit'] == 'SAI',
        plthydro['Unit'] == 'CHU',
        plthydro['Unit'] == 'HAR',
        plthydro['Unit'] == 'CAH',
        plthydro['Unit'] == 'HUA',
        plthydro['Unit'] == 'CHJ',
        plthydro['Unit'] == 'YAN',
        plthydro['Unit'] == 'KIL',
        plthydro['Unit'] == 'LAN',
        plthydro['Unit'] == 'PUH',
        plthydro['Unit'] == 'QUE',
        plthydro['Unit'] == 'SJA',
        plthydro['Unit'] == 'MIS',
        plthydro['Unit'] == 'SJS',
        plthydro['Unit'] == 'SJE',
        plthydro['Unit'] == 'UMA',
        plthydro['Unit'] == 'PLD',
        plthydro['Unit'] == 'SEH',
        plthydro['Unit'] == 'JUN',
        plthydro['Unit'] == 'CON'
    ]
opt20 = [153.73,193002.74,309.72,2732.94,13566.64,103.74,1382.71,3121,7716.32,13.16
,40.32,1.02,792.31,2.85,13.24,4.76,8.27,15.13,8251.22,56.03,277.04,1.97,17.66,12.4,5443.6
,330427.89,91.69,28.9,7769.57,144.29,49946,30.68,4.52
]

plthydro['STOCapacity'] = np.select(cond1, opt20)

##eliminar generadores con capacidad 0
indexNames = plthydro[plthydro['PowerCapacity'] == 0].index
plthydro.drop(indexNames , inplace=True)



### TERMO
pltthermo = pd.merge(thermo, dbus,  how="left", on=['Unit'])
pltthermo['Technology'] = 'GTUR'
condiciones =[
              (pltthermo['Fuel'] >= 1)&(pltthermo['Fuel'] <= 10), 
              (pltthermo['Fuel'] >= 12)&(pltthermo['Fuel'] <= 14),
              (pltthermo['Fuel'] == 11), 
              (pltthermo['Fuel'] >= 17)&(pltthermo['Fuel'] <= 21),
              (pltthermo['Fuel'] >= 15)&(pltthermo['Fuel'] <= 16), 
              (pltthermo['Fuel'] >= 22)&(pltthermo['Fuel'] <= 24),
              ]
opciones = ['GAS',
            'GAS',
            'OIL',
            'OIL',
            'BIO',
            'BIO'
            ] 
pltthermo['Fuel'] = np.select(condiciones,opciones)
column_to_move = pltthermo.pop('Fuel')
pltthermo.insert(4, 'Fuel', column_to_move)
pltthermo['STOCapacity'] = ''


##VRES
pltvres = pd.merge(vres, dbus,  how="left", on=['Unit'])
condiciones1 =[
              (pltvres['!Num'] >= 1)&(pltvres['!Num'] <= 2), 
              (pltvres['!Num'] >= 10)&(pltvres['!Num'] <= 18),
              (pltvres['!Num'] >= 5)&(pltvres['!Num'] <= 9),
              ]
opciones1 = ['WTON',
            'WTON',
            'PHOT',
            ] 
opciones2 = ['WIN',
            'WIN',
            'SUN',
            ] 
pltvres['Technology'] = np.select(condiciones1,opciones1)
pltvres['Fuel'] = np.select(condiciones1,opciones2)
pltvres = pltvres.drop(['!Num'], axis=1)
pltvres['STOCapacity'] = ''


frames = [plthydro, pltthermo, pltvres]
  
PowerPlantData = pd.concat(frames)

#PARA QUE ENDE PONGA VALORES DE SUS UNIDADES GENERADORAS
# PowerPlantData['Nunits'] = 1
# PowerPlantData[['Efficiency','MinUpTime','MinDownTime','RampUpRate',
#                'RampDownRate','StartUpCost','NoLoadCost','RampingCost',
#                'PartLoadMin','MinEfficiency','StartUpTime','CO2Intensity',
#                'STOSelfDischarge','STOMaxChargingPower',
#                'STOChargingEfficiency']] = 'ENDE'

# PowerPlantData[['CHPType','CHPPowerToHeat']] = 0

#######################Asignando valores tipo
ppd = PowerPlantData

cond = [
        ppd['Fuel']=='WAT',
        ppd['Fuel']=='GAS',
        ppd['Fuel']=='OIL',
        ppd['Fuel']=='BIO',
        ppd['Fuel']=='WIN',
        ppd['Fuel']=='SUN']

opt1 = [0.8,0.35,0.35,0.31,1,1]
opt2 = [0,0,0,0,0,0]
opt3 = [0,0,0,0,0,0]
opt4 = [0.06666667,0.06666667,0.06666667,0.06666667,0.02,0.02]
opt5 = [0.06666667,0.06666667,0.06666667,0.06666667,0.02,0.02]
opt6 = [0,25,25,25,0,0]
opt7 = [0,0,0,0,0,0]
opt8 = [0,0.8,0.8,0.8,0,0]
opt9 = [0,0.3,0.3,0.3,0,0]
opt10 = [1,0.33,0.33,0.33,1,1]
opt11 = [0,0,0,0,0,0]
opt12 = [0,0.574,0.755,0,0,0]
opt13 = ['','','','','','']
opt14 = ['','','','','','']
opt15 = [0,'','','','','']
opt16 = [0,'','','','','']
opt17 = [0.8,'','','','','']
opt18 = [1,1,1,1,1,1]

ppd['Efficiency'] = np.select(cond, opt1)
ppd['MinUpTime'] = np.select(cond, opt2)
ppd['MinDownTime'] = np.select(cond, opt3)
ppd['RampUpRate'] = np.select(cond, opt4)
ppd['RampDownRate'] = np.select(cond, opt5)
ppd['StartUpCost'] = np.select(cond, opt6)
ppd['NoLoadCost'] = np.select(cond, opt7)
ppd['RampingCost'] = np.select(cond, opt8)
ppd['PartLoadMin'] = np.select(cond, opt9)
ppd['MinEfficiency'] = np.select(cond, opt10)
ppd['StartUpTime'] = np.select(cond, opt11)
ppd['CO2Intensity'] = np.select(cond, opt12)
ppd['CHPType'] = np.select(cond, opt13)
ppd['CHPPowerToHeat'] = np.select(cond, opt14)
ppd['STOSelfDischarge'] = np.select(cond, opt15)
ppd['STOMaxChargingPower'] = np.select(cond, opt16)
ppd['STOChargingEfficiency'] = np.select(cond, opt17)
ppd['Nunits'] = np.select(cond, opt18)



#ordenar el dataframe
PowerPlantData = ppd
PowerPlantData = PowerPlantData[['PowerCapacity','Unit','Zone','Technology','Fuel',
                                 'Efficiency','MinUpTime','MinDownTime','RampUpRate',
                                 'RampDownRate','StartUpCost','NoLoadCost','RampingCost',
                                 'PartLoadMin','MinEfficiency','StartUpTime','CO2Intensity',
                                 'CHPType','CHPPowerToHeat','STOCapacity','STOSelfDischarge',
                                 'STOMaxChargingPower','STOChargingEfficiency','Nunits']] 


PowerPlantData.set_index('PowerCapacity',inplace=True, drop=True)

df9 = PowerPlantData
df9.reset_index(level =0, inplace = True)
buslist = pd.read_csv('../BaseDatos_DispaSET/BusList-ZONES1.csv', encoding='cp1252')

busname = buslist.Busname
busname.to_dict()
busname = np.asarray(busname)
zone = buslist.Zone
zone.to_dict()
zone = np.asarray(zone)
for i, j in zip(busname, zone):
    df9['Zone'] = df9['Zone'].str.replace(i,j, regex=False)


df9.set_index('PowerCapacity',inplace=True, drop=True)


df9.to_csv('../BaseDatos_DispaSET/PowerPlantData/PowerPlantData_AREAS.csv') 












