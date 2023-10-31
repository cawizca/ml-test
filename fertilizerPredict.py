from flask import Flask, jsonify, request
import pandas as pd
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Load the trained model from the pickle file
with open('Research_Random_forest.pkl', 'rb') as f:
    model = pickle.load(f)

def fertilizerPrediction():
    json = request.get_json()
    print(json)
    df = pd.DataFrame(json, index=[0])
    if(df.loc[0]['Deficiency Type']=='N'):
        df ['Deficiency Type_N'] = [True]
        df ['Deficiency Type_P'] = [False]
    elif(df.loc[0]['Deficiency Type']=='P'):
        df ['Deficiency Type_N'] = [False]
        df ['Deficiency Type_P'] = [True]
    df.drop(columns=["Deficiency Type"], inplace=True)
    print(df)
    single_pred = np.array(df).reshape(1,-1)
    prediction = model.predict(single_pred)
    prediction_str = prediction.tolist()
    res= {"Prediction" : prediction_str[0]}
    return (res)