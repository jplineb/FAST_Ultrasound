# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:00:56 2019

@author: John Paul
"""

import csv
import os
import shutil

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

with open('export.csv', 'r') as f:
    reader = csv.reader(f)
    thelist = list(reader)
    
print(thelist)
quality1list = []
quality2list = []
quality3list = []
quality4list = []
quality5list = []
frameswantedquality1 = []
frameswantedquality2 = []
frameswantedquality3 = []
frameswantedquality4 = []
frameswantedquality5 = []



for x in thelist:
    for a in x:
        if '"quality_level":"quality_1"' in a:
            quality1list.append(x)
        if '"quality_level":"quality_2"' in a:
            quality2list.append(x)
        if '"quality_level":"quality_3"' in a:
            quality3list.append(x)
        if '"quality_level":"quality_4"' in a:
            quality4list.append(x)
        if '"quality_level":"quality_5"' in a:
            quality5list.append(x)
            
            
for x in quality1list:
    a = x[9]
    frameswantedquality1.append(a)
for x in quality2list:
    a = x[9]
    frameswantedquality2.append(a)
for x in quality3list:
    a = x[9]
    frameswantedquality3.append(a)
for x in quality4list:
    a = x[9]
    frameswantedquality4.append(a)
for x in quality5list:
    a = x[9]
    frameswantedquality5.append(a)
    

for root, dirs, files in os.walk(fetchloc):
    for file in files:
        if file.endswith(tuple(frameswantedquality1)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality1)
        if file.endswith(tuple(frameswantedquality2)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality2)
        if file.endswith(tuple(frameswantedquality3)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality3)
        if file.endswith(tuple(frameswantedquality4)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality4)
        if file.endswith(tuple(frameswantedquality5)):
            frameloc = os.path.join(root, file)
            shutil.copy(frameloc, labeledquality5)
        

def find_duplicate_bf(A):
    n = len(A)
    for i in range(n):
        for j in range(i+1,n):
            if A[i] == A[j]:
                return A[i]
            
find_duplicate_bf(frameswantedquality1)


            
#framecompare = list(set(frameswantedcrap) & set(frameswantednotcrap)) # compares the lists for anyh overlap
#for root, dirs, files in os.walk(newsavecrap): #  deletes the overlapped frame in the crap folder
#    for file in files:
#        if file.endswith(tuple(framecompare)):
#            frameloc = os.path.join(root, file)
#            os.remove(frameloc)
            