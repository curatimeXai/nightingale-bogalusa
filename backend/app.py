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
CORS(app, origins=["http://localhost:8080"])

# Load trained models
svm_model = joblib.load('models/svm_model.pkl')
xgb_model = joblib.load('models/xgb_model.pkl')
keras_model = load_model('models/keras_model.h5')
scaler = joblib.load('models/scaler.pkl')

def calculate_risk_score(predictions):
    """Calculate weighted risk score from multiple models"""
    weights = {
        'svm': 0.3,
        'xgb': 0.4,
        'keras': 0.3
    }
    
    weighted_score = (
        predictions['svm'] * weights['svm'] +
        predictions['xgb'] * weights['xgb'] +
        predictions['keras'] * weights['keras']
    )
    
    return {
        'score': weighted_score,
        'level': get_risk_level(weighted_score),
        'description': get_risk_description(weighted_score)
    }

def get_risk_level(score):
    if score >= 0.75:
        return "high"
    elif score >= 0.5:
        return "mid"
    else:
        return "low"

def get_risk_description(score):
    if score >= 0.75:
        return "High cardiovascular risk important - Recommended medical consultation"
    elif score >= 0.5:
        return "Moderate cardiovascular risk - Recommended monitoring"
    else:
        return "Low cardiovascular risk - Maintaining good habits"

def analyze_lifestyle_factors(data):
    """Analyze individual lifestyle factors and provide recommendations"""
    analysis = []
    
    # BMI Analysis
    bmi = float(data['BMI'])
    if bmi >= 30:
        analysis.append({
            'factor': 'BMI',
            'status': 'Critique',
            'value': bmi,
            'recommendation': 'Recommended medical consultation for your management'
        })
    elif bmi >= 25:
        analysis.append({
            'factor': 'BMI',
            'status': 'À surveiller',
            'value': bmi,
            'recommendation': 'balanced diet and more exercise'
        })
    
    # Sleep Analysis
    sleep = float(data['Sleep'])
    if sleep < 6:
        analysis.append({
            'factor': 'Sommeil',
            'status': 'Insuffisant',
            'value': sleep,
            'recommendation': 'Increase your sleep time to 7-9 hours per night'
        })
    elif sleep > 9:
        analysis.append({
            'factor': 'Sommeil',
            'status': 'Excessif',
            'value': sleep,
            'recommendation': 'sleep can indicate other health problems'
        })
    # Exercise Analysis
    exercise = float(data['Exercise'])
    if exercise < 150:
        analysis.append({
            'factor': 'Activité physique',
            'status': 'Insuffisant',
            'value': exercise,
            'recommendation': 'Aim for at least 150 minutes of moderate activity per week'
        })
    
    return analysis

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
        print("Diabetes:", data['Diabetes'])  # Check raw input
        print("Processed Diabetes:", input_data['Diabetes'])  # After conversion


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
        
        predictions_dict = {
            'svm': float(svm_pred),
            'xgb': float(xgb_pred),
            'keras': float(keras_pred)
        }
        
        risk_assessment = calculate_risk_score(predictions_dict)
        lifestyle_analysis = analyze_lifestyle_factors(data)

        # Modifiez le retour JSON pour inclure les nouvelles informations
        return jsonify({
            "risk_assessment": risk_assessment,
            "lifestyle_analysis": lifestyle_analysis,
            "model_predictions": {
                "svm": {
                    "probability": float(svm_pred),
                    "label": svm_label
                },
                "xgb": {
                    "probability": float(xgb_pred),
                    "label": xgb_label
                },
                "keras": {
                    "probability": float(keras_pred),
                    "label": keras_label
                }
            },
            "shap_impact": shap_explanation["feature_impact"],
            "shap_plot": shap_explanation["shap_plot"],
            "shap_summary_text": shap_explanation["shap_summary_text"]
        })

    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
        # Return JSON response with predictions, labels, charts, and SHAP values
        return jsonify({
           "shap_impact": shap_explanation["feature_impact"], 
            "shap_plot": shap_explanation["shap_plot"],  
            "shap_summary_text": shap_explanation["shap_summary_text"],          
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
def summarize_shap_impact(feature_impact, top_n=3, exclude=["Age", "Gender"]):
    """
    Generate a summary sentence for the top features contributing to prediction.

    Args:
    - feature_impact (dict): feature -> SHAP value
    - top_n (int): number of top features to include
    - exclude (list): features to skip in the summary

    Returns:
    - summary_text (str): readable explanation
    """
    # Remove excluded features and sort by absolute impact
    filtered = {k: v for k, v in feature_impact.items() if k not in exclude}
    top_features = sorted(filtered.items(), key=lambda item: abs(item[1]), reverse=True)[:top_n]

    readable_names = [f.replace("_", " ").capitalize() for f, _ in top_features]

    if not readable_names:
        return "No strong influencing factors were identified in your prediction."

    return f"This result is mostly influenced by {', '.join(readable_names[:-1])}" + \
           (f", and {readable_names[-1]}." if len(readable_names) > 1 else f"{readable_names[0]}.")

def get_shap_explanation(input_scaled):
    """Get SHAP explanation for the input data"""
    # Use the TreeExplainer for XGBoost model
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(input_scaled)
    
    # Calculate feature impact for the first instance
    individual_shap_values = shap_values[0]  # Getting SHAP values for the first data point
    feature_names = scaler.feature_names_in_
    feature_impact = {feature_names[i]: float(individual_shap_values[i]) for i in range(len(feature_names))}
    shap_summary_text = summarize_shap_impact(feature_impact)
    # feature_impact = {scaler.feature_names_in_[i]: individual_shap_values[i] for i in range(len(scaler.feature_names_in_))}
    # Convert feature_impact values to native Python float
    #feature_impact = {k: float(v) for k, v in feature_impact.items()}
    # Generate SHAP summary plot
    #plt.figure()
   # shap.summary_plot(shap_values, input_scaled, feature_names=scaler.feature_names_in_,show=False)
    # --- Filter out "Age" and "Gender" ---
    filtered_features = [f for f in feature_impact if f not in ['Age', 'Gender']]
    filtered_values = [feature_impact[f] for f in filtered_features]

    colors = ['green' if val < 0 else 'red' for val in filtered_values]
    # --- Create SHAP Bar Chart (Horizontal) ---
    plt.figure(figsize=(10, 6))
   # features = list(feature_impact.keys())
   # values = list(feature_impact.values())
   # colors = ['green' if val < 0 else 'red' for val in values]
    
    bars = plt.barh(filtered_features, filtered_values, color=colors)
    plt.xlabel("SHAP Value (Impact on Model Output)")
    plt.title("SHAP Impact for Individual Prediction")
    plt.axvline(x=0, color='black', linestyle='--')
    plt.gca().invert_yaxis()  # Highest impact on top

    for bar, val in zip(bars, filtered_values):
        plt.text(val + 0.05 if val >= 0 else val - 0.4, bar.get_y() + bar.get_height() / 2,
                 f"{val:.2f}", va='center', ha='left' if val >= 0 else 'right', color='black')
    # Save to buffer and encode for frontend use
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    shap_plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
    print(f"SHAP plot base64 length: {len(shap_plot_base64)}") 
    return {"feature_impact": feature_impact, "shap_plot": shap_plot_base64,"shap_summary_text": shap_summary_text}

if __name__ == '__main__':
    app.run(debug=True)




