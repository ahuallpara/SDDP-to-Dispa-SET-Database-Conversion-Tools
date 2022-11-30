# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 16:06:36 2022

@author: UMSS
"""
import numpy as np
import pandas as pd

Installed_cap=pd.read_csv('../SDDP_FLOWS/chidrobo.csv',encoding='cp1252')
Installed_cap=Installed_cap[['.PV.','....Pot']].transpose()
Installed_cap.columns = Installed_cap.iloc[0].astype(str)
Installed_cap=Installed_cap.drop('.PV.',axis=0)
sddpflw = pd.read_csv('../SDDP_FLOWS/hinflw_w.csv', encoding='cp1252')
sddpflw=sddpflw.drop('1979/01',axis=1)
Fall_down=Installed_cap.values[0,:]*1E6/(sddpflw*9.81*1000)

df_t = pd.DataFrame()

df_t['Datetime'] = pd.date_range(start='1979-01-07 23:00:00+00:00', end='2020-12-31 23:00:00+00:00', freq='W')
df_t['Datetime'] = pd.to_datetime(df_t['Datetime'])

 
df_t['Week'] = pd.DatetimeIndex(df_t.Datetime).week
df_t['Year'] = pd.DatetimeIndex(df_t.Datetime).year 
df_t = df_t.drop(df_t[df_t['Week']==53].index)
df_t.reset_index(level =0, inplace = True)
df_t = df_t.drop(['index'], axis=1)

Fall_down=pd.concat([df_t,Fall_down],axis=1)
Fall_down=Fall_down.drop(columns=['Week','Year'])
Fall_down.to_csv('../SDDP_FLOWS/FallDown.csv')
