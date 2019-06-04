# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 13:39:36 2019

@author: jplineb
"""
import os
import pandas as pd
from ibm_watson import VisualRecognitionV3

wrkingdir = os.getcwd()
datasetloc = './FASTFRAMES8'

### Identifying Unused Current Data ###
used_data_df = pd.read_csv("listof_TrainandTestData.csv")
lsofuseddata = used_data_df.External_ID.tolist()

filesindataset = []
for root, dirs, files in os.walk(datasetloc):
    for file in files:
        filesindataset.append(file)
lsofunusedata = [x for x in filesindataset if x not in lsofuseddata]
lsoffileswthpaths = []
for z in lsofunusedata:
    z = datasetloc + '/' + z
    lsoffileswthpaths.append(z)
amount_imgs = len(lsoffileswthpaths)
Watsontestdf = pd.DataFrame([],columns = ["Filename", "Quality_1", "Quality_2", "Quality_3",
                             "Quality_4", "Quality_5", "Predicted_Quality"])
#########################################

##### API ussage ###########
visual_recognition = VisualRecognitionV3('2018-03-19', 
                                         url='https://gateway.watsonplatform.net/visual-recognition/api',
                                         iam_apikey='mXPz9F8EB1_I3HqVMyvC-aYF_3_D43xEI3cJyge7lX7x')
outputs = []
ctr = 0
batch1 = lsoffileswthpaths[0:5000]
batch2 = lsoffileswthpaths[5000:10000]
batch3 = lsoffileswthpaths[10000:15000]
batch4 = lsoffileswthpaths[15000:]
def watsonimageclass(test):
    ctr = 0
    print("Processing Image", "of", ctr, amount_imgs )
    print(test)
    with open(test,'rb') as image_file:
        try:
            classes = visual_recognition.classify(image_file, threshold= '0',
                                                  owner=["me"],
                                                  classifier_ids='Testclassifier_2146332589').get_result()
        except Exception as e:
            print("Something went wrong! Error:", e)
            print('frame')
            print(test)
            classes = []
        ctr+= 1
    return classes


############################
    

### Thread Pool Executor Code ###
from concurrent.futures import ThreadPoolExecutor

# send rows to Watson Visual Recognition asynchronously
nthread=30
batchstr = 'batch_4'
batchnum = batch4 # defines batch number 
with ThreadPoolExecutor(max_workers=nthread) as executor: 
    futures = executor.map(watsonimageclass, batchnum) 
    
# turn futures generator into list of results
list_results = []
for r in futures:
	list_results.append(r)
    
# converts the results to an item on the dataframe    
for classes in list_results:
    if not classes == []:
        outputs = (classes['images'][0])
        predicted_img_class_watson = outputs['classifiers'][0]['classes']
        img_name = outputs['image']
        Watsontestdf = Watsontestdf.append({'Filename': img_name,
                                        'Quality_1':predicted_img_class_watson[0]["score"],
                                        'Quality_2':predicted_img_class_watson[1]["score"],
                                        'Quality_3':predicted_img_class_watson[2]["score"],
                                        'Quality_4':predicted_img_class_watson[3]["score"],
                                        'Quality_5':predicted_img_class_watson[4]["score"]}, ignore_index = True)

#################################


### Getting Prediction Score ###       
def getpredictedscore(q1, q2, q3, q4, q5):
    pq = (q1*1+q2*2+q3*3+q4*4+q5*5)
    return pq


Watsontestdf["Predicted_Quality"] = Watsontestdf.apply(lambda x: getpredictedscore(x.Quality_1, x.Quality_2, x.Quality_3, x.Quality_4, x.Quality_5), axis = 1)
################################



csv_name = ('./modelresults_unuseddata' + batchstr + '.csv')
Watsontestdf.to_csv(csv_name ) # exporting to csv            