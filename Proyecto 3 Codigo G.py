# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:39:39 2022

@author: Lbasper
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#nivel profesores
datos1 = pd.read_csv("Porcen_doc_2022_1.csv",encoding='latin-1',delimiter=";").fillna(0)
llav1=datos1.keys()
a=datos1[llav1[1]]/datos1[llav1[4]]
b=datos1[llav1[2]]/datos1[llav1[4]]
c=datos1[llav1[3]]/datos1[llav1[4]]
datos1=pd.concat([a,b,c],axis=1, join ='inner')


#sexo profesores de catedra
datos2 = pd.read_csv("Porcen_sexo_catedra_2022_1.csv",encoding='latin-1',delimiter=";").fillna(0)
llav2=datos2.keys()
a=datos2[llav2[2]]/datos2[llav2[4]]
b=datos2[llav2[3]]/datos2[llav2[4]]
datos2=pd.concat([a,b],axis=1, join ='inner').fillna(0)


#sexo profesores de planta
datos3 = pd.read_csv("Porcen_sexo_planta_2022_1.csv",encoding='latin-1',delimiter=";").fillna(0)
llav3=datos3.keys()
a=datos3[llav3[1]]/datos3[llav3[3]]
b=datos3[llav3[2]]/datos3[llav3[3]]
datos3=pd.concat([a,b],axis=1, join ='inner')


datospredic = pd.read_csv("Matriz doble programa.csv",encoding='latin-1',delimiter=";").fillna(0)
llavpredic=datospredic.keys()


for i in range(31):
    programa=i+1
    sumar=datospredic[llavpredic[programa]].sum()
    datospre=datospredic[llavpredic[programa]]/sumar

    # Columna 1_%doc,2_%maes,3_%esp/pre,4_%hombre_cat,5_%mujeres_cat,6_%hombre_plan,7_%mujer_plan
    X=pd.concat([datos1,datos2,datos3],axis=1, join ='inner',ignore_index=True)


    Y=datospre

    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score
    X_entreno,X_testeo, Y_entreno, Y_testeo=  train_test_split(X,Y, test_size=0.3)
    GB = GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.01)
    GB.fit(X_entreno, Y_entreno)
    r2_puntaje= r2_score(Y_testeo, GB.predict(X_testeo))
    t=GB.feature_importances_ *100
print(r2_puntaje)
print(t)
learning_rates = [0.01,0.1,1]
n_estimators = np.arange(1,220,20)

fig = plt.figure(figsize=(12,5))
for lr in learning_rates:
    r2_test = []
    r2_train = []

    for ne in n_estimators:
        GB = GradientBoostingRegressor(n_estimators=ne, learning_rate=lr)
        GB.fit(X_entreno, Y_entreno)
        r2_test.append( r2_score(Y_testeo, GB.predict(X_testeo)) )
        r2_train.append( r2_score(Y_entreno, GB.predict(X_entreno)) )
    
    plt.subplot(1,2,1)
    plt.plot(n_estimators,r2_test, label=f'lr:{lr}')
        
    plt.subplot(1,2,2)
    plt.plot(n_estimators,r2_train, label=f'lr:{lr}')
    plt.subplot(1,2,1)
    plt.grid()
    plt.legend()
    plt.xlabel('n_estimators')
    plt.ylabel('r2_test')
   
#Grafica las importancias en orden descendente
importances = GB.feature_importances_*100
predictors = X.keys()
plt.figure()
a = pd.Series([33.33303261,49.10290515,0.71836079,3.64632882,6.23594064,3.20792674,3.75550525], predictors)
a.plot(kind='barh')
plt.xlabel('Feature Importances')