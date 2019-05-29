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


     
dflabelbox["Quality"] = dflabelbox.Label.apply(get_class)
dflabelbox["File_Name"] = dflabelbox.External_ID.apply(get_filename)
dflabelbox["Frame_Number"] = dflabelbox.External_ID.apply(get_frame)

dflabelbox = dflabelbox.drop("Label", axis = 1)

dfnewheaders = ["Created_By","Quality", "External_ID", "File_Name", "Frame_Number"]

dfnew = dflabelbox.reindex(columns = dfnewheaders)




duplicateRowsDF = dfnew[dfnew.duplicated(["External_ID"], keep = False)]

dup_all = dfnew.duplicated(["External_ID"], keep = False)

# remove if reviewers disagree and actual reviewer is John Cull
dup_remove = dup_all & (dfnew.Created_By=='john.cull@prismahealth.org')

# creates the new clean dataframe
df_clean = dfnew.loc[~dup_remove]

df_clean.to_csv("listof_TrainandTestData.csv")