# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:03:17 2022

@author: navia
"""
import pandas as pd
import numpy as np

#from datetime import datetime
df = pd.read_csv('../BaseDatos_SDDP/rcirflw.csv', encoding='cp1252', header=3)
df = df.drop('Ser.',axis=1)
df = df.transpose()
df = df.reset_index()
df['index'] = df['index'].astype(str) 



# df=df[['index','(  MW)']]
df['NOMBRE2']=df['index'].str.slice(stop=3)
df['NOMBRE3']=df['index'].str.slice(start=3,stop=6)
df['NOMBRE4']=df['index'].str.slice(start=6,stop=9)
df['NOMBRE5']=df['index'].str.slice(start=9,stop=12)
df1=pd.concat([pd.DataFrame(df['NOMBRE2'] + '-' + df['NOMBRE3']+' -> '+ df['NOMBRE4'] + '-' + df['NOMBRE5']),df],axis=1)
df2=pd.concat([pd.DataFrame(df['NOMBRE4'] + '-' + df['NOMBRE5']+' -> '+ df['NOMBRE2'] + '-' + df['NOMBRE3']),df*(-1)],axis=1)
df1 = df1.drop('index',axis=1)
df4 = df1.transpose()
df4.columns = df4.iloc[0]
df4 = df4[1:]
df4 = df4.rename({'Eta-p -> -':'Week','Blo-q -> -':'Block',
                  'MON-115 -> GBE-115':'MOE-115 -> GBE-115','GBE-115 -> MON-115':'GBE-115 -> MOE-115',
                  'ARB-115 -> MON-115':'ARB-115 -> MOE-115','MON-115 -> ARB-115':'MOE-115 -> ARB-115',
                  'CHN-115 -> MON-115':'CHN-115 -> MOE-115','MON-115 -> CHN-115':'MOE-115 -> CHN-115',
                  'MON-115 -> MIN-115':'MOE-115 -> MIN-115','MIN-115 -> MON-115':'MIN-115 -> MOE-115',
                  'LCA-230 -> THU-230':'LCA-230 -> TOH-230','THU-230 -> LCA-230':'TOH-230 -> LCA-230',
                  'LIT-230 -> THU-230':'LIT-230 -> TOH-230','THU-230 -> LIT-230':'TOH-230 -> LIT-230',
                  'THU-069 -> THU-230':'TOH-069 -> TOH-230','THU-230 -> THU-069':'TOH-230 -> TOH-069',
                  'CHL-069 -> THU-069':'CHL-069 -> TOH-069','THU-069 -> CHL-069':'TOH-069 -> CHL-069',
                  'CHL-069 -> THU-069':'CHL-069 -> TOH-069','THU-069 -> CHL-069':'TOH-069 -> CHL-069',
                  'CAÑ-069 -> FER-069':'CAN-069 -> FER-069','PAR-069 -> CAÑ-069':'PAR-069 -> CAN-069'
                   }, axis=1)

df4= df4.transpose()
df4 = df4.rename({0:'Zero'}, axis=1)
df4.reset_index(level =0, inplace = True)
df4 = df4.rename({0:'index'}, axis=1)
buslist = pd.read_csv('../BaseDatos_DispaSET/BusList-ZONES1.csv', encoding='cp1252')

busname = buslist.Busname
busname.to_dict()
busname = np.asarray(busname)
zone = buslist.Zone
zone.to_dict()
zone = np.asarray(zone)
for i, j in zip(busname, zone):
    df4['index'] = df4['index'].str.replace(i,j, regex=False)
df4 = df4.rename({'Zero':0}, axis=1)
df4 = df4.drop(['NOMBRE2', 'NOMBRE3', 'NOMBRE4','NOMBRE5'], axis=1)
df5= df4.transpose()
df5.columns = df5.iloc[0]
df5 = df5[1:]
df6 = df5.groupby(level=0, axis=1).sum()

df7 = df6.drop(['CE -> CE', 'NO -> NO', 'SU -> SU','OR -> OR'], axis=1)

df8 = df7.rename({'CE -> NO':'NO','CE -> OR':'OR', 'CE -> SU':'SU', 'NO -> CE':'CE','OR -> NO':'NO'}, axis=1)
df9 = df8.groupby(level=0, axis=1).sum()
column_to_move = df9.pop('Week')
df9.insert(0, 'Week', column_to_move)
column_to_move1 = df9.pop('Block')
df9.insert(1, 'Block', column_to_move1)


df10 = df7.rename({'CE -> NO':'CE','CE -> OR':'CE', 'CE -> SU':'CE', 'NO -> CE':'NO','OR -> NO':'OR'}, axis=1)
df11 = df10.groupby(level=0, axis=1).sum()
df12 = df11* (-1)
df12['Week'] = df12['Week']*(-1) 
df12['Block'] = df12['Block']*(-1) 
column_to_move = df12.pop('Week')
df12.insert(0, 'Week', column_to_move)
column_to_move1 = df12.pop('Block')
df12.insert(1, 'Block', column_to_move1)
df12 = df12.rename({'Week':'Week1','Block':'Block1'}, axis=1)

frames = (df9, df12)
df = pd.concat(frames, axis = 1)
df = df.drop(['Week1', 'Block1'], axis=1)
df = df.groupby(level=0, axis=1).sum()
column_to_move = df.pop('Week')
df.insert(0, 'Week', column_to_move)
column_to_move1 = df.pop('Block')
df.insert(1, 'Block', column_to_move1)


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

 
    
df5 = df2.interpolate(method='linear', limit_direction='forward', axis=0)   
    
flowout = df5.where(df5 <= 0,  0)

flowin = df5.where(df5 >= 0,  0)


flowout.to_csv('../BaseDatos_DispaSET/Results/FINAL_SDDP/OuputFlowOut.csv', header=True, index=True)

flowin.to_csv('../BaseDatos_DispaSET/Results/FINAL_SDDP/OuputFlowIn.csv', header=True, index=True)


