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
    df = df.rename({i:j}, axis=1)

df = df.groupby(level=0, axis=1).sum()


mask = (df['Etap'] > 156)
df2 = df.loc[mask]

gtermoce  = df2['CE'].sum()/1000
gtermono  = df2['NO'].sum()/1000
gtermoor  = df2['OR'].sum()/1000
gtermosu  = df2['SU'].sum()/1000


#%% GENERACION HIDRO

df = pd.read_csv('../BaseDatos_SDDP/rgerhid.csv', encoding='cp1252', index_col=0, header=3)
df.reset_index(level =0, inplace = True)
df = df.drop(['Ser.'], axis=1)
df.columns = df.columns.str.replace(' ', '')
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
    df = df.rename({i:j}, axis=1)

df = df.groupby(level=0, axis=1).sum()


mask = (df['Etap'] > 156)
df2 = df.loc[mask]

ghidroce  = df2['CE'].sum()/1000
ghidrono  = df2['NO'].sum()/1000
ghidroor  = 0
ghidrosu  = df2['SU'].sum()/1000

#%% GENERACION RENOVABLE

df = pd.read_csv('../BaseDatos_SDDP/rgergnd.csv', encoding='cp1252', index_col=0, header=3)
df.reset_index(level =0, inplace = True)
df = df.drop(['Ser.'], axis=1)
df.columns = df.columns.str.replace(' ', '')
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
    df = df.rename({i:j}, axis=1)

df = df.groupby(level=0, axis=1).sum()


mask = (df['Etap'] > 156)
df2 = df.loc[mask]

gvresce  = df2['CE'].sum()/1000
gvresno  = 0
gvresor  = df2['OR'].sum()/1000
gvressu  = df2['SU'].sum()/1000
#%% CONSTRUCCION DE TABLA
datat1 = data=[['CE',ghidroce,0,gtermoce,'-',gvresce,0],
               ['NO',ghidrono,0,gtermono,'-',gvresno,0],
               ['OR',ghidroor,0,gtermoor,'-',gvresor,0],
               ['SU',ghidrosu,0,gtermosu,'-',gvressu,0]]

tabla1=pd.DataFrame(datat1,columns = ['ZONA','GENERACION HIDRO [TWh]', 'EMISIONES CO2 HIDRO [MT]', 'GENERACION TERMO [TWh]', 'EMISIONES CO2 TERMO [MT]','GENERACION VRES [TWh]', 'EMISIONES CO2 VRES [MT]'])

tabla1.to_csv('../BaseDatos_DispaSET/Results/FINAL_SDDP/1.resumen.csv', header=True, index=True)









    
    
    
    
    
    
    
    
    
        

