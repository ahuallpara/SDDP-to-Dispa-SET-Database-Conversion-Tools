# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 09:16:00 2022

@author: navia
"""

import numpy as np
import pandas as pd
from functools import reduce


hinflw = pd.read_csv('../BaseDatos_SDDP/hinflw_w.csv', encoding='cp1252', header=None)

chidrobo = pd.read_csv('../BaseDatos_SDDP/chidrobo.csv', encoding='cp1252', header=0)
chidrobo = chidrobo[['...Nombre...','.PV.']]
chidrobo = chidrobo.T
chidrobo.reset_index(level =0, inplace = True)
chidrobo = chidrobo.drop(['index'], axis=1)
target_row = 1
idx = [target_row] + [i for i in range(len(chidrobo)) if i != target_row]
chidrobo = chidrobo.iloc[idx]
chidrobo = chidrobo.reset_index(drop=True)

# chidrobo.columns = chidrobo.iloc[0]
# chidrobo = chidrobo[1:]
# chidrobo['Año'] = 'Year'
# chidrobo['Etapa'] = 'Week'
# column_to_move0 = chidrobo.pop('Año')
# chidrobo.insert(0, 'Año', column_to_move0)
# column_to_move1 = chidrobo.pop('Etapa')
# chidrobo.insert(1, 'Etapa', column_to_move1)

# chidrobo = pd.concat([chidrobo.columns.to_frame().T, chidrobo], ignore_index=True)
# chidrobo.columns = range(len(chidrobo.columns))


# frames = [chidrobo, hinflw]

# result = pd.concat(frames)
# result = result.drop(result.index[[0]])

# result.reset_index(level =0, inplace = True)
# result = result.drop(['index'], axis=1)
# result.columns = result.iloc[0]
# result = result[1:]

#%%
hinflw1 = hinflw.drop([0,1], axis=1)
hinflw1 = hinflw1.transpose()
hinflw1.reset_index(level =0, inplace = True)
hinflw1 = hinflw1.rename({0:'code'}, axis=1)	
hinflw1['code'] = hinflw1['code'].astype(int)
dfinf = hinflw1


chidrobo = chidrobo.transpose()
chidrobo = chidrobo.rename({0:'Unitcode', 1:'Unitname'}, axis=1)	


unitname = chidrobo.Unitname
unitname.to_dict()
unitname = np.asarray(unitname)
unitcode = chidrobo.Unitcode
unitcode.to_dict()
unitcode = np.asarray(unitcode)

for i, j in zip(unitcode, unitname):

    hinflw1['code'] = hinflw1['code'].replace(i,j, regex=False)

hinflw2= hinflw1.transpose()
hinflw2.reset_index(level =0, inplace = True)
hinflw2.columns = hinflw2.iloc[0]
hinflw2 = hinflw2[1:]
hinflw2.columns = hinflw2.iloc[0]
hinflw2 = hinflw2[1:]
hinflw2 = hinflw2.drop(['code'], axis=1)
hinflw2.reset_index(level =0, inplace = True)
hinflw2 = hinflw2.drop(['index'], axis=1)

dfcol = hinflw[[0,1]]
dfcol.columns = dfcol.iloc[0]
dfcol = dfcol[1:]
dfcol.reset_index(level =0, inplace = True)
dfcol = dfcol.drop(['index'], axis=1)

frames = [dfcol, hinflw2]

result = pd.concat(frames,axis=1)
result = result.rename({'Año':'Year', 'Etapa':'Week'}, axis=1)	

#CASCADE SYSTEMS

#SISTEMA CORANI
result['SIS'] = result['SIS']+result['COR']
result['SJS'] = result['SJS']+result['SIS']+result['FICTICIA']
result['SJE'] = result['SJE']+result['SJS']

#SISTEMA YURA
result['KIL'] = result['KIL']+result['CON']
result['LAN'] = result['LAN']+result['KIL']
result['PUH'] = result['PUH']+result['LAN']

#SISTEMA MISICUNI
result['MOLLE'] = result['MOLLE']+result['MIS']

#SISTEMA TAQUESI
result['CHJ'] = result['CHJ']+result['CHJLG']
result['YAN'] = result['YAN']+result['CHJ']

#SISTEMA ZONGO
result['TIQ'] = result['TIQ']+result['TIQLG']
result['BOT'] = result['BOT']+result['TIQ']+result['ZON']
result['CUT'] = result['CUT']+result['BOT']
result['SRO01'] = result['SRO01']+result['CUT']
result['SRO02'] = result['SRO02']+result['SRO02LG']
result['SAI'] = result['SAI']+result['SRO01']+result['SRO02']
result['CHU'] = result['CHU']+result['SAI']
result['HAR'] = result['HAR']+result['CHU']
result['CAH'] = result['CAH']+result['HAR']
result['HUA'] = result['HUA']+result['CAH']

#SISTEMA JUNTAS
result['JUN'] = result['JUN']+result['SEH']+result['JUNTAS_TO']

#SISTEMA MIGUILLAS
result['ANG'] = result['ANG']+result['ANGLG']
result['CHO'] = result['CHO']+result['ANG']+result['MIG']
result['CRB'] = result['CRB']+result['CHO']+result['CRBLG']
result['CARABUCO_TO'] = result['CARABUCO_TO']+result['CRB']
result['CHACAJAHU_TO'] = result['CHACAJAHU_TO']+result['CHUCALOMA_TO']
result['CALACHAKA_TO'] = result['CALACHAKA_TO']+result['CALACHAUM_LG']
result['UMAPALCA_CA'] = result['UMAPALCA_CA']+result['CARABUCO_TO']+result['CHACAJAHU_TO']+result['CALACHAKA_TO']
result['UMA'] = result['UMA']+result['UMAPALCA_CA']
result['PALILLA01_CA'] = result['PALILLA01_CA']+result['UMA']+result['CALACHAMI_TO']+result['JALANCHA_TO']
result['PALILLA02_CA'] = result['PALILLA02_CA']+result['PALILLA01_CA']+result['CHORO_TO']
result['PLD'] = result['PLD']+result['PALILLA02_CA']+result['KEWANI_TO']



#%%   QMAX HIDRO
qmaxhydro = pd.read_csv('../BaseDatos_SDDP/chidrobo.csv', encoding='cp1252', header=0)
qmaxhydro = qmaxhydro[['...Nombre...','.QMax..']]
qmaxhydro = qmaxhydro.T
qmaxhydro.reset_index(level =0, inplace = True)
qmaxhydro = qmaxhydro.drop(['index'], axis=1)
qmaxhydro.columns = qmaxhydro.iloc[0]
qmaxhydro = qmaxhydro[1:]

qmaxhydro['Año'] = 'Año'

df1 = pd.DataFrame()
df1['Year']  = [1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,
                1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,
                2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,
                2017,2018,2019,2020,2021]
df1['Año']  = 'Año'

df2 = pd.merge(df1, qmaxhydro, how="left", on=['Año'])
df2 = df2.drop(['Año'], axis=1)

#%%
# FPhydro = pd.read_csv('C:/Users/navia/Desktop/EJEMPLO/BaseDatos_SDDP/chidrobo.csv', encoding='cp1252', header=0)
# FPhydro = FPhydro[['...Nombre...','.FPMed.']]
# FPhydro = FPhydro.T
# FPhydro.reset_index(level =0, inplace = True)
# FPhydro = FPhydro.drop(['index'], axis=1)
# FPhydro.columns = FPhydro.iloc[0]
# FPhydro = FPhydro[1:]

# FPhydro['Año'] = 'Año'

# df3 = pd.DataFrame()
# df3['Year']  = [1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,
#                 1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,
#                 2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,
#                 2017,2018,2019,2020,2021]
# df3['Año']  = 'Año'

# df4 = pd.merge(df3, FPhydro, how="left", on=['Año'])
# df4 = df4.drop(['Año'], axis=1)

#%%

df_t = pd.DataFrame()

df_t['Datetime'] = pd.date_range(start='1978-12-31 23:00:00+00:00', end='2021-12-31 23:00:00+00:00', freq='W')
df_t['Datetime'] = pd.to_datetime(df_t['Datetime'])

 
df_t['Week'] = pd.DatetimeIndex(df_t.Datetime).week
df_t['Year'] = pd.DatetimeIndex(df_t.Datetime).year 
df_t = df_t.drop(df_t[df_t['Week']==53].index)
df_t.reset_index(level =0, inplace = True)
df_t = df_t.drop(['index'], axis=1)


  
dfqmax = pd.merge( df_t, df2,  how="left", on=['Year'])
dfqmax = dfqmax.drop(dfqmax[dfqmax['Week']==53].index)
dfqmax.reset_index(level =0, inplace = True)
dfqmax = dfqmax.drop(['index'], axis=1)
dfqmax = dfqmax.fillna(0)
dfqmax = dfqmax.drop(['Year', 'Week'], axis=1)
dfqmax.set_index('Datetime', inplace = True)


# dfFP = pd.merge( df_t, df4,  how="left", on=['Year'])
# dfFP = dfFP.drop(dfFP[dfFP['Week']==53].index)
# dfFP.reset_index(level =0, inplace = True)
# dfFP = dfFP.drop(['index'], axis=1)
# dfFP = dfFP.fillna(0)
# dfFP = dfFP.drop(['Year', 'Week'], axis=1)
# dfFP.set_index('Datetime', inplace = True)


# multiplicar y dividir result * dfFP / dfpot


frames = [df_t, result]

result1 = pd.concat(frames, axis=1)
result1 = result1.fillna(0)
result1 = result1.drop(['Year', 'Week'], axis=1)
result1 = result1.rename({'Datetime':'TIMESTAMP'}, axis=1)	
result1.set_index('TIMESTAMP',inplace=True, drop=True)


#result1 = result1.drop(result1.index[[0]])

# result2 = result1.mul (dfFP)
result3 = result1.div (dfqmax)
result3 = result3.fillna(0)



df_t1 = pd.DataFrame()

df_t1['Datetime'] = pd.date_range(start='1978-12-31 23:00:00+00:00', end='2021-12-31 23:00:00+00:00', freq='H')
df_t1['Datetime'] = pd.to_datetime(df_t1['Datetime'])

 
df_t1['Week'] = pd.DatetimeIndex(df_t1.Datetime).week
df_t1['Year'] = pd.DatetimeIndex(df_t1.Datetime).year 
df_t1 = df_t1.drop(df_t1[df_t1['Week']==53].index)
df_t1.reset_index(level =0, inplace = True)
df_t1 = df_t1.drop(['index'], axis=1)
df_t1 = df_t1.drop(['Year', 'Week'], axis=1)
df_t1 = df_t1.rename({'Datetime':'TIMESTAMP'}, axis=1)	
df_t1.set_index('TIMESTAMP',inplace=True, drop=True)


result4 = df_t1.join(result3, how="outer")
#%%
ScaledInflows = result4.interpolate()

ScaledInflows.reset_index(level =0, inplace = True)
ScaledInflows = ScaledInflows.drop(['TIMESTAMP'], axis=1)

ScaledInflows['Datetime'] = pd.date_range(start='1979-02-25 23:00:00+00:00', end='2021-12-31 23:00:00+00:00', freq='H')
ScaledInflows['Datetime'] = pd.to_datetime(ScaledInflows['Datetime'])
ScaledInflows = ScaledInflows.rename({'Datetime':'TIMESTAMP'}, axis=1)	

#########FILTRAR FECHAS Y ELIMINAR LO QUE NO SIRVE como si fuera 2026
ScaledInflows.reset_index(inplace = True)
mask1 = (ScaledInflows['TIMESTAMP'] > '2020-12-31 22:00:00+00:00') & (ScaledInflows['TIMESTAMP'] <= '2021-12-31 23:00:00+00:00')
si2026 = ScaledInflows.loc[mask1]
si2026['Datetime'] = pd.date_range(start='2025-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
si2026['Datetime'] = pd.to_datetime(si2026['Datetime'])
si2026 = si2026.drop(['TIMESTAMP','ANGLG','CRBLG','TIQLG','SRO02LG','CHJLG','CALACHAUM_LG','CALACHAKA_TO',
                        'CHUCALOMA_TO','CHACAJAHU_TO','CARABUCO_TO','UMAPALCA_CA','PALILLA01_CA',
                        'JALANCHA_TO','CALACHAMI_TO','PALILLA02_CA','CHORO_TO','KEWANI_TO',
                        'JUNTAS_TO','FICTICIA','MOLLE'], axis=1)
si2026 = si2026.rename({'Datetime':'TIMESTAMP'}, axis=1)	
si2026.set_index('TIMESTAMP',inplace=True, drop=True)
si2026 = si2026.drop(['index'], axis=1)




si2026.to_csv('../BaseDatos_DispaSET/ScaledInflows/ScaledInflows_cascade.csv')

       
##########FILTRAR 2021 Y ELIMINAR LO QUE NO SIRVE 

average_by_year = pd.DataFrame({'Year':1979,'Count CE':0,'Count NO':0,'Count SU':0,
                                'Average CE':0,'Average NO':0,'Average SU':0,'Std CE':0,'Std NO':0,'Std SU':0,
                                'Min CE':0,'Min NO':0,'Min SU':0,'25% CE':0,'25% NO':0,'25% SU':0,
                                '50% CE':0,'50% NO':0,'50% SU':0,'75% CE':0,'75% NO':0,'75% SU':0,
                                'Max CE':0,'Max NO':0,'Max SU':0}, index=[0])

for k in range(1980,2022):
    mask1 = (ScaledInflows['TIMESTAMP'] > str(k-1)+'-12-31 22:00:00+00:00') & (ScaledInflows['TIMESTAMP'] <= str(k)+'-12-31 23:00:00+00:00')
    sinfl = ScaledInflows.loc[mask1]

    sinfl = sinfl.drop(['ANGLG','CRBLG','TIQLG','SRO02LG','CHJLG','CALACHAUM_LG','CALACHAKA_TO',
                        'CHUCALOMA_TO','CHACAJAHU_TO','CARABUCO_TO','UMAPALCA_CA','PALILLA01_CA',
                        'JALANCHA_TO','CALACHAMI_TO','PALILLA02_CA','CHORO_TO','KEWANI_TO',
                        'JUNTAS_TO','FICTICIA','MOLLE'], axis=1)

    sinfl.set_index('TIMESTAMP',inplace=True, drop=True)
    sinfl = sinfl.drop(['index'], axis=1)
    
    sinfl.to_csv('../BaseDatos_DispaSET/ScaledInflows/'+ str(k) +'.csv')
    
    #POWERPLANT to zones
    df1 = pd.read_csv('../BaseDatos_DispaSET/PowerPlantData/PowerPlantData_AREAS.csv', encoding='cp1252')
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
        sinfl = sinfl.rename({i:j}, axis=1)

    sinfl = sinfl.groupby(level=0, axis=1).sum()

    sinflzones = sinfl[['CE','NO','SU']]
    

    average = pd.DataFrame({'Year':k,'Count CE':sinflzones['CE'].count(),'Count NO':sinflzones['NO'].count(),'Count SU':sinflzones['SU'].count(),
                            'Average CE':sinflzones['CE'].mean(),'Average NO':sinflzones['NO'].mean(),'Average SU':sinflzones['SU'].mean(),
                            'Std CE':sinflzones['CE'].std(),'Std NO':sinflzones['NO'].std(),'Std SU':sinflzones['SU'].std(),
                            'Min CE':sinflzones['CE'].min(),'Min NO':sinflzones['NO'].min(),'Min SU':sinflzones['SU'].min(),
                            '25% CE':sinflzones['CE'].quantile(.25),'25% NO':sinflzones['NO'].quantile(.25),'25% SU':sinflzones['SU'].quantile(.25),
                            '50% CE':sinflzones['CE'].quantile(.50),'50% NO':sinflzones['NO'].quantile(.50),'50% SU':sinflzones['SU'].quantile(.50),
                            '75% CE':sinflzones['CE'].quantile(.75),'75% NO':sinflzones['NO'].quantile(.75),'75% SU':sinflzones['SU'].quantile(.75),
                            'Max CE':sinflzones['CE'].max(),'Max NO':sinflzones['NO'].max(),'Max SU':sinflzones['SU'].max()}, index=[0])
    average_by_year =  average_by_year.append(average)
    
    
    sinflzones.to_csv('../BaseDatos_DispaSET/ScaledInflows/'+ str(k) +'_zones.csv')

average_by_year.to_csv('../BaseDatos_DispaSET/ScaledInflows/AverageByYear.csv')


