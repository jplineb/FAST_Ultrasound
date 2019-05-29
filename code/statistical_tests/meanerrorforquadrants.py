# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:50:13 2019

@author: jplineb
"""


### equation one is for average error calc by mean*abs(predicted-1)


import pandas as pd
import numpy as np
import json
import os


# Load in the data #
filesindir = os.listdir()
csvlocation = './quadrant_confidence.csv'
df = pd.read_csv(csvlocation)
df.head()

# look at json format #
test_case = df.predicted_class[4]

# Creating a function to grab scores and qualities from json output #

def get_score(score_json):
    scores = json.loads(score_json)
    watson_tuples = []
    for d in scores:
        watson_tuples.append((int(d['class'].split(' ')[1]), d['score']))
        
    conf_wt_avg = 0
    wt_sum = 0
    for q, c in watson_tuples:
        conf_wt_avg+=c*q
        wt_sum+=c
        
    conf_wt_avg = conf_wt_avg/wt_sum
    
    return(conf_wt_avg)

df["predicted_qual"] = df.predicted_class.apply(get_score)
df['actual_qual'] = df.actual_class.apply(lambda x: int(x.split(' ')[1]))

def abserror(predic_qual_score, actual_qual_score):
    calc_abs_error = abs(predic_qual_score-actual_qual_score)
    
    return calc_abs_error


df["absolute error"] = df.apply(lambda x: abserror(x.predicted_qual, x.actual_qual),axis=1)

df=df.groupby(['actual_class', 'Quadrant']).agg("mean").reset_index()

allq_avg_abs_error = df["absolute error"].mean()

# Creating a pivot table

dfpivot = df.pivot_table(values = ["absolute error"], index = ["actual_class", "Quadrant"])

dfpivot.to_csv("mean_abserror_results_Quadrants.csv")




#df2 = df.set_index("actual_class", drop = False)
#
#qualities = ["Quality 1", "Quality 2", "Quality 3", "Quality 4", "Quality 5"]
#Avgerrorforeachqual = [0, 0, 0, 0, 0]



#for x in qualities:  Useless
#    alpha = df2.loc[x]
#    locinqualities = qualities.index(x)
#    Avgerrorforeachqual[locinqualities] = alpha["absolute error"].mean()

# Creating a second dataframe with actual_class as index #

#df2 = df.set_index("actual_class", drop = False)

#qualities = ["Quality 1", "Quality 2", "Quality 3", "Quality 4", "Quality 5"]
#meanforeachqual = [0, 0, 0, 0, 0]
#Avgerrorforeachqual = [0, 0, 0, 0, 0]


# for loop to creat a data frame for each quality level and grab scores #
#for x in qualities:
#    n = 0
#    z = 0
#    listofscores = [] # temporary list to store the confidence score for each attempt
#    equation1_error = [] # temporary list to store error 
#    charlie = df2.loc[x] # creates a data frame for each quality level
#    amount_of_rows = charlie.shape[0]
#    echo = charlie.values.tolist()
#    locinqualities = qualities.index(x)
#    while z <= (amount_of_rows - 1):
#        n = n + 1
#        jsonlang = echo[z][2]
#        outputs = get_score(jsonlang)
#        predscoreforclass = outputs[1][locinqualities]
#        listofscores.append(predscoreforclass)
#        z = z + 1
#    mean = sum(listofscores)/n
#    meanforeachqual[locinqualities] = mean
#    for gamma in listofscores:
#        equation1 = mean*abs(gamma - 1)
#        equation1_error.append(equation1)
#    Avgerrorforeachqual[locinqualities] = sum(equation1_error)
    
        
        
        
        
        
    