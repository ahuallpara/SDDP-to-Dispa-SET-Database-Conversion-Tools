# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 08:59:55 2022

@author: navia
"""

import numpy as np
import pandas as pd
from functools import reduce


#outages termal units
dft1 = pd.read_csv('../BaseDatos_SDDP/pmtrsebo.csv', encoding='cp1252')
dft1 = dft1.fillna(0)
dft1 = dft1/100
dft1.Año = dft1.Año*100
dft1.Etapas = dft1.Etapas*100
dft1 = dft1.rename({'Año':'Year'}, axis=1)
dft1 = dft1.rename({'Etapas':'Week'}, axis=1)

df_tt = pd.DataFrame()

df_tt['Datetime'] = pd.date_range(start='2021-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
df_tt['Datetime'] = pd.to_datetime(df_tt['Datetime'])

 
df_tt['Week'] = pd.DatetimeIndex(df_tt.Datetime).week
df_tt['Year'] = pd.DatetimeIndex(df_tt.Datetime).year   

outagesterm1 = pd.merge( df_tt, dft1,  how="left", on=['Year','Week'])
column_to_move1 = outagesterm1.pop('Datetime')
outagesterm1.insert(0, 'Datetime', column_to_move1)
outagesterm1 = outagesterm1.fillna(0)

outagesterm1 = outagesterm1.drop(['Year','Week'], axis=1)

outagesterm1.set_index('Datetime', inplace = True)

dft2 = pd.read_csv('../BaseDatos_SDDP/ctermibo.csv', encoding='cp1252')
dft2 = dft2[['...Nombre...','..Ih...']]

dft2 = dft2.transpose()
dft2.reset_index(level =0, inplace = True)
dft2 = dft2.drop(['index'], axis=1)
dft2.columns = dft2.iloc[0]
dft2 = dft2[1:]
dft2 = dft2/100
dft2['Año'] = 'Año'

dft3 = pd.DataFrame()
dft3['Year']  = [2021, 2022, 2023, 2024, 2025, 2026]
dft3['Año']  = 'Año'

dft4 = pd.merge( dft3, dft2,  how="left", on=['Año'])
dft4 = dft4.drop(['Año'], axis=1)


df_tt1 = pd.DataFrame()

df_tt1['Datetime'] = pd.date_range(start='2021-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
df_tt1['Datetime'] = pd.to_datetime(df_tt1['Datetime'])

 
df_tt1['Year'] = pd.DatetimeIndex(df_tt1.Datetime).year   

outagesterm2 = pd.merge( df_tt1, dft4,  how="left", on=['Year'])
column_to_move1 = outagesterm2.pop('Datetime')
outagesterm2.insert(0, 'Datetime', column_to_move1)
outagesterm2 = outagesterm2.fillna(0)
outagesterm2 = outagesterm2.drop(['Year'], axis=1)

outagesterm2.set_index('Datetime', inplace = True)


outagesterm = outagesterm1.add(outagesterm2, fill_value=0)
outagesterm = outagesterm.where(outagesterm <= 1, 1) 
outagesterm.reset_index(level =0, inplace = True)

################################################################################


#outages hydro units
dfh1 = pd.read_csv('../BaseDatos_SDDP/pmhisebo.csv', encoding='cp1252')
dfh1 = dfh1.fillna(0)
dfh1 = dfh1/100
dfh1.Año = dfh1.Año*100
dfh1.Etapas = dfh1.Etapas*100
dfh1 = dfh1.rename({'Año':'Year'}, axis=1)
dfh1 = dfh1.rename({'Etapas':'Week'}, axis=1)

df_th = pd.DataFrame()

df_th['Datetime'] = pd.date_range(start='2021-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
df_th['Datetime'] = pd.to_datetime(df_th['Datetime'])

df_th['Year'] = pd.DatetimeIndex(df_th.Datetime).year  
df_th['Week'] = pd.DatetimeIndex(df_th.Datetime).week
  
outageshydro = pd.merge( df_th, dfh1,  how="left", on=['Year','Week'])
column_to_move1 = outageshydro.pop('Datetime')
outageshydro.insert(0, 'Datetime', column_to_move1)
outageshydro = outageshydro.fillna(0)

outageshydro = outageshydro.drop(['Year','Week'], axis=1)

################################################################################


#outages vres units
dfv1 = pd.read_csv('../BaseDatos_SDDP/cgndbo.csv', encoding='cp1252')
dfv1 = dfv1.fillna(0)
dfv1 = dfv1[['Name','ProbFal']]
dfv1 = dfv1.transpose()
dfv1.reset_index(level =0, inplace = True)
dfv1 = dfv1.drop(['index'], axis=1)
dfv1.columns = dfv1.iloc[0]
dfv1 = dfv1[1:]

dfv1 = dfv1/100
dfv1['Año'] = 'Año'

dfv2 = pd.DataFrame()
dfv2['Year']  = [2021, 2022, 2023, 2024, 2025, 2026]
dfv2['Año']  = 'Año'

dfv3 = pd.merge( dfv1, dfv2,  how="left", on=['Año'])
dfv3 = dfv3.drop(['Año'], axis=1)

df_tv = pd.DataFrame()

df_tv['Datetime'] = pd.date_range(start='2021-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
df_tv['Datetime'] = pd.to_datetime(df_tv['Datetime'])

df_tv['Year'] = pd.DatetimeIndex(df_tv.Datetime).year  

outagesvres = pd.merge( df_tv, dfv3,  how="left", on=['Year'])
column_to_move1 = outagesvres.pop('Datetime')
outagesvres.insert(0, 'Datetime', column_to_move1)
outagesvres = outagesvres.fillna(0)

outagesvres = outagesvres.drop(['Year'], axis=1)



################################################################################
#merge all the outages
  
Outages = pd.merge( outagesterm, outageshydro,  how="left", on=['Datetime'])
Outages = pd.merge( Outages, outagesvres,  how="left", on=['Datetime'])
Outages = Outages.rename({'Datetime':'TIMESTAMP'}, axis=1)	



##########FILTRAR FECHAS Y ELIMINAR LO QUE NO SIRVE

mask1 = (Outages['TIMESTAMP'] > '2025-12-31 22:00:00+00:00') & (Outages['TIMESTAMP'] <= '2026-12-31 23:00:00+00:00')
Outages = Outages.loc[mask1]
Outages.set_index('TIMESTAMP',inplace=True, drop=True)
Outages = Outages.drop(['ANGLG','CRBLG','TIQLG','SRO02LG','CHJLG','CALACHAUM_LG','CALACHAKA_TO',
                        'CHUCALOMA_TO','CHACAJAHU_TO','CARABUCO_TO','UMAPALCA_CA','PALILLA01_CA',
                        'JALANCHA_TO','CALACHAMI_TO','PALILLA02_CA','CHORO_TO','KEWANI_TO',
                        'JUNTAS_TO','FICTICIA','MOLLE'], axis=1)

Outages.to_csv('../BaseDatos_DispaSET/Outages/Outages.csv')