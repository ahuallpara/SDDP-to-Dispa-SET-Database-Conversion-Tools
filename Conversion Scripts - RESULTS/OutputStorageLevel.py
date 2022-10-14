# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 18:04:10 2021

@author: MARCO NAVIA
"""
import numpy as np
import pandas as pd
from functools import reduce
#### NOTA IMPORTANTE: QUITAR ACENTOS DE LOS ARCHIVOS CSV DEL SDDP
#%% 
#GENERACION TERMICA
df = pd.read_csv('../BaseDatos_SDDP/rvolfin.csv', encoding='cp1252', index_col=0, header=3)
df.reset_index(level =0, inplace = True)
df = df.drop(['Ser.'], axis=1)
df.columns = df.columns.str.replace(' ', '')
df = df.rename({'Etap':'Week','Bloq':'Block'}, axis=1)	

#convertir hm3 a MW
hydro = pd.read_csv('../BaseDatos_SDDP/chidrobo.csv', encoding='cp1252', header=0)
hydro = hydro[['...Nombre...','.FPMed.']]
hydro = hydro.rename({'...Nombre...':'Unit'}, axis=1)	

hydro['ConversionFactor'] = (hydro['.FPMed.'] * 10000)/36
hydro = hydro.drop(['.FPMed.'], axis=1)
hydro = hydro.transpose()
hydro.reset_index(level =0, inplace = True)
hydro = hydro.drop(['index'], axis=1)
hydro.columns = hydro.iloc[0]
hydro = hydro[1:]
convfact = pd.DataFrame()

i=0

for i in range(208):
    convfact = convfact.append(hydro)

df_data = df[['Week','Block']]
df = df.drop(['Week','Block'], axis=1)

df_converted = pd.DataFrame()

hydrolist = hydro.columns

for i in hydrolist:
    convfact = convfact.rename({i:'Factor'+i}, axis=1)

convfact.reset_index(level =0, inplace = True)
convfact = convfact.drop(['index'], axis=1)
frames = (df, convfact)
df_converted = pd.concat(frames, axis = 1)

for i in hydrolist:
    df_converted = df_converted.rename({i:'Prev.'+i}, axis=1)

for i in hydrolist:
    df_converted[i] = df_converted['Factor'+i] * df_converted['Prev.'+i]

df_converted = df_converted[hydrolist]
frames = (df_data, df_converted)
df_new = pd.concat(frames, axis = 1)

df = df_new

#para escoger el ultimo año
mask = (df['Week'] > 156)
df = df.loc[mask]
df['Week'] = df['Week'] - 156

df_t = pd.DataFrame()

df_t['Datetime'] = pd.date_range(start='2025-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
df_t['Datetime'] = pd.to_datetime(df_t['Datetime'])

df_t['Weekday'] = pd.DatetimeIndex(df_t.Datetime).weekday
df_t['Hour'] = pd.DatetimeIndex(df_t.Datetime).hour
df_t['Block'] = " "


condiciones =[
    #lunes
              (df_t['Weekday'] == 0)&(df_t['Hour'] == 0), 
              (df_t['Weekday'] == 0)&(df_t['Hour'] == 23),
              (df_t['Weekday'] == 0)&(df_t['Hour'] >= 8)&(df_t['Hour'] <= 18),
              (df_t['Weekday'] == 0)&(df_t['Hour'] >= 1)&(df_t['Hour'] <= 7),
              (df_t['Weekday'] == 0)&(df_t['Hour'] == 19), 
              (df_t['Weekday'] == 0)&(df_t['Hour'] == 22),
              (df_t['Weekday'] == 0)&(df_t['Hour'] >= 20)&(df_t['Hour'] <= 21),
    #martes
              (df_t['Weekday'] == 1)&(df_t['Hour'] == 0), 
              (df_t['Weekday'] == 1)&(df_t['Hour'] == 23),
              (df_t['Weekday'] == 1)&(df_t['Hour'] >= 8)&(df_t['Hour'] <= 18),
              (df_t['Weekday'] == 1)&(df_t['Hour'] >= 1)&(df_t['Hour'] <= 7),
              (df_t['Weekday'] == 1)&(df_t['Hour'] == 19), 
              (df_t['Weekday'] == 1)&(df_t['Hour'] == 22),
              (df_t['Weekday'] == 1)&(df_t['Hour'] == 20),
              (df_t['Weekday'] == 1)&(df_t['Hour'] == 21),
    #miercoles                        
              (df_t['Weekday'] == 2)&(df_t['Hour'] == 0), 
              (df_t['Weekday'] == 2)&(df_t['Hour'] == 23),
              (df_t['Weekday'] == 2)&(df_t['Hour'] >= 8)&(df_t['Hour'] <= 18),
              (df_t['Weekday'] == 2)&(df_t['Hour'] >= 1)&(df_t['Hour'] <= 7),
              (df_t['Weekday'] == 2)&(df_t['Hour'] == 19), 
              (df_t['Weekday'] == 2)&(df_t['Hour'] == 22),
              (df_t['Weekday'] == 2)&(df_t['Hour'] == 20),
              (df_t['Weekday'] == 2)&(df_t['Hour'] == 21),
    #jueves                            
              (df_t['Weekday'] == 3)&(df_t['Hour'] == 0), 
              (df_t['Weekday'] == 3)&(df_t['Hour'] == 23),
              (df_t['Weekday'] == 3)&(df_t['Hour'] >= 8)&(df_t['Hour'] <= 18),
              (df_t['Weekday'] == 3)&(df_t['Hour'] >= 1)&(df_t['Hour'] <= 7),
              (df_t['Weekday'] == 3)&(df_t['Hour'] == 19), 
              (df_t['Weekday'] == 3)&(df_t['Hour'] == 22),
              (df_t['Weekday'] == 3)&(df_t['Hour'] == 20),
              (df_t['Weekday'] == 3)&(df_t['Hour'] == 21),
    #viernes                            
              (df_t['Weekday'] == 4)&(df_t['Hour'] == 0), 
              (df_t['Weekday'] == 4)&(df_t['Hour'] == 23),
              (df_t['Weekday'] == 4)&(df_t['Hour'] >= 8)&(df_t['Hour'] <= 18),
              (df_t['Weekday'] == 4)&(df_t['Hour'] >= 1)&(df_t['Hour'] <= 7),
              (df_t['Weekday'] == 4)&(df_t['Hour'] == 19), 
              (df_t['Weekday'] == 4)&(df_t['Hour'] == 22),
              (df_t['Weekday'] == 4)&(df_t['Hour'] == 20),
              (df_t['Weekday'] == 4)&(df_t['Hour'] == 21),
    #sabado              
              (df_t['Weekday'] == 5)&(df_t['Hour'] == 0), 
              (df_t['Weekday'] == 5)&(df_t['Hour'] == 23),
              (df_t['Weekday'] == 5)&(df_t['Hour'] >= 8)&(df_t['Hour'] <= 18),
              (df_t['Weekday'] == 5)&(df_t['Hour'] >= 1)&(df_t['Hour'] <= 7),
              (df_t['Weekday'] == 5)&(df_t['Hour'] >= 19)&(df_t['Hour'] <= 22),
              
    #domingo             
              (df_t['Weekday'] == 6)&(df_t['Hour'] >= 0)&(df_t['Hour'] <= 18),
              (df_t['Weekday'] == 6)&(df_t['Hour'] == 19), 
              (df_t['Weekday'] == 6)&(df_t['Hour'] >= 20)&(df_t['Hour'] <= 21),
              (df_t['Weekday'] == 6)&(df_t['Hour'] >= 22)&(df_t['Hour'] <= 23)
              ]   

opciones = [4,4,4,5,3,3,2,
            4,4,4,5,3,3,1,2,
            4,4,4,5,3,3,1,2,
            4,4,4,5,3,3,1,2,
            4,4,4,5,3,3,1,2,
            4,4,4,5,3,
            5,4,3,4
            ] 

df_t['Block'] = np.select(condiciones,opciones)
    
 
df_t['Week'] = pd.DatetimeIndex(df_t.Datetime).week
  
   

column_to_move = df_t.pop('Week')
df_t.insert(0, 'Week', column_to_move)
column_to_move1 = df_t.pop('Block')
df_t.insert(1, 'Block', column_to_move1)

df_t = df_t.drop(['Hour','Weekday'], axis=1)


df2 = pd.merge( df_t, df,  how="left", on=['Week', 'Block'])
column_to_move1 = df2.pop('Datetime')
df2.insert(0, 'Datetime', column_to_move1)

df2 = df2.drop(['Week','Block'], axis=1)
df2 = df2.rename({'Datetime':'TIMESTAMP'}, axis=1)	
df2.set_index('TIMESTAMP', inplace = True)

# df2.interpolate()

df3 = df2.astype(float)
   
df4 = df3.interpolate()  
    
df5 = df4.interpolate(method='linear', limit_direction='backward', axis=0)   
    

#POWERPLANT to zones
df1 = pd.read_csv('../BaseDatos_DispaSET/PowerPlantData/PowerPlantData.csv', encoding='cp1252')
df1.reset_index(level =0, inplace = True)
buslist = pd.read_csv('../BaseDatos_DispaSET/BusList-ZONES1.csv', encoding='cp1252')

busname = buslist.Busname
busname.to_dict()
busname = np.asarray(busname)
zone = buslist.Zone
zone.to_dict()
zone = np.asarray(zone)
for i, j in zip(busname, zone):
    df1['Zone'] = df1['Zone'].str.replace(i,j, regex=False)

genlist = df1[['Unit','Zone']]

#demand

genname = genlist.Unit
genname.to_dict()
genname = np.asarray(genname)
zone = genlist.Zone
zone.to_dict()
zone = np.asarray(zone)
for i, j in zip(genname, zone):
    df5 = df5.rename({i:j}, axis=1)

df5 = df5.groupby(level=0, axis=1).sum()

df5 = df5[['CE','NO','SU']]

 
df5.to_csv('../BaseDatos_DispaSET/Results/FINAL_SDDP/OutputStorageLevel.csv', header=True, index=True)


