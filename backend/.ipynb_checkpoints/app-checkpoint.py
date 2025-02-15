from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
from keras.models import load_model
from flask_cors import CORS
import io
import base64
import matplotlib
matplotlib.use('Agg')
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
    try:
        # Get user input from frontend
        data = request.get_json()
        print("Received data:", data)

        # Mappings for categorical data
        gender_map = {'Male': 1, 'Female': 0}
        smoking_map = {'Not at all': 0, 'Sometimes': 1, 'Everyday': 2}

        # Convert user input into a DataFrame
        input_data = {
            'Gender': gender_map.get(data['Gender'], 0),
            'BMI': float(data['BMI']),
            'Smoking': smoking_map.get(data['Smoking'], 0),
            'Alcohol': float(data['Alcohol']),
            'Sleep': float(data['Sleep']),
            'Exercise': float(data['Exercise']),
            'Fruit': float(data['Fruit']),
            'Diabetes': int(data['Diabetes']),  # Ensure int type
            'Kidney': int(data['Kidney']),      # Ensure int type
            'Stroke': int(data['Stroke'])       # Ensure int type
        }
        print("Processed input data:", input_data)

        # Convert to DataFrame
        df_input = pd.DataFrame([input_data])

        # Apply one-hot encoding (same as training)
        df_input = pd.get_dummies(df_input)

        # Ensure all expected features are present
        for col in scaler.feature_names_in_:
            if col not in df_input.columns:
                df_input[col] = 0  # Add missing columns

        # Ensure correct column order
        df_input = df_input[scaler.feature_names_in_]

        # Scale input
        input_scaled = scaler.transform(df_input)
        print("Scaled input data:", input_scaled)

        # Get predictions (convert NumPy float32 to Python float)
        svm_pred = float(svm_model.predict_proba(input_scaled)[0][1])
        xgb_pred = float(xgb_model.predict_proba(input_scaled)[0][1])
        keras_pred = float(keras_model.predict(input_scaled)[0][0])  # Ensure float type

        print(f"SVM prediction: {svm_pred}, XGBoost prediction: {xgb_pred}, Keras prediction: {keras_pred}")

        # Convert predictions into "Up" or "Down"
        svm_label = get_thumb_value(svm_pred)
        xgb_label = get_thumb_value(xgb_pred)
        keras_label = get_thumb_value(keras_pred)

        # Generate pie charts
        svm_pie_chart = create_pie_chart(svm_pred, "SVM Prediction")
        xgb_pie_chart = create_pie_chart(xgb_pred, "XGBoost Prediction")
        keras_pie_chart = create_pie_chart(keras_pred, "Keras Prediction")

        # Return predictions as Python native float values for serialization
        return jsonify({
            "svm_prediction": float(svm_pred),  # Explicit conversion to float
            "xgb_prediction": float(xgb_pred),  # Explicit conversion to float
            "keras_prediction": float(keras_pred),  # Explicit conversion to float
            "svm_label": svm_label,
            "xgb_label": xgb_label,
            "keras_label": keras_label,
            "svm_pie_chart": svm_pie_chart,
            "xgb_pie_chart": xgb_pie_chart,
            "keras_pie_chart": keras_pie_chart
        })

    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def get_thumb_value(probability):
    """Convert probability into 'Up' or 'Down' label"""
    return "Up" if probability >= 0.5 else "Down"

def create_pie_chart(probability, title):
    """Generate a pie chart showing risk probability"""
    labels = ["No Risk", "High Risk"]
    sizes = [1 - probability, probability]
    colors = ["green", "red"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax.set_title(title)

    # Save to a buffer
    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)
    buf.seek(0)
    
    # Encode to base64 for sending to frontend
    encoded_img = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded_img}"


if __name__ == '__main__':
    app.run(debug=True)




