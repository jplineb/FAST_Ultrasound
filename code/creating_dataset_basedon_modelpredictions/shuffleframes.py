# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:26:14 2019

@author: jplineb
"""

import os
import pandas as pd
import random
import shutil

loaddest = './labelbox_upload/'
savedest = './labelbox_upload_shuffle/'

files = os.listdir(loaddest)

randomfiles = random.sample(files, len(files))
newlynamed_randomfiles = []

for x in range(len(randomfiles)):
    x = 'A' + str(x) + '.png'
    newlynamed_randomfiles.append(x)



df = pd.DataFrame({"OG_Filename:" : files,
                   "Shuffled_names": randomfiles,
                   "New_Name" : newlynamed_randomfiles})

df.to_csv('filenameshuffle_dataframe.csv')



if not os.path.exists(savedest):
    os.makedirs(savedest)


for x,y in zip(files, newlynamed_randomfiles):
    x = loaddest + x
    y = savedest + y
    shutil.copy(x,y)
