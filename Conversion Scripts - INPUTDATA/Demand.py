# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 18:04:10 2021

@author: MARCO NAVIA
"""
import numpy as np
import pandas as pd
from functools import reduce



df = pd.read_csv('../BaseDatos_SDDP/dbf005bo.csv', encoding='cp1252', index_col=0)
df['Datetime'] = pd.to_datetime(dict(year=df['yyyy'], month=df['mm'], day=df['dd']))
df1 = df.rename({'Bus name':'Busname'}, axis=1)	
df1['Busname']  = df1['Busname'].str.rstrip(' ')
df1 = df1.drop(['Load code', 'dd', 'mm', 'yyyy', 'Load shedding flag'], axis=1)
Busname_datalist = df1.Busname.unique()
Busname_datalist = Busname_datalist[:, np.newaxis].T

df2 = []
for i in Busname_datalist[0]:
    
    df2.append(df1.loc[df1['Busname'] == i])
    

df3 = []
df4 = []

for c in df2:
    
    df3.append(c.rename({'Load(MW)': c.iat[0,0]}, axis=1))	
    
for e in df3:
    df4.append(e.drop(['Busname'], axis=1))
  
data_merge = reduce(lambda left, right: pd.merge(left, right, on=('Datetime', 'Block'), how='outer'), df4)
data_merge['Weekday'] = pd.DatetimeIndex(data_merge.Datetime).weekday
data_merge['Week'] = pd.DatetimeIndex(data_merge.Datetime).week
data_merge['Year'] = pd.DatetimeIndex(data_merge.Datetime).year


column_to_move0 = data_merge.pop('Year')
data_merge.insert(0, 'Year', column_to_move0)
column_to_move1 = data_merge.pop('Week')
data_merge.insert(1, 'Week', column_to_move1)
column_to_move2 = data_merge.pop('Block')
data_merge.insert(2, 'Block', column_to_move2)

data_merge = data_merge.drop(['Datetime', 'Weekday'], axis=1)

#aumentando la semana 53
mask = (data_merge['Year'] == 2026) & (data_merge['Week'] == 52)
filtered_data_merge = data_merge.loc[mask]
filtered_data_merge['Week'] = filtered_data_merge['Week'].replace(52,53) 
data_merge = data_merge.append(filtered_data_merge)
########

df_t = pd.DataFrame()

df_t['Datetime'] = pd.date_range(start='2021-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
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
df_t['Year'] = pd.DatetimeIndex(df_t.Datetime).year   
   

column_to_move0 = df_t.pop('Year')
df_t.insert(0, 'Year', column_to_move0)
column_to_move1 = df_t.pop('Week')
df_t.insert(1, 'Week', column_to_move1)
column_to_move2 = df_t.pop('Block')
df_t.insert(2, 'Block', column_to_move2)

df_t = df_t.drop(['Hour','Weekday'], axis=1)


demand = pd.merge( df_t, data_merge,  how="left", on=['Year','Week', 'Block'])
column_to_move1 = demand.pop('Datetime')
demand.insert(0, 'Datetime', column_to_move1)

demand = demand.drop(['Year', 'Week','Block'], axis=1)
demand = demand.rename({'Datetime':'TIMESTAMP'}, axis=1)	
mask1 = (demand['TIMESTAMP'] > '2025-12-31 22:00:00+00:00') & (demand['TIMESTAMP'] <= '2026-12-31 23:00:00+00:00')
filtered_demand = demand.loc[mask1]
filtered_demand = filtered_demand.fillna(0)
filtered_demand.set_index('TIMESTAMP',inplace=True, drop=True)

#MISSING BUSES

df10 = filtered_demand.columns.unique()
df10 = pd.DataFrame(df10, columns=['Busname'])


dfc = pd.read_csv('../BaseDatos_SDDP/dcirc.csv', encoding='cp1252')

dfc=dfc[['Nome........','(  MW)']]
dfc['NOMBRE2']=dfc['Nome........'].str.slice(stop=3)
dfc['NOMBRE3']=dfc['Nome........'].str.slice(start=3,stop=6)
dfc['NOMBRE4']=dfc['Nome........'].str.slice(start=6,stop=9)
dfc['NOMBRE5']=dfc['Nome........'].str.slice(start=9,stop=12)
df1c=pd.concat([pd.DataFrame(dfc['NOMBRE2'] + '-' + dfc['NOMBRE3'])],axis=1)
df2c=pd.concat([pd.DataFrame(dfc['NOMBRE4'] + '-' + dfc['NOMBRE5'])],axis=1)

frames = (df1c,df2c)
df3c = pd.concat(frames, axis = 0)
df3c.columns=['Busname']

BusList = df3c.Busname.unique()
BusList = pd.DataFrame(BusList, columns=['Busname'])

frames = (df10,BusList)
df3a = pd.concat(frames, axis = 0)
df3a.columns=['Busname']

#df4 = df3.Busname.unique()
#df4 = pd.DataFrame(df4, columns=['Busname'])
df3a['Duplicated'] = df3a.duplicated(keep=False)


condicion = (df3a['Duplicated']==False)

df4a = df3a[condicion]
df4a.reset_index(level =0, inplace = True)
df4a = df4a.drop(['index'], axis=1)


MissingDemand = df4a.transpose()
MissingDemand.columns = MissingDemand.iloc[0]
MissingDemand = MissingDemand[1:]
frames = (filtered_demand,MissingDemand)
finaldemand = pd.concat(frames, axis = 1)
finaldemand = finaldemand.fillna(0)
#RENAME BUSBARS THAT HAVE PROBLEMS 

finaldemand = finaldemand.rename({'CAÑ-069':'CAN-069','MON-115':'MOE-115','THU-069':'TOH-069','THU-230':'TOH-230'}, axis=1)


finaldemand['TIMESTAMP'] = pd.date_range(start='2025-12-31 23:00:00+00:00', end='2027-01-01 00:00:00+00:00', freq='H')
finaldemand['TIMESTAMP'] = pd.to_datetime(finaldemand['TIMESTAMP'])
mask1 = (finaldemand['TIMESTAMP'] > '2025-12-31 22:00:00+00:00') & (finaldemand['TIMESTAMP'] <= '2026-12-31 23:00:00+00:00')
finaldemand = finaldemand.loc[mask1]
finaldemand.reset_index(level =0, inplace = True)
finaldemand = finaldemand.drop(['index'], axis=1)
finaldemand.set_index('TIMESTAMP',inplace=True, drop=True)	

df = finaldemand
buslist = pd.read_csv('../BaseDatos_DispaSET/BusList-ZONES1.csv', encoding='cp1252')
df1 = df
busname = buslist.Busname
busname.to_dict()
busname = np.asarray(busname)
zone = buslist.Zone
zone.to_dict()
zone = np.asarray(zone)
for i, j in zip(busname, zone):
    df1 = df1.rename({i:j}, axis=1)

df2 = df1.groupby(level=0, axis=1).sum()



df2.to_csv('../BaseDatos_DispaSET/Demand/Demand_AREAS.csv')
    
    
    
    
    
    
    
    
        

