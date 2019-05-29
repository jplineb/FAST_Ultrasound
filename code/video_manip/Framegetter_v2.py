# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:00:56 2019

@author: John Paul
"""

import csv
import os
import shutil
import pandas as pd
from collections import Counter

wrkingdirect = os.getcwd()
sourcefolder = '/FASTFRAMES8/'

fetchloc = wrkingdirect + sourcefolder
labeledquality1 = wrkingdirect + '/labeledquality1/'
labeledquality2 = wrkingdirect + '/labeledquality2/'
labeledquality3 = wrkingdirect + '/labeledquality3/'
labeledquality4 = wrkingdirect + '/labeledquality4/'
labeledquality5 = wrkingdirect + '/labeledquality5/'

if not os.path.exists(labeledquality1):
    os.makedirs(labeledquality1)
if not os.path.exists(labeledquality2):
    os.makedirs(labeledquality2)
if not os.path.exists(labeledquality3):
    os.makedirs(labeledquality3)
if not os.path.exists(labeledquality4):
    os.makedirs(labeledquality4)
if not os.path.exists(labeledquality5):
    os.makedirs(labeledquality5)

with open('listof_TrainandTestData.csv', 'r') as f:
    reader = csv.reader(f)
    thelist = list(reader)
    

quality1list = []
quality2list = []
quality3list = []
quality4list = []
quality5list = []




for x in thelist:
    if x[2] == '1':
        quality1list.append(x[3])
    if x[2] == '2':
        quality2list.append(x[3])
    if x[2] == '3':
        quality3list.append(x[3])
    if x[2] == '4':
        quality4list.append(x[3])
    if x[2] == '5':
        quality5list.append(x[3])
            
            


for root, dirs, files in os.walk(fetchloc):
    for file in files:
        if file.endswith(tuple(quality1list)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality1)
        if file.endswith(tuple(quality2list)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality2)
        if file.endswith(tuple(quality3list)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality3)
        if file.endswith(tuple(quality4list)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality4)
        if file.endswith(tuple(quality5list)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality5)
        

def get_dupes(l):
    return [k for k, v in Counter(l).items() if v > 1]

dupes = get_dupes(quality1list)

#def find_duplicate_bf(A):
#    n = len(A)
#    for i in range(n):
#        for j in range(i+1,n):
#            if A[i] == A[j]:
#                return A[i]
#            
#find_duplicate_bf(frameswantedquality1)


            
#framecompare = list(set(frameswantedcrap) & set(frameswantednotcrap)) # compares the lists for anyh overlap
#for root, dirs, files in os.walk(newsavecrap): #  deletes the overlapped frame in the crap folder
#    for file in files:
#        if file.endswith(tuple(framecompare)):
#            frameloc = os.path.join(root, file)
#            os.remove(frameloc)
            