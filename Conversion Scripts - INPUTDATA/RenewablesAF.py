# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:26:50 2022

@author: navia
"""

import numpy as np
import pandas as pd
from functools import reduce


vresaf = pd.read_csv('../BaseDatos_SDDP/blrenw005bo0_w.csv', encoding='cp1252', header=1)
vresaf = vresaf.drop(['Year'], axis=1)
vresaf = vresaf.rename({'!Scn.':'Year'}, axis=1)

condiciones =[
    #lunes
              (vresaf['Year'] == 1), 
              (vresaf['Year'] == 2), 
              (vresaf['Year'] == 3), 
              (vresaf['Year'] == 4), 
              (vresaf['Year'] == 5) 
              ]

opciones = [2022,
            2023,
            2024,
            2025,
            2026,
            ] 

vresaf['Year'] = np.select(condiciones,opciones)

#aumentando la semana 53
mask = (vresaf['Year'] == 2026) & (vresaf['Week'] == 52)
filtered_vresaf = vresaf.loc[mask]
filtered_vresaf['Week'] = filtered_vresaf['Week'].replace(52,53) 
vresaf = vresaf.append(filtered_vresaf)
#######

df_t = pd.DataFrame()

df_t['Datetime'] = pd.date_range(start='2021-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
df_t['Datetime'] = pd.to_datetime(df_t['Datetime'])

df_t['Weekday'] = pd.DatetimeIndex(df_t.Datetime).weekday
#df_t['Time'] = pd.DatetimeIndex(df_t.Datetime).time
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
df_t['Year'] = pd.DatetimeIndex(df_t.Datetime).year   
   

column_to_move0 = df_t.pop('Year')
df_t.insert(0, 'Year', column_to_move0)
column_to_move1 = df_t.pop('Week')
df_t.insert(1, 'Week', column_to_move1)
column_to_move2 = df_t.pop('Block')
df_t.insert(2, 'Block', column_to_move2)
df_t = df_t.drop(['Hour','Weekday'], axis=1)


RenewablesAF = pd.merge( df_t, vresaf,  how="left", on=['Year','Week', 'Block'])
column_to_move1 = RenewablesAF.pop('Datetime')
RenewablesAF.insert(0, 'Datetime', column_to_move1)

RenewablesAF = RenewablesAF.drop(['Year', 'Week','Block'], axis=1)
RenewablesAF = RenewablesAF.rename({'Datetime':'TIMESTAMP'}, axis=1)	


##########FILTRAR FECHAS
mask1 = (RenewablesAF['TIMESTAMP'] > '2025-12-31 22:00:00+00:00') & (RenewablesAF['TIMESTAMP'] <= '2026-12-31 23:00:00+00:00')
RenewablesAF = RenewablesAF.loc[mask1]
################

RenewablesAF.set_index('TIMESTAMP',inplace=True, drop=True)
RenewablesAF.to_csv('../BaseDatos_DispaSET/RenewablesAF/RenewablesAF.csv')