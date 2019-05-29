# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:50:51 2019

@author: jplineb
"""
import pandas as pd
import json
import os



wrkingdir = os.getcwd()
filesindir = os.listdir()
dflabelbox = pd.read_csv("labelbox_outputs.csv")
dflabelbox = dflabelbox.drop(["ID", "DataRow ID", "Labeled Data",
                              "Project Name", "Created At", "Seconds to Label", "Agreement",
                              "Dataset Name", "Reviews", "View Label"], axis=1)


dflabelbox = dflabelbox.set_index("Label", drop=False)
dflabelbox = dflabelbox.drop("Skip", axis = 0)
dflabelbox = dflabelbox.reset_index(drop=True)
dflabelbox.columns = [c.replace(' ', '_') for c in dflabelbox.columns]

test_case = dflabelbox.Label[60]

def get_class(alpha):
    outputs = json.loads(alpha)
    
    quality_level = ((int(outputs['quality_level'].split('_')[1])))
    
    return(quality_level)
    
a = get_class(test_case)

def get_filename(beta):
    filename= beta.split('_')[0]
    
    return filename

def get_frame(charlie):
    frame = charlie.split('__')[1]
    
    return frame

def emailtoname(email):
    if email == 'john.cull@prismahealth.org':
        name = 'John Cull'
    if email == 'dustin.morrow@prismahealth.org':
        name = 'Dustin Morrow'
    return name

def absoluteerror(x,y):
    error = abs(x - y)
    return error


     
dflabelbox["Quality"] = dflabelbox.Label.apply(get_class)
dflabelbox["File_Name"] = dflabelbox.External_ID.apply(get_filename)
dflabelbox["Frame_Number"] = dflabelbox.External_ID.apply(get_frame)
dflabelbox["Created_By"] = dflabelbox.Created_By.apply(emailtoname)


dflabelbox = dflabelbox.drop("Label", axis = 1)

dfnewheaders = ["Created_By","Quality", "External_ID", "File_Name", "Frame_Number"]

dfnew = dflabelbox.reindex(columns = dfnewheaders)

dfpivot = dfnew.pivot_table(index = 'External_ID', columns = 'Created_By', values = 'Quality')
dfpivot = dfpivot.dropna()
dfpivot = dfpivot.reset_index(drop = False)
dfpivot = dfpivot.sort_values("External_ID")
dfpivot = dfpivot[dfpivot['Dustin Morrow'] != dfpivot['John Cull']]

Disagreements = './Disagreements/'

if not os.path.exists(Disagreements):
    os.makedirs(Disagreements)

newfilenames = []
for x in range(len(dfpivot["External_ID"])):
    name = 'A' + str(x) + '.png'
    newfilenames.append(name)

dfpivot["SimpFileName"] = newfilenames
    
dfpivot.to_csv("DisagreementFilelist_Master.csv")
dfpivot.to_excel("DisagreementFilelist.xlsx")

fileswanted = dfpivot.External_ID.tolist()
for root, dirs, files in os.walk(r'C:\Users\jplineb\Desktop\FAST_Watson\FASTFRAMES8'):
    for file in files:
        if file.endswith(tuple(fileswanted)):
            oldlocation = os.path.join(root, file)
            simpfilename = dfpivot.loc[dfpivot.External_ID == file]['SimpFileName']
            simpfilename = simpfilename.tolist()[0]
            newlocation = os.path.join(Disagreements, simpfilename)
            os.rename(oldlocation, newlocation)
            
            





