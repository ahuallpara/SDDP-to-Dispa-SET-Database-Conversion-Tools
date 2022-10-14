# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 08:59:55 2022

@author: navia
"""

import numpy as np
import pandas as pd
from functools import reduce



hydro = pd.read_csv('../BaseDatos_SDDP/chidrobo.csv', encoding='cp1252', header=0)
hydro = hydro[['...Nombre...','....Pot','.VInic.']]
hydro = hydro.rename({'...Nombre...':'Unit','....Pot':'PowerCapacity','.VInic.':'Vol'}, axis=1)	


##eliminar generadores con capacidad 0
indexNames = hydro[hydro['PowerCapacity'] == 0].index
hydro.drop(indexNames , inplace=True)
hydro = hydro.drop(['PowerCapacity'], axis=1)

hydro = hydro.transpose()

hydro.reset_index(level =0, inplace = True)
hydro = hydro.drop(['index'], axis=1)
hydro.columns = hydro.iloc[0]
hydro = hydro[1:]
reslev = hydro

i=0

for i in range(8760):
    reslev = reslev.append(hydro)

#crear df con estampa de tiempo

reslev['Datetime'] = pd.date_range(start='2025-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H')
reslev['Datetime'] = pd.to_datetime(reslev['Datetime'])
reslev = reslev.rename({'Datetime':'TIMESTAMP'}, axis=1)	


reslev.set_index('TIMESTAMP',inplace=True, drop=True)


reslev.to_csv('../BaseDatos_DispaSET/ReservoirLevels/ReservoirLevels.csv')












