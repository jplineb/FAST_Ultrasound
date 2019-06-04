# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:37:54 2019

@author: jplineb
"""

import os
import pandas as pd
import pickle
import random
import shutil

wrkingdir = os.getcwd()
framedir = '../FASTFRAMES8/'

### Load data ###
df_frames = pd.read_csv('./modelresults_all.csv') # Reads dataframe from csv
loaded_model = pickle.load(open('LRmodel.sav', 'rb')) # loads model using pickle
#################

### Get model predictions ###
x_test = df_frames.iloc[:,3:8].values # is array
y_test_pred = loaded_model.predict(x_test)
roundedpredict = []
for z in range(len(y_test_pred)):
    if y_test_pred[z] < 1:
        num = 1
    elif y_test_pred[z] > 5:
        num = 5
    else:
        num = round(y_test_pred[z])      
    roundedpredict.append(num)
        
        
df_frames['Calib_Predict'] = y_test_pred
df_frames['Calib_Rounded_Predict'] = roundedpredict

df1 = df_frames.loc[df_frames['Calib_Rounded_Predict'] == 1]
df2 = df_frames.loc[df_frames['Calib_Rounded_Predict'] == 2]
df3 = df_frames.loc[df_frames['Calib_Rounded_Predict'] == 3]
df4 = df_frames.loc[df_frames['Calib_Rounded_Predict'] == 4]
df5 = df_frames.loc[df_frames['Calib_Rounded_Predict'] == 5]

### Get frames and store them ###
quality1 = df1.Filename.tolist()
quality2 = df2.Filename.tolist()
quality3 = df3.Filename.tolist()
quality4 = df4.Filename.tolist()
quality5 = df5.Filename.tolist()

quality1 = random.sample(quality1, 500)
quality2 = random.sample(quality2, 500)
quality3 = random.sample(quality3, 500)
quality4 = random.sample(quality4, 500)
quality5 = random.sample(quality5, 500)

newfolders = ['Quality_1_Predict', 'Quality_2_Predict', 'Quality_3_Predict',
              'Quality_4_Predict', 'Quality_5_Predict']

for x in newfolders:
    x = wrkingdir + '/' + x
    if not os.path.exists(x):
        os.makedirs(x)
        
for root, dirs, files in os.walk(framedir):
    for file in files:
        if file.endswith(tuple(quality1)):
            frameloc = os.path.join(root,file)
            dest = './Quality_1_Predict/' + file
            shutil.copy(frameloc, dest)
        if file.endswith(tuple(quality2)):
            frameloc = os.path.join(root,file)
            dest = './Quality_2_Predict/' + file
            shutil.copy(frameloc, dest)
        if file.endswith(tuple(quality3)):
            frameloc = os.path.join(root,file)
            dest = './Quality_3_Predict/' + file
            shutil.copy(frameloc, dest)
        if file.endswith(tuple(quality4)):
            frameloc = os.path.join(root,file)
            dest = './Quality_4_Predict/' + file
            shutil.copy(frameloc, dest)
        if file.endswith(tuple(quality5)):
            frameloc = os.path.join(root,file)
            dest = './Quality_5_Predict/' + file
            shutil.copy(frameloc, dest)
        
            