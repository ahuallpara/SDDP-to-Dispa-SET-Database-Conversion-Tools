# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:03:17 2022

@author: navia
"""
import pandas as pd
import numpy as np

#from datetime import datetime
df = pd.read_csv('../BaseDatos_SDDP/dcirc.csv', encoding='cp1252')
#df=pd.read_csv("C:/Users/navia/Dispa-SET_ENDE/ConversionTools/DataBase_SDDP/dcirc.csv",sep=';',encoding='latin-1')
df=df[['Nome........','(  MW)']]
df['NOMBRE2']=df['Nome........'].str.slice(stop=3)
df['NOMBRE3']=df['Nome........'].str.slice(start=3,stop=6)
df['NOMBRE4']=df['Nome........'].str.slice(start=6,stop=9)
df['NOMBRE5']=df['Nome........'].str.slice(start=9,stop=12)
df1=pd.concat([pd.DataFrame(df['NOMBRE2'] + '-' + df['NOMBRE3']+' -> '+ df['NOMBRE4'] + '-' + df['NOMBRE5']),df[['(  MW)']]],axis=1)
df1.columns=['A','(  MW)']
df2=pd.concat([pd.DataFrame(df['NOMBRE4'] + '-' + df['NOMBRE5']+' -> '+ df['NOMBRE2'] + '-' + df['NOMBRE3']),df[['(  MW)']]],axis=1)
df2.columns=['A','(  MW)']
df1['Nro']=np.arange(1,len(df1)+1)
df2['Nro']=np.arange(1,len(df1)+1)
df3=pd.concat([df1,df2])
df3.sort_values(['Nro'],inplace=True)
df4=df3[['A','(  MW)']]
df5=df4.T
df5.columns = df5.iloc[0]
df5=df5.drop('A')
df_t=pd.date_range(start='2021-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
df5=pd.concat([df5]*(df_t.shape[0]),ignore_index=False)
df5['Datetime']=df_t
column_to_move0 = df5.pop('Datetime')
df5.insert(0, 'Datetime', column_to_move0)
df5=df5.reset_index()
df5 = df5.drop(['index'], axis=1)
df5 = df5.rename({'Datetime':'TIMESTAMP'}, axis=1)	

##########FILTRAR FECHAS Y ELIMINAR LO QUE NO SIRVE

mask1 = (df5['TIMESTAMP'] > '2025-12-31 22:00:00+00:00') & (df5['TIMESTAMP'] <= '2026-12-31 23:00:00+00:00')
df5 = df5.loc[mask1]
#######RENOMBRAR BUSES QUE CAUSAN PROBLEMAS

df6 = df5.rename({'MON-115 -> GBE-115':'MOE-115 -> GBE-115','GBE-115 -> MON-115':'GBE-115 -> MOE-115',
                 'ARB-115 -> MON-115':'ARB-115 -> MOE-115','MON-115 -> ARB-115':'MOE-115 -> ARB-115',
                 'CHN-115 -> MON-115':'CHN-115 -> MOE-115','MON-115 -> CHN-115':'MOE-115 -> CHN-115',
                 'MON-115 -> MIN-115':'MOE-115 -> MIN-115','MIN-115 -> MON-115':'MIN-115 -> MOE-115',
                 'LCA-230 -> THU-230':'LCA-230 -> TOH-230','THU-230 -> LCA-230':'TOH-230 -> LCA-230',
                 'LIT-230 -> THU-230':'LIT-230 -> TOH-230','THU-230 -> LIT-230':'TOH-230 -> LIT-230',
                 'THU-069 -> THU-230':'TOH-069 -> TOH-230','THU-230 -> THU-069':'TOH-230 -> TOH-069',
                 'CHL-069 -> THU-069':'CHL-069 -> TOH-069','THU-069 -> CHL-069':'TOH-069 -> CHL-069',
                 'CHL-069 -> THU-069':'CHL-069 -> TOH-069','THU-069 -> CHL-069':'TOH-069 -> CHL-069',
                 'PAR-069 -> CAÑ-069':'PAR-069 -> CAN-069','CAÑ-069 -> PAR-069':'CAN-069 -> PAR-069',
                 'CAÑ-069 -> FER-069':'CAN-069 -> FER-069','FER-069 -> CAÑ-069':'FER-069 -> CAN-069'
                 }, axis=1)

df6.set_index('TIMESTAMP',inplace=True, drop=True)
ntc = df6  
 
df3 = ntc
df4= df3.transpose()
df4.reset_index(level =0, inplace = True)
buslist = pd.read_csv('../BaseDatos_DispaSET/BusList-ZONES1.csv', encoding='cp1252')

busname = buslist.Busname
busname.to_dict()
busname = np.asarray(busname)
zone = buslist.Zone
zone.to_dict()
zone = np.asarray(zone)
for i, j in zip(busname, zone):
    df4['A'] = df4['A'].str.replace(i,j, regex=False)

df5= df4.transpose()
df5.columns = df5.iloc[0]
df5 = df5[1:]
df6 = df5.groupby(level=0, axis=1).sum()
df7 = df6.drop(['CE -> CE', 'NO -> NO', 'SU -> SU','OR -> OR'], axis=1)

df7.to_csv('../BaseDatos_DispaSET/NTC/NTC_AREAS.csv') 