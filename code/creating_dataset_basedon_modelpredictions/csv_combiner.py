# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:23:52 2019

@author: jplineb
"""


import pandas as pd


df1 = pd.read_csv('modelresults_unuseddatabatch_1.csv')
df2 = pd.read_csv('modelresults_unuseddatabatch_2.csv')
df3 = pd.read_csv('modelresults_unuseddatabatch_3.csv')
df4 = pd.read_csv('modelresults_unuseddatabatch_4.csv')

df1 = df1.append([df2, df3, df4])

df1.to_csv('modelresults_all.csv')