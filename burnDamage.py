#importing necessary libraries
# from cmath import sin
from flask import Flask, jsonify, request,render_template
import pandas as pd

import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt


import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Load the trained model from the pickle file
with open('Damage_Classification_2.pkl', 'rb') as f:
    damage_classify_model = pickle.load(f)

with open('Fertilizer_Damage_Severity_Classification.pkl', 'rb') as f:
    fertilizer_burn_classify_model = pickle.load(f)

with open('Pesticide_Damage_Severity_Classification.pkl', 'rb') as f:
    pesticide_damage_classify_model = pickle.load(f)

def preprocess_image(image):
    img = image.convert("RGB")  # Convert image to RGB format
    img = img.resize((256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_preprocessed = tf.expand_dims(img_array, 0)
    return img_preprocessed

def burn_level(type , url):

    image_url = url

    class_names = ['100', '20', '40', '60', '80']
    
    # Access the value passed in the URL via the 'value' parameter
    
    uploaded_image_url = image_url
    #imge from url
    response = requests.get(uploaded_image_url)
    image = Image.open(BytesIO(response.content))
    uploaded_image = preprocess_image(image)

    if(type==0):
        print("Fertlizer burn level")
        prediction = fertilizer_burn_classify_model.predict(np.array(uploaded_image))
    else:
        print("Pesticide burn level")
        prediction = pesticide_damage_classify_model.predict(np.array(uploaded_image))
    print(prediction)
    top=np.argmax(prediction[0])
    print(class_names[top])
    return (class_names[top])

def damage_classify():
    json = request.get_json()
    print(json)

    print("asdt predict")
    image_url = request.get_json().get('url')
    # .args.get('url')
    class_names = ['Tomato_fertilizer_burn', 'Tomato_healthy', 'Tomato_pesticide_burn']
    
    # Access the value passed in the URL via the 'value' parameter
    
    uploaded_image_url = image_url
    #imge from url
    response = requests.get(uploaded_image_url)
    image = Image.open(BytesIO(response.content))
    uploaded_image = preprocess_image(image)

    prediction = damage_classify_model.predict(np.array(uploaded_image))
    print(prediction)
    top=np.argmax(prediction[0])
    print(class_names[top])
    if((top==0)|(top==2)):
        level=burn_level(top,uploaded_image_url)
        return ({"Prediction":str(top), "Level":level})

    return ({"Prediction":str(top)})
