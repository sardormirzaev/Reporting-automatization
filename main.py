# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 17:00:10 2020

@author: U0047365
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import function_0 as f0
import function_1 as f1
os.chdir("")  # Pfad eingeben

LCR=['Unnamed: 2','Unnamed: 16'] 
FCR=['Unnamed: 3','Unnamed: 17']
#%%
############################################## 

import1= 'sample10.xlsm' # Datei auswählen
select_model=FCR        # FCR oder LCR auswählen
#LCR

###############################################

#%%
print("Loading  the required datasets...")
df=pd.read_excel(import1,'Stichtagsdaten',encoding='utf-8', index=True)
df=df.iloc[1:,:]

pd_df=pd.read_excel(import1,'Masterskala',encoding='utf-8', index=True)
pd_df2=pd_df.iloc[1:,:].reset_index()

dfs=pd.DataFrame(df,columns=select_model)

dfs.columns=['ST1','ST2']
print("Loading is completed.")
#%%


###Matrixtabelle aufbauen

matrix_tabelle=migmatrix(dfs)

### Ratings Stufe und Anzahl

counted=abwechslung(dfs)

max_veschl_und_verb=maximal_zahlen(dfs)  

  

###ROC curve
plot_curve(dfs) 

### Trennschärfe Optimalmodell (AR) ###

A18,A19=AUC_AR_gemessen(dfs)
A19

### Trennschärfe Optimalmodell (AR) ###

A21=AR_optimal_model(dfs)    

A22=A19/A21  
A22

### Implizite Trennschärfe (AR) ###

pd_zu_stufe=pd_df2['Unnamed: 1']    # Die Verteiligung der Ausfallwahrscheinlichkeit auswählen

anz_klassen=matrix_tabelle.iloc[0:25,26]    # Stichtag 2 auswählen 

A24=AR_implizit(anz_klassen,pd_zu_stufe)

A25=A19/A24
A25

#%%
