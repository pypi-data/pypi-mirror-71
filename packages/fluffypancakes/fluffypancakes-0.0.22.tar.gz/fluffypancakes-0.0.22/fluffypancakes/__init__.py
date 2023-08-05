# -*- coding: utf-8 -*-
"""
@authors: Suhas Sharma and Rahul P
"""

import numpy as np
import pandas as pd
import pathlib
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

from features import Features

def serve(url, progressBar=True):
    dataset = str(pathlib.Path(__file__).parent.absolute()) + r'/data/dataset.csv'
    data = pd.read_csv(dataset)
    # Selecting required columns
    x = data.iloc[:,1:-1]
    y = data.iloc[:,-1]
    
    # Preprocessing
    x = x.dropna()
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    
    # Feature Extraction        
    output_vector = Features().extract_features(url, progressBar)
    
    if(type(output_vector)!=str):
        output_vector = [output_vector]
        
        output_vector = np.asarray(output_vector)
        
        model = RandomForestClassifier(n_estimators = 30, oob_score = True, n_jobs = -1, random_state = 101, max_features = None, min_samples_leaf = 2)
        model.fit(x, y)
        
        prediction = model.predict(output_vector)
        prediction = prediction[0]
    else:
        prediction = output_vector

    return prediction
