# -*- coding: utf-8 -*-
"""
Created on Fri May 24 13:39:21 2019

@author: jplineb
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import confusion_matrix


df = pd.read_csv("FASTDataFrameNice.csv")
## Defining Pass or Fail Function ###
def passorfail(score):
    if score < 2.5: #Defines if score is fail --> 0
        grade = 0
    elif score >= 2.5: #Defines if score is pass --> 1
        grade = 1
        
    return grade

## Adding Pass or Fail Columns ###

df["actual_grade"] = df.actual_qual.apply(passorfail)
df["watson_predicted_grade"] = df.predicted_qual.apply(passorfail)

## Splitting Data ###

calib_frac = 0.33

figuresfromallruns = []
for a in range(0,1000):
     
    # Train test Split #
    df_train, df_test = train_test_split(df, test_size = 1-calib_frac)
    print(df_train.shape)
    
    # Grabbing off Pass or Fail Values #
        # Test Values #
    y_dftest = df_test.actual_grade.values
    x_dftest = df_test.iloc[:, 3:8].values
    
    
        # Train Values #
    y_dftrain = df_train.actual_grade.values
    x_dftrain = df_train.iloc[:, 3:8].values
    
    
    ## Train the calibration modle ##
    estim = LogisticRegression(fit_intercept = True, C=1e10)
    estim.fit(x_dftrain, y_dftrain)
    
    print(estim.coef_)
    
    ## Get Final Scores ##
    y_test_pred = estim.predict(x_dftest)
    print("The mean square error is:")
    print(np.sqrt(mean_squared_error(y_dftest, y_test_pred)))
    print("The mean absolute error is:")
    print(mean_absolute_error(y_dftest, y_test_pred))
    
    df_eval = pd.DataFrame(x_dftest)
    df_eval['y_test'] = y_dftest
    df_eval['y_test_pred'] = y_test_pred
    df_eval = df_eval.rename(columns = {0:'watson_grade'})
    df_fulltest = df_test.reset_index()
    df_fulltest['calibration_grade'] = y_test_pred
    df_fulltest.head()
    
    
    ## Visual Outputs ##
    
    ################## confusion matrix ####################
    
    def plot_confusion_matrix(y_true, y_pred,
#                              classes,
#                              normalize=False,
#                              title=None,
#                              cmap=plt.cm.Blues
                              ):
#        """
#        This function prints and plots the confusion matrix.
#        Normalization can be applied by setting `normalize=True`.
#        """
#        if not title:
#            if normalize:
#                title = 'Normalized confusion matrix'
#            else:
#                title = 'Confusion matrix, without normalization'
    
        # Compute confusion matrix
        cm = confusion_matrix(y_true, y_pred)
#        # Only use the labels that appear in the data
#        if normalize:
#            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
#            print("Normalized confusion matrix")
#        else:
#            print('Confusion matrix, without normalization')
#    
#        print(cm)
#    
#        fig, ax = plt.subplots()
#        im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
#        ax.figure.colorbar(im, ax=ax)
#        # We want to show all ticks...
#        ax.set(xticks=np.arange(cm.shape[1]),
#               yticks=np.arange(cm.shape[0]),
#               # ... and label them with the respective list entries
#               xticklabels=classes, yticklabels=classes,
#               title=title,
#               ylabel='True label',
#               xlabel='Predicted label')
#    
#        # Rotate the tick labels and set their alignment.
#        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#                 rotation_mode="anchor")
#    
#        # Loop over data dimensions and create text annotations.
#        fmt = '.2f' if normalize else 'd'
#        thresh = cm.max() / 2.
#        for i in range(cm.shape[0]):
#            for j in range(cm.shape[1]):
#                ax.text(j, i, format(cm[i, j], fmt),
#                        ha="center", va="center",
#                        color="white" if cm[i, j] > thresh else "black")
#        fig.tight_layout()
        return cm
     
    
    CalGrade = df_fulltest["calibration_grade"].values.tolist()
    #i = 0
    #for x in CalGrade:
    #    if x > .5:
    #        CalGrade[i] = 1
    #    elif x <= .5:
    #        CalGrade[i] = 0
    #    i = i + 1 
      
    TruGrade = df_fulltest['actual_grade'].values.tolist()
    
    CalConfMatrx = plot_confusion_matrix(TruGrade, CalGrade)
    
    WatsGrade = df_fulltest["watson_predicted_grade"].values.tolist()

    WatsConfMatrx = plot_confusion_matrix(TruGrade, WatsGrade)
    
    confusionfigs = [CalConfMatrx, WatsConfMatrx]
    
    figuresfromallruns.append(confusionfigs)
        



 

##############################################################################
    
##### Looking at Multiple Loops ######
i = 1
for x in figuresfromallruns:
    print("Confusion Matricies for Run " + str(i))
    print('\n'.join(map(str, x)))
    i = i + 1
    
    

##### Test #####
#alpha = figuresfromallruns[0][0]
#beta = figuresfromallruns[1][0]
#charlie = (alpha + beta)/2
################ 

##### Averaging the Results for the sum of the matricies from every loop #####
totalmatrix = np.zeros((2,2))
for x in figuresfromallruns:
    totalmatrix = totalmatrix + x[0]
Averagematrix = totalmatrix/(len(figuresfromallruns))
Averagematrix = Averagematrix.astype(int)

    ### Confusion Matrix Function ###
def plot_confusion_matrix_havematrix(cm, classes, normalize = False, title = None, cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

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
    return fig
    #################################
    
Averagematrixfig = plot_confusion_matrix_havematrix(Averagematrix,
                                                    classes = ["Pass", "Fail"],
                                                    title = "Average Calibrated Predictions")
plt.savefig("PoF_confusion_matrix_WOnorm.png")
AverageNormalizedConfusionMatrix = plot_confusion_matrix_havematrix(Averagematrix,
                                                    classes = ["Pass", "Fail"],
                                                    title = "Average Calibrated Predictions Normalized", normalize = True)
plt.savefig("PoF_confusion_matrix_norm.png")
    
    
    