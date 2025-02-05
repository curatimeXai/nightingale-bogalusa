from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
from keras.models import load_model
from flask_cors import CORS
import io
import base64
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

# Load trained models
svm_model = joblib.load('models/svm_model.pkl')
xgb_model = joblib.load('models/xgb_model.pkl')
keras_model = load_model('models/keras_model.h5')
scaler = joblib.load('models/scaler.pkl')

@app.route('/')
def home():
    return "Welcome to the Heart Disease Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data from the request
    data = request.get_json()
    
    # Simulate model predictions 
    svm_prediction = 0  
    xgb_prediction = 1  
    keras_prediction = 0.75  
    
    # Generate the pie chart for each model prediction
    svm_pie_chart = create_pie_chart(svm_prediction, 'SVM Prediction')
    xgb_pie_chart = create_pie_chart(xgb_prediction, 'XGBoost Prediction')
    keras_pie_chart = create_pie_chart(keras_prediction, 'Keras Prediction')

    # Return the results along with the pie chart images (as base64-encoded strings)
    return jsonify({
        'svm_prediction': svm_prediction,
        'xgb_prediction': xgb_prediction,
        'keras_prediction': keras_prediction,
        'svm_pie_chart': svm_pie_chart,
        'xgb_pie_chart': xgb_pie_chart,
        'keras_pie_chart': keras_pie_chart
    })

def create_pie_chart(prediction, model_name):
    # Define the pie chart data
    if prediction == 0:
        data = [80, 20]  # Low risk and High risk percentages
    elif prediction == 1:
        data = [20, 80]
    else:
        data = [50, 50]  # For a value between 0 and 1
    
    labels = ['Low Risk', 'High Risk']
    colors = ['#36A2EB', '#FF5733']

    # Create a figure and a subplot
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Convert plot to an image in base64 format
    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')  # Base64-encoded string
    
    return img_base64

if __name__ == '__main__':
    app.run(debug=True)


