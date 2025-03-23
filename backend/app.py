from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import joblib
import numpy as np
from keras.models import load_model
from flask_cors import CORS
import io
import shap
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__,static_folder ="static")
CORS(app, origins=["http://localhost:8080", "https://xai-heart-disease-app-206040473281.europe-north2.run.app"])

# Load trained models
svm_model = joblib.load('models/svm_model.pkl')
xgb_model = joblib.load('models/xgb_model.pkl')
keras_model = load_model('models/keras_model.h5')
scaler = joblib.load('models/scaler.pkl')

@app.route('/')
def home():
    #return "Welcome to the Heart Disease Prediction API!"
    return send_from_directory('static', 'index.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from frontend request (JSON format)
        data = request.get_json()
        print("Received data:", data)

        # Define mappings for categorical variables (convert text to numerical values)
        gender_map = {'Male': 1, 'Female': 0}
        smoking_map = {'Not at all': 0, 'Sometimes': 1, 'Everyday': 2}

        # Convert user input into a DataFrame
        input_data = {
            'Gender': gender_map.get(data['Gender'], 0),# Convert gender to numeric
            'BMI': float(data['BMI']),# Convert BMI to float
            'Smoking': smoking_map.get(data['Smoking'], 0),# Convert smoking to numeric
            'Alcohol': float(data['Alcohol']),  # Convert alcohol consumption to float
            'Sleep': float(data['Sleep']), # Convert sleep hours to float
            'Exercise': float(data['Exercise']),# Convert exercise frequency to float
            'Fruit': float(data['Fruit']),# Convert fruit intake to float
            'Diabetes': int(data['Diabetes']),# Convert diabetes (0/1)
            'Kidney': int(data['Kidney']),# Convert kidney disease (0/1)
            'Stroke': int(data['Stroke'])# Convert stroke history (0/1)
        }
        print("Processed input data:", input_data)

        # Convert dictionary into a Pandas DataFrame for model compatibility
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
        svm_pred = float(svm_model.predict_proba(input_scaled)[0][1]) # SVM prediction probability
        xgb_pred = float(xgb_model.predict_proba(input_scaled)[0][1]) # XGBoost prediction probability
        keras_pred = float(keras_model.predict(input_scaled)[0][0]) # Keras model probability
        print(f"SVM prediction: {svm_pred}, XGBoost prediction: {xgb_pred}, Keras prediction: {keras_pred}")

        # Convert prediction probability to "Up" (High Risk) or "Down" (Low Risk)
        svm_label = get_thumb_value(svm_pred)
        xgb_label = get_thumb_value(xgb_pred)
        keras_label = get_thumb_value(keras_pred)

        # Generate pie charts for risk visualization
        svm_pie_chart = create_pie_chart(svm_pred, "SVM Prediction")
        xgb_pie_chart = create_pie_chart(xgb_pred, "XGBoost Prediction")
        keras_pie_chart = create_pie_chart(keras_pred, "Keras Prediction")
        # Get SHAP feature impact for the current prediction
        shap_explanation = get_shap_explanation(input_scaled)

        # Return JSON response with predictions, labels, charts, and SHAP values
        return jsonify({
           "shap_impact": shap_explanation["feature_impact"], 
            "shap_plot": shap_explanation["shap_plot"],
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
    """
    Convert probability into a risk label:
    - If probability is >= 0.5, return "Up" (High Risk)
    - Otherwise, return "Down" (Low Risk)
    """
   
    return "Up" if probability >= 0.5 else "Down"

def create_pie_chart(probability, title):
    """
    Generate a pie chart that visualizes heart disease risk probability.

    Parameters:
    - probability (float): Predicted risk score (between 0 and 1).
    - title (str): Title for the pie chart.

    Returns:
    - A base64-encoded string of the pie chart image (for frontend display).
    """
    labels = ["No Risk", "High Risk"] # Labels for pie chart segments
    sizes = [1 - probability, probability] # Size of "No Risk" vs "High Risk"
    colors = ["green", "red"] # Green for low risk, red for high risk
    # Create a pie chart figure
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax.set_title(title)

    # Save to a buffer
    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)
    buf.seek(0)
    
    # Encode to base64 for sending to frontend
    img_base64 = base64.b64encode(buf.read()).decode('utf-8') 
    
    return img_base64
def get_shap_explanation(input_scaled):
    """Get SHAP explanation for the input data"""
    # Use the TreeExplainer for XGBoost model
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(input_scaled)

    # Calculate feature impact for the first instance
    individual_shap_values = shap_values[0]  # Getting SHAP values for the first data point
    feature_impact = {scaler.feature_names_in_[i]: individual_shap_values[i] for i in range(len(scaler.feature_names_in_))}
    # Convert feature_impact values to native Python float
    feature_impact = {k: float(v) for k, v in feature_impact.items()}
    # Generate SHAP summary plot
    plt.figure()
    shap.summary_plot(shap_values, input_scaled, feature_names=scaler.feature_names_in_,show=False)
    
    # Save to buffer and encode for frontend use
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    shap_plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
    print(f"SHAP plot base64 length: {len(shap_plot_base64)}") 
    return {"feature_impact": feature_impact, "shap_plot": shap_plot_base64}

if __name__ == '__main__':
    app.run(debug=True)




