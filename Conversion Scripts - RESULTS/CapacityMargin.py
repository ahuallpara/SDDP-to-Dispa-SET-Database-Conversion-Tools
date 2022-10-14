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
#HIDRO
df = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_SDDP/margcapahid.csv', encoding='cp1252', index_col=0, header=5)
df.reset_index(level =0, inplace = True)
df = df.drop([0,261,262,263,264,265],axis=0)
df.reset_index(level =0, inplace = True)
df.columns = df.columns.str.replace(' ', '')
df = df.drop(['index',''], axis=1)
df.reset_index(level =0, inplace = True)

dfa = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_SDDP/rgerhid.csv', encoding='cp1252', index_col=0, header=3)
dfa.reset_index(level =0, inplace = True)
dfa = dfa.drop(['Ser.'], axis=1)
dfa.columns = dfa.columns.str.replace(' ', '')
dfa = dfa.rename({'Etap':'Week','Bloq':'Block'}, axis=1)	

#para escoger el ultimo año
mask = (dfa['Week'] > 156)
dfa = dfa.loc[mask]
dfa['Week'] = dfa['Week'] - 156
dfa = dfa[['Week','Block']]
dfa.reset_index(level =0, inplace = True)
dfa = dfa.drop(['index'], axis=1)
dfa.reset_index(level =0, inplace = True)

df = pd.concat([df, dfa],axis=1)
df = df.drop(['index','Unnamed:54'], axis=1)
column_to_move = df.pop('Week')
df.insert(0, 'Week', column_to_move)
column_to_move1 = df.pop('Block')
df.insert(1, 'Block', column_to_move1)

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
df2.columns = df2.columns.str.replace(' ', '')

#POWERPLANT to zones
df1 = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_DispaSET/PowerPlantData/PowerPlantData.csv', encoding='cp1252')
df1.reset_index(level =0, inplace = True)
buslist = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_DispaSET/BusList-ZONES1.csv', encoding='cp1252')

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

df2 = df2.fillna(0)
df3 = df2.astype(float)


df3 = df3.groupby(level=0, axis=1).sum()
df3 = df3[['CE','NO','SU']]

capmarghidro = df3

#%% 
#TERMO
df = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_SDDP/margcapater.csv', encoding='cp1252', index_col=0, header=6)
df.reset_index(level =0, inplace = True)
df = df.drop([0,261,262,263,264,265],axis=0)
df.reset_index(level =0, inplace = True)
df.columns = df.columns.str.replace(' ', '')
df = df.drop(['index',''], axis=1)
df.reset_index(level =0, inplace = True)

dfa = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_SDDP/rgerter.csv', encoding='cp1252', index_col=0, header=3)
dfa.reset_index(level =0, inplace = True)
dfa = dfa.drop(['Ser.'], axis=1)
dfa.columns = dfa.columns.str.replace(' ', '')
dfa = dfa.rename({'Etap':'Week','Bloq':'Block'}, axis=1)	

#para escoger el ultimo año
mask = (dfa['Week'] > 156)
dfa = dfa.loc[mask]
dfa['Week'] = dfa['Week'] - 156
dfa = dfa[['Week','Block']]
dfa.reset_index(level =0, inplace = True)
dfa = dfa.drop(['index'], axis=1)
dfa.reset_index(level =0, inplace = True)

df = pd.concat([df, dfa],axis=1)
df = df.drop(['index'], axis=1)
column_to_move = df.pop('Week')
df.insert(0, 'Week', column_to_move)
column_to_move1 = df.pop('Block')
df.insert(1, 'Block', column_to_move1)

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
df2.columns = df2.columns.str.replace(' ', '')

#POWERPLANT to zones
df1 = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_DispaSET/PowerPlantData/PowerPlantData.csv', encoding='cp1252')
df1.reset_index(level =0, inplace = True)
buslist = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_DispaSET/BusList-ZONES1.csv', encoding='cp1252')

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

df2 = df2.ffill(axis = 0)
df3 = df2.astype(float)


df3 = df3.groupby(level=0, axis=1).sum()
df3 = df3[['CE','OR','NO','SU']]
    
    
capmargtermo = df3   

capmarg = pd.DataFrame()   
capmarg['CE']  =  capmargtermo['CE'] + capmarghidro['CE']
capmarg['OR']  =  capmargtermo['OR'] 
capmarg['NO']  =  capmargtermo['NO'] + capmarghidro['NO'] 
capmarg['SU']  =  capmargtermo['SU'] + capmarghidro['SU']      


    
capmarg.to_csv('../BaseDatos_DispaSET/Results/FINAL_SDDP/CapacityMargin.csv', header=True, index=True)
  
    
