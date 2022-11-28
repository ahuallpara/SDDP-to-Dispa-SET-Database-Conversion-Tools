# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 16:06:36 2022

@author: UMSS
"""
import numpy as np
import pandas as pd

sddpflw = pd.read_csv('../SDDP_FLOWS/rgerhid.csv', encoding='cp1252', header=3)
Installed_cap=pd.read_csv('../SDDP_FLOWS/chidrobo.csv',encoding='cp1252')
Installed_cap=Installed_cap[['....Pot']]
sddpflwy1 =pd.DataFrame(sddpflw.iloc[:260].sum()*1000)  
sddpflwy2=pd.DataFrame(sddpflw.iloc[261:521].sum()*1000)  
sddpflwy3=pd.DataFrame(sddpflw.iloc[520:780].sum()*1000) 
sddpflwy4 = pd.DataFrame(sddpflw.iloc[780:].sum()*1000)
gen=pd.concat([sddpflwy1,sddpflwy2,sddpflwy3,sddpflwy4],axis=1)
gen=gen.drop(['Etap','Ser.','Bloq'],axis=0)
gen.columns=['y1','y2','y3','y4']
gen=gen.reset_index()
CF=gen.iloc[:,1:].div((Installed_cap['....Pot']*365*24), axis=0)
CF.index=gen['index']
CF=CF.fillna(0)
CF.to_csv('../SDDP_FLOWS/CapacityFactor.csv')
