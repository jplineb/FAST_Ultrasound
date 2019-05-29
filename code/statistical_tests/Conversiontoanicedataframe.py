# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:43:15 2019

@author: jplineb
"""

import pandas as pd
import os
import json

wrkingdirect = os.getcwd()

filesindir = os.listdir()
csvfile = "./test_results_doublequotes.csv"

df = pd.read_csv(csvfile)

qualities = ["Quality 1", "Quality 2", "Quality 3", "Quality 4", "Quality 5"]





def seperatescore(jsonoutputs):
    scores = json.loads(jsonoutputs)
    watson_tuples = []
    for d in scores:
        watson_tuples.append((d['class'], d['score']))
    
    watson_dict = dict((y, x) for y, x in watson_tuples)
    
    return watson_dict

#test_case = df.predicted_class[4]
#a = seperatescore(test_case)


#def get_score(score_json):
#    scores = json.loads(score_json)
#    watson_tuples = []
#    for d in scores:
#        watson_tuples.append((int(d['class'].split(' ')[1]), d['score']))
#        
#    conf_wt_avg = 0
#    wt_sum = 0
#    for q, c in watson_tuples:
#        conf_wt_avg+=c*q
#        wt_sum+=c
#        
#    conf_wt_avg = conf_wt_avg/wt_sum
#    
#    return(conf_wt_avg)

#df["predicted_qual"] = df.predicted_class.apply(get_score)
df['actual_qual'] = df.actual_class.apply(lambda x: int(x.split(' ')[1]))

        


df["dictscore"] = df.predicted_class.apply(seperatescore) 


def scoretocolumn(beta, gamma):
    score = beta[gamma]
    
    return score

#test_case2 = scoretocolumn(a,"Quality 1")

for x in qualities:
    df[x] = df.apply(lambda y: scoretocolumn(y.dictscore, x), axis = 1)
   
## Attempt at creating wt_avg 
def conf_wt_avg(x):
    print(x)
    conf_wt_avg_calc = 0
    wt_sum = 0
    n = 0
    for z in qualities:
        n+= 1
        a = x[z]

        conf_wt_avg_calc+= (n*a)
        wt_sum+=(a)
    
    conf_wt_avg_calc = conf_wt_avg_calc/wt_sum
    
    return(conf_wt_avg_calc)
    

 

df["predicted_qual"] = df.apply(conf_wt_avg, axis = 1)
#    

dfnewheaders = ["img_name", "actual_qual","Quality 1", "Quality 2", "Quality 3", "Quality 4", "Quality 5", "predicted_qual"]

df = df.drop(["predicted_class", "actual_class", "dictscore", "Unnamed: 0" ], axis = 1) 

dfnew = df.reindex(columns = dfnewheaders)

dfnew.to_csv("FASTDataFrameNice.csv")
     