# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:55:37 2019

@author: John Paul
"""
# Cell Dedicated to imports #
import os
import json
from watson_developer_cloud import VisualRecognitionV3
from prettytable import PrettyTable
import pandas as pd
import time

# Defining Locations #
Quality1_folder = './Quality1_Test/'
Quality2_folder = './Quality2_Test/'
Quality3_folder = './Quality3_Test/'
Quality4_folder = './Quality4_Test/'
Quality5_folder = './Quality5_Test/'

Test_imgs_Quality1 = os.listdir(Quality1_folder) # list test img names
Test_imgs_Quality2 = os.listdir(Quality2_folder)
Test_imgs_Quality3 = os.listdir(Quality3_folder)
Test_imgs_Quality4 = os.listdir(Quality4_folder)
Test_imgs_Quality5 = os.listdir(Quality5_folder)

FASTWATSON8_test_img_loc_Quality1 = [('Quality 1', Quality1_folder + x) for x in Test_imgs_Quality1] # stores the location of each image 
FASTWATSON8_test_img_loc_Quality2 = [('Quality 2', Quality2_folder + x) for x in Test_imgs_Quality2]
FASTWATSON8_test_img_loc_Quality3 = [('Quality 3', Quality3_folder + x) for x in Test_imgs_Quality3]
FASTWATSON8_test_img_loc_Quality4 = [('Quality 4', Quality4_folder + x) for x in Test_imgs_Quality4]
FASTWATSON8_test_img_loc_Quality5 = [('Quality 5', Quality5_folder + x) for x in Test_imgs_Quality5]

FASTWATSON8_test_img_loc = FASTWATSON8_test_img_loc_Quality1 + FASTWATSON8_test_img_loc_Quality2 + FASTWATSON8_test_img_loc_Quality3 + FASTWATSON8_test_img_loc_Quality4 + FASTWATSON8_test_img_loc_Quality5
amount_imgs = len(FASTWATSON8_test_img_loc) # check step

# Visual Recognition Test #
visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey='1ZWY-v59DKJKTLQnOfbolRls0CxukEmsJoKtSHzjtZ7T')

outputs = []
results = pd.DataFrame([], columns = ['actual_class', 'predicted_class', 'score', 'img_name'])
Images_ran = 0

ctr = 0
for z in FASTWATSON8_test_img_loc:  
    print("Processing image", ctr+1, "of" ,amount_imgs)
    with open(z[1], 'rb') as image_file:
        try:
            classes = visual_recognition.classify(image_file, threshold= '0', owners=["me"]).get_result()
            outputs = (classes['images'][0])
            predicted_img_class_watson = outputs['classifiers'][0]['classes']
            img_name = outputs['image']
            results = results.append({'actual_class': z[0],  
                            'predicted_class': predicted_img_class_watson, 
                            'score': score, 
                            'img_name': img_name}, ignore_index = True)
        except:
            time.sleep(5)
            print('Classification call put to sleep due to error')
            print('frame')
            print(img_name)
    ctr = ctr + 1
results.to_csv('./test_results.csv')



        

        
        