# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 14:44:14 2022

@author: Isaline Gomand
"""

import numpy as np
import pandas as pd
from functools import reduce

InflowsSDDP = pd.read_csv('../BaseDatos_SDDP/hinflw_w.csv', encoding='cp1252', header=0)
PlantsSDDP = pd.read_csv('../BaseDatos_SDDP/chidrobo.csv', encoding='cp1252', header=0)
HROR_Units = pd.read_csv('HROR_Units_Sulmyra.csv', encoding='cp1252', index_col=0)

TimebyWeek = pd.DataFrame()
TimebyHour = pd.DataFrame()

TimebyHour = pd.date_range(start=str(InflowsSDDP['Año'].iloc[0])+'-01-01 00:00:00+00:00', end=str(InflowsSDDP['Año'].iloc[-1]+1)+'-01-01 00:00:00+00:00', freq='H')

df_final = pd.DataFrame(index=[TimebyHour], columns=PlantsSDDP['...Nombre...'])

TimebyWeek['Date'] = pd.date_range(start=str(InflowsSDDP['Año'].iloc[0])+'-01-01 00:00:00+00:00', end=str(InflowsSDDP['Año'].iloc[-1]+1)+'-01-01 00:00:00+00:00', freq='W')
TimebyWeek['Week'] = pd.DatetimeIndex(TimebyWeek.Date).week
TimebyWeek['Year'] = pd.DatetimeIndex(TimebyWeek.Date).year
TimebyWeek['Month'] = pd.DatetimeIndex(TimebyWeek.Date).month
TimebyWeek['Week'] = TimebyWeek['Week'].replace(53, 1)
for year in TimebyWeek.loc[TimebyWeek['Month']==1][TimebyWeek['Week']==52]['Year']:
    TimebyWeek.at[TimebyWeek.loc[TimebyWeek['Week'] == 52].loc[TimebyWeek['Year'] == year].index.tolist()[0], 'Year'] = year-1
TimebyWeek.set_index('Date', inplace=True)

QMax = pd.DataFrame(PlantsSDDP['.QMax..'])
QMax.index = PlantsSDDP['...Nombre...']

df = pd.DataFrame(columns=PlantsSDDP['...Nombre...'])
time = TimebyWeek.index[1]
for time in TimebyWeek.index:
    new_inflows = InflowsSDDP[InflowsSDDP['Año'] == TimebyWeek.loc[time]['Year']]
    tab = new_inflows[new_inflows['Etapa'] == TimebyWeek.loc[time]['Week']].iloc[:, 2:]
    tab.columns = PlantsSDDP['...Nombre...']
    tab.index = [str(time)]
    df = pd.concat([df, tab], axis=0)

last_row = pd.DataFrame(InflowsSDDP.iloc[-1, 2:])
last_row.index = PlantsSDDP['...Nombre...']
last_row.columns = [str(pd.DataFrame(TimebyHour).iloc[-1][0])]
df = pd.concat([df, last_row.T], axis=0)

#SISTEMA CORANI
df.loc[:,'SIS'] = df[:]['SIS']+df[:]['COR']
df.loc[:,'SJS'] = df[:]['SJS']+df[:]['SIS']+df[:]['FICTICIA']
df.loc[:,'SJE'] = df[:]['SJE']+df[:]['SJS']
#SISTEMA YURA
df.loc[:,'KIL'] = df[:]['KIL']+df[:]['CON']
df.loc[:,'LAN'] = df[:]['LAN']+df[:]['KIL'].clip(upper=float(QMax.loc['KIL']))
df.loc[:,'PUH'] = df[:]['PUH']+df[:]['LAN']
#SISTEMA MISICUNI
df.loc[:,'MOLLE'] = df[:]['MOLLE']+df[:]['MIS'].clip(upper=float(QMax.loc['MIS']))
#SISTEMA TAQUESI
df.loc[:,'CHJ'] = df[:]['CHJ']+df[:]['CHJLG']
df.loc[:,'YAN'] = df[:]['YAN']+df[:]['CHJ']
#SISTEMA ZONGO
df.loc[:,'TIQ'] = df[:]['TIQ']+df[:]['TIQLG'].clip(upper=float(QMax.loc['TIQLG']))
df.loc[:,'BOT'] = df[:]['BOT']+df[:]['TIQ']+df[:]['ZON']
df.loc[:,'CUT'] = df[:]['CUT']+df[:]['BOT']+(df[:]['TIQ']-df[:]['TIQ'].clip(upper=float(QMax.loc['TIQ'])))
df.loc[:,'SRO01'] = df[:]['SRO01']+df[:]['CUT'].clip(upper=float(QMax.loc['CUT']))
df.loc[:,'SRO02'] = df[:]['SRO02']+df[:]['SRO02LG']
df.loc[:,'SAI'] = df[:]['SAI']+df[:]['SRO01']+df[:]['SRO02']
df.loc[:,'CHU'] = df[:]['CHU']+df[:]['SAI']+(df[:]['SRO02']-df[:]['SRO02'].clip(upper=float(QMax.loc['SRO02'])))
df.loc[:,'HAR'] = df[:]['HAR']+df[:]['CHU']
df.loc[:,'CAH'] = df[:]['CAH']+df[:]['HAR']
df.loc[:,'HUA'] = df[:]['HUA']+df[:]['CAH']
#SISTEMA JUNTAS
df.loc[:,'JUNTAS_TO'] = df[:]['JUNTAS_TO']+(df[:]['SEH']-df[:]['SEH'].clip(upper=float(QMax.loc['SEH'])))
df.loc[:,'JUN'] = df[:]['JUN']+df[:]['SEH'].clip(upper=float(QMax.loc['SEH']))+df[:]['JUNTAS_TO'].clip(upper=float(QMax.loc['JUNTAS_TO']))

#SISTEMA MIGUILLAS
df.loc[:,'ANG'] = df[:]['ANG']+df[:]['ANGLG']
df.loc[:,'CHO'] = df[:]['CHO']+df[:]['ANG'].clip(upper=float(QMax.loc['ANG']))+df[:]['MIG'].clip(upper=float(QMax.loc['MIG']))
df.loc[:,'CRB'] = df[:]['CRB']+df[:]['CHO']+df[:]['CRBLG']+(df[:]['ANG']-df[:]['ANG'].clip(upper=float(QMax.loc['ANG'])))
df.loc[:,'CARABUCO_TO'] = df[:]['CARABUCO_TO']+df[:]['CRB'].clip(upper=float(QMax.loc['CRB']))
df.loc[:,'CHACAJAHU_TO'] = df[:]['CHACAJAHU_TO']+df[:]['CHUCALOMA_TO'].clip(upper=float(QMax.loc['CHUCALOMA_TO']))
df.loc[:,'CALACHAKA_TO'] = df[:]['CALACHAKA_TO']+df[:]['CALACHAUM_LG']
df.loc[:,'UMAPALCA_CA'] = df[:]['UMAPALCA_CA']+df[:]['CARABUCO_TO'].clip(upper=float(QMax.loc['CARABUCO_TO']))+df[:]['CHACAJAHU_TO'].clip(upper=float(QMax.loc['CHACAJAHU_TO']))+df[:]['CALACHAKA_TO'].clip(upper=float(QMax.loc['CALACHAKA_TO']))
df.loc[:,'UMA'] = df[:]['UMA']+df[:]['UMAPALCA_CA'].clip(upper=float(QMax.loc['UMAPALCA_CA']))
df.loc[:,'JALANCHA_TO'] = df[:]['JALANCHA_TO']+(df[:]['UMA']-df[:]['UMA'].clip(upper=float(QMax.loc['UMA'])))+(df[:]['CHUCALOMA_TO']-df[:]['CHUCALOMA_TO'].clip(upper=float(QMax.loc['CHUCALOMA_TO'])))+(df[:]['CHACAJAHU_TO']-df[:]['CHACAJAHU_TO'].clip(upper=float(QMax.loc['CHACAJAHU_TO'])))
df.loc[:,'CALACHAMI_TO'] = df[:]['CALACHAMI_TO']+(df[:]['UMAPALCA_CA']-df[:]['UMAPALCA_CA'].clip(upper=float(QMax.loc['UMAPALCA_CA'])))+(df[:]['CALACHAKA_TO']-df[:]['CALACHAKA_TO'].clip(upper=float(QMax.loc['CALACHAKA_TO'])))
df.loc[:,'PALILLA01_CA'] = df[:]['PALILLA01_CA']+df[:]['UMA']+df[:]['CALACHAMI_TO'].clip(upper=float(QMax.loc['CALACHAMI_TO']))+df[:]['JALANCHA_TO'].clip(upper=float(QMax.loc['JALANCHA_TO']))
df.loc[:,'PALILLA02_CA'] = df[:]['PALILLA02_CA']+df[:]['CHORO_TO'].clip(upper=float(QMax.loc['CHORO_TO']))+df[:]['PALILLA01_CA'].clip(upper=float(QMax.loc['PALILLA01_CA']))
df.loc[:,'PLD'] = df[:]['PLD']+df[:]['PALILLA02_CA'].clip(upper=float(QMax.loc['PALILLA02_CA']))+df[:]['KEWANI_TO'].clip(upper=float(QMax.loc['KEWANI_TO']))

df_final.iloc[0][:] = df.iloc[0][:]
df_final.iloc[-1][:] = df.iloc[-1][:]
for time in df.index:
    df_final.loc[time][:] = pd.DataFrame(df.loc[time][:]).T

QMax = QMax*3600
Inflows = df_final.astype('float64').interpolate()*3600
InflowsPerSec = Inflows/3600
ScaledInflows = pd.DataFrame(index=Inflows.index, columns=Inflows.columns)
for unit in Inflows.columns:
    ScaledInflows.loc[:,unit] = Inflows.loc[:,unit]/float(QMax.loc[unit])
    if unit in HROR_Units[HROR_Units['Technology']=='HROR'].index:
        ScaledInflows.loc[:, unit] = ScaledInflows.loc[:, unit].clip(upper=1)

startYear = int(str(TimebyHour[0])[0:4])
endYear = int(str(TimebyHour[-1])[0:4])
CapFactor = pd.DataFrame()
for year in range(startYear, endYear):
    CapFactor[year] = ScaledInflows.loc[str(year)].mean()
    ScaledInflows.loc[str(year)].to_csv('..\..\..\Dispa-SET_ENDE/ScaledInflows_N_Addition/' + str(year) + '.csv')
CapFactor.to_csv('..\..\..\Dispa-SET_ENDE/ScaledInflows_N_Addition/CapFactor_N_Addition.csv')
CapFactorMean = CapFactor.mean(axis=1)
CapFactorMax = CapFactor.max(axis=1)
CapFactorMin = CapFactor.min(axis=1)

CapFactorRef = pd.read_csv('CapacityFactor.csv', encoding='cp1252', index_col=0)
CapFactorRef_1 = CapFactorRef['Year 1']
CapFactorRef_2 = CapFactorRef['Year 2']
CapFactorRef_3 = CapFactorRef['Year 3']
CapFactorRef_4 = CapFactorRef['Year 4']

import matplotlib.pyplot as plt
Units = CapFactor.index
fig = plt.figure(figsize=(10, 7))
plt.scatter(Units, CapFactorMean, marker="<", color='C0')
# plt.scatter(Units, CapFactorMin, marker="v", color='C0')
# plt.scatter(Units, CapFactorMax, marker="^", color='C0')
plt.scatter(Units, CapFactorRef_1, marker="1", color='C3')
plt.scatter(Units, CapFactorRef_2, marker="2", color='C3')
plt.scatter(Units, CapFactorRef_3, marker="3", color='C3')
plt.scatter(Units, CapFactorRef_4, marker="4", color='C3')
plt.xticks(rotation=90)
plt.ylim(0, 2)
# plt.show()
plt.savefig('CapacityFactors.png')