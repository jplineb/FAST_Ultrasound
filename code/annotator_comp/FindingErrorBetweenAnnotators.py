# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:50:51 2019

@author: jplineb
"""
import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


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
dfpivot ['error'] = dfpivot.apply(lambda x: absoluteerror(x['Dustin Morrow'], x['John Cull']), axis = 1)
average_error = dfpivot.error.agg('mean')
dfdisaggree = dfpivot[dfpivot['Dustin Morrow'] != dfpivot['John Cull']]
disaggree_average_error = dfdisaggree.error.agg('mean')

###### Confusion Matrix Function ##############


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='Dustin Morrow',
           xlabel='John Cull')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


########################################################

DMorrow = dfpivot['Dustin Morrow']
JCull = dfpivot['John Cull']

    
Errorconfusionmatrix = plot_confusion_matrix(DMorrow, JCull, classes = ['Quality 1', 'Quality 2', 'Quality 3', 'Qualtiy 4', 'Quality 5'], title = 'Comparison of Annotators')
plt.savefig('Error_confusionmatrix_WOnorm.png')

ErrorconfusionmatrixNorm = plot_confusion_matrix(DMorrow, JCull, classes = ['Quality 1', 'Quality 2', 'Quality 3', 'Qualtiy 4', 'Quality 5'], title = 'Comparison of Annotators Normalized', normalize = True)
plt.savefig('Error_confusionmatrix_norm.png')

print('Average Error is: ' + str(average_error))
print('Average Error when different: ' + str(disaggree_average_error))






