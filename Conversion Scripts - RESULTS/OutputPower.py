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
df = pd.read_csv('../BaseDatos_SDDP/rgerter.csv', encoding='cp1252', index_col=0, header=3)
df.reset_index(level =0, inplace = True)
df = df.drop(['Ser.'], axis=1)
df.columns = df.columns.str.replace(' ', '')
df = df.rename({'Etap':'Week','Bloq':'Block'}, axis=1)	

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

# Conversion de valores por bloque a valores horarios Power/duration each block per week
durB = 61
durM = 81
durI = 16
durSP = 6
durP = 4

df3 = df2.drop(['Datetime','Week'], axis=1)
df3.reset_index(level =0, inplace = True)
df3 = df3.rename({'index':'order'}, axis=1)	

bloqueB = df3[df3['Block'] == 5]
bloqueB = bloqueB/durB
bloqueB['order'] = bloqueB['order']*durB
bloqueB['Block'] = bloqueB['Block']*durB

bloqueM = df3[df3['Block'] == 4]
bloqueM = bloqueM/durM
bloqueM['order'] = bloqueM['order']*durM
bloqueM['Block'] = bloqueM['Block']*durM

bloqueI = df3[df3['Block'] == 3]
bloqueI = bloqueI/durI
bloqueI['order'] = bloqueI['order']*durI
bloqueI['Block'] = bloqueI['Block']*durI

bloqueSP = df3[df3['Block'] == 2]
bloqueSP = bloqueSP/durSP
bloqueSP['order'] = bloqueSP['order']*durSP
bloqueSP['Block'] = bloqueSP['Block']*durSP

bloqueP = df3[df3['Block'] == 1]
bloqueP = bloqueP/durP
bloqueP['order'] = bloqueP['order']*durP
bloqueP['Block'] = bloqueP['Block']*durP

frames = (bloqueB,bloqueM,bloqueI,bloqueSP,bloqueP)
df4 = pd.concat(frames, axis = 0)
df4 = df4.sort_values(by=['order'])
 
df3 = df4*1000

df3['TIMESTAMP'] = df2['Datetime']
column_to_move = df3.pop('TIMESTAMP')
df3.insert(0, 'TIMESTAMP', column_to_move)

df3 = df3.drop(['Block','order'], axis=1)


df2 = df3

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

#FILTRAR GAS Y BIO POR SEPARADO
genlist = df1[['Unit','Zone','Fuel']]
genlistGAS = genlist[(genlist.Fuel) == 'GAS']
genlistGAS = genlistGAS.drop(['Fuel'], axis=1)
genlistBIO = genlist[(genlist.Fuel) == 'BIO']
genlistBIO = genlistBIO.drop(['Fuel'], axis=1)

#GAS
genname = genlistGAS.Unit
genname.to_dict()
genname = np.asarray(genname)
zone = genlistGAS.Zone
zone.to_dict()
zone = np.asarray(zone)
for m, n in zip(genname, zone):
    df2 = df2.rename({m:n}, axis=1)

df2 = df2.groupby(level=0, axis=1).sum()

df2.set_index('TIMESTAMP',inplace=True, drop=True)

genGAS = df2[['CE','OR','NO','SU']]
df2 = df2.drop(['CE','OR','NO','SU'], axis=1)
#BIO
genname = genlistBIO.Unit
genname.to_dict()
genname = np.asarray(genname)
zone = genlistBIO.Zone
zone.to_dict()
zone = np.asarray(zone)
for o, p in zip(genname, zone):
    df2 = df2.rename({o:p}, axis=1)

df2 = df2.groupby(level=0, axis=1).sum()



genBIO = df2[['OR','NO']]
df2 = df2.drop(['OR','NO'], axis=1)



#FINAL
#%% 
#%% 
#GENERACION HIDRO
df = pd.read_csv('../BaseDatos_SDDP/rgerhid.csv', encoding='cp1252', index_col=0, header=3)
df.reset_index(level =0, inplace = True)
df = df.drop(['Ser.'], axis=1)
df.columns = df.columns.str.replace(' ', '')
df = df.rename({'Etap':'Week','Bloq':'Block'}, axis=1)	

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

# Conversion de valores por bloque a valores horarios Power/duration each block per week
durB = 61
durM = 81
durI = 16
durSP = 6
durP = 4

df3 = df2.drop(['Datetime','Week'], axis=1)
df3.reset_index(level =0, inplace = True)
df3 = df3.rename({'index':'order'}, axis=1)	

bloqueB = df3[df3['Block'] == 5]
bloqueB = bloqueB/durB
bloqueB['order'] = bloqueB['order']*durB
bloqueB['Block'] = bloqueB['Block']*durB

bloqueM = df3[df3['Block'] == 4]
bloqueM = bloqueM/durM
bloqueM['order'] = bloqueM['order']*durM
bloqueM['Block'] = bloqueM['Block']*durM

bloqueI = df3[df3['Block'] == 3]
bloqueI = bloqueI/durI
bloqueI['order'] = bloqueI['order']*durI
bloqueI['Block'] = bloqueI['Block']*durI

bloqueSP = df3[df3['Block'] == 2]
bloqueSP = bloqueSP/durSP
bloqueSP['order'] = bloqueSP['order']*durSP
bloqueSP['Block'] = bloqueSP['Block']*durSP

bloqueP = df3[df3['Block'] == 1]
bloqueP = bloqueP/durP
bloqueP['order'] = bloqueP['order']*durP
bloqueP['Block'] = bloqueP['Block']*durP

frames = (bloqueB,bloqueM,bloqueI,bloqueSP,bloqueP)
df4 = pd.concat(frames, axis = 0)
df4 = df4.sort_values(by=['order'])
 
df3 = df4*1000

df3['TIMESTAMP'] = df2['Datetime']
column_to_move = df3.pop('TIMESTAMP')
df3.insert(0, 'TIMESTAMP', column_to_move)

df3 = df3.drop(['Block','order'], axis=1)


df2 = df3

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
    df2 = df2.rename({i:j}, axis=1)

df2 = df2.groupby(level=0, axis=1).sum()




df2.set_index('TIMESTAMP',inplace=True, drop=True)

genHIDRO = df2[['CE','NO','SU']]
df2 = df2.drop(['CE','NO','SU'], axis=1)

#FINAL
#%% 

#%% 
#GENERACION RENOVABLE
df = pd.read_csv('../BaseDatos_SDDP/rgergnd.csv', encoding='cp1252', index_col=0, header=3)
df.reset_index(level =0, inplace = True)
df = df.drop(['Ser.'], axis=1)
df.columns = df.columns.str.replace(' ', '')
df = df.rename({'Etap':'Week','Bloq':'Block'}, axis=1)	

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

# Conversion de valores por bloque a valores horarios Power/duration each block per week
durB = 61
durM = 81
durI = 16
durSP = 6
durP = 4

df3 = df2.drop(['Datetime','Week'], axis=1)
df3.reset_index(level =0, inplace = True)
df3 = df3.rename({'index':'order'}, axis=1)	

bloqueB = df3[df3['Block'] == 5]
bloqueB = bloqueB/durB
bloqueB['order'] = bloqueB['order']*durB
bloqueB['Block'] = bloqueB['Block']*durB

bloqueM = df3[df3['Block'] == 4]
bloqueM = bloqueM/durM
bloqueM['order'] = bloqueM['order']*durM
bloqueM['Block'] = bloqueM['Block']*durM

bloqueI = df3[df3['Block'] == 3]
bloqueI = bloqueI/durI
bloqueI['order'] = bloqueI['order']*durI
bloqueI['Block'] = bloqueI['Block']*durI

bloqueSP = df3[df3['Block'] == 2]
bloqueSP = bloqueSP/durSP
bloqueSP['order'] = bloqueSP['order']*durSP
bloqueSP['Block'] = bloqueSP['Block']*durSP

bloqueP = df3[df3['Block'] == 1]
bloqueP = bloqueP/durP
bloqueP['order'] = bloqueP['order']*durP
bloqueP['Block'] = bloqueP['Block']*durP

frames = (bloqueB,bloqueM,bloqueI,bloqueSP,bloqueP)
df4 = pd.concat(frames, axis = 0)
df4 = df4.sort_values(by=['order'])
 
df3 = df4*1000

df3['TIMESTAMP'] = df2['Datetime']
column_to_move = df3.pop('TIMESTAMP')
df3.insert(0, 'TIMESTAMP', column_to_move)

df3 = df3.drop(['Block','order'], axis=1)


df2 = df3

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

#FILTRAR SOLAR Y EOLICAS POR SEPARADO
genlist = df1[['Unit','Zone','Fuel']]
genlistSUN = genlist[(genlist.Fuel) == 'SUN']
genlistSUN = genlistSUN.drop(['Fuel'], axis=1)
genlistWIN = genlist[(genlist.Fuel) == 'WIN']
genlistWIN = genlistWIN.drop(['Fuel'], axis=1)

#SUN
genname = genlistSUN.Unit
genname.to_dict()
genname = np.asarray(genname)
zone = genlistSUN.Zone
zone.to_dict()
zone = np.asarray(zone)
for i, j in zip(genname, zone):
    df2 = df2.rename({i:j}, axis=1)

df2 = df2.groupby(level=0, axis=1).sum()

df2.set_index('TIMESTAMP',inplace=True, drop=True)

genSUN = df2[['CE','SU']]
df2 = df2.drop(['CE','SU'], axis=1)

#WIN
genname = genlistWIN.Unit
genname.to_dict()
genname = np.asarray(genname)
zone = genlistWIN.Zone
zone.to_dict()
zone = np.asarray(zone)
for k, l in zip(genname, zone):
    df2 = df2.rename({k:l}, axis=1)

df2 = df2.groupby(level=0, axis=1).sum()



genWIN = df2
df2 = df2.drop(['CE','OR','SU'], axis=1)


#FINAL
#%% PLOTS
import numpy as np
import matplotlib.pyplot as plt  
genGAS = genGAS.rename({'CE':'GAS-CE','OR':'GAS-OR','NO':'GAS-NO','SU':'GAS-SU'}, axis=1)
genHIDRO = genHIDRO.rename({'CE':'WAT-CE','NO':'WAT-NO','SU':'WAT-SU'}, axis=1)	
genBIO = genBIO.rename({'NO':'BIO-NO','OR':'BIO-OR'}, axis=1)
genSUN = genSUN.rename({'CE':'SUN-CE','SU':'SUN-SU'}, axis=1)
genWIN = genWIN.rename({'CE':'WIN-CE','OR':'WIN-OR','SU':'WIN-SU'}, axis=1)
outputpower =  pd.concat([genGAS, genHIDRO, genBIO, genSUN , genWIN], axis=1)


 
outputpower.to_csv('../BaseDatos_DispaSET/Results/FINAL_SDDP/OutputPower.csv', header=True, index=True)


        

