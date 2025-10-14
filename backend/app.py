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
import re

app = Flask(__name__, static_folder="static")
CORS(app, origins=["http://localhost:8080"])

# Load trained models
svm_model = joblib.load('models/svm_model.pkl')
xgb_model = joblib.load('models/xgb_model.pkl')
keras_model = load_model('models/keras_model.h5')
scaler = joblib.load('models/scaler.pkl')


def calculate_risk_score(predictions):
    """Calculate weighted risk score from multiple models"""
    weights = {'svm': 0.3, 'xgb': 0.4, 'keras': 0.3}
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
        return "High cardiovascular risk - Recommended medical consultation"
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
            'recommendation': 'Balanced diet and more exercise'
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
            'recommendation': 'Too much sleep can indicate other health problems'
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
    return send_from_directory('static', 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)

        gender_map = {'Male': 1, 'Female': 0}
        smoking_map = {'Not at all': 0, 'Sometimes': 1, 'Every day': 2}

        # Convert user input into DataFrame
        input_data = {
            'Gender': gender_map.get(data['Gender'], 0),
            'BMI': float(data['BMI']),
            'Smoking': smoking_map.get(data['Smoking'], 0),
            'Alcohol': float(data['Alcohol']),
            'Sleep': float(data['Sleep']),
            'Exercise': float(data['Exercise']),
            'Fruit': float(data['Fruit']),
            'Diabetes': int(data['Diabetes']),
            'Kidney': int(data['Kidney']),
            'Stroke': int(data['Stroke']),
            'Age': int(data['Age'])
        }

        df_input = pd.DataFrame([input_data])
        df_input = pd.get_dummies(df_input)

        # Ensure all features present
        for col in scaler.feature_names_in_:
            if col not in df_input.columns:
                df_input[col] = 0
        df_input = df_input[scaler.feature_names_in_]

        input_scaled = scaler.transform(df_input)

        # Predictions
        svm_pred = float(svm_model.predict_proba(input_scaled)[0][1])
        xgb_pred = float(xgb_model.predict_proba(input_scaled)[0][1])
        keras_pred = float(keras_model.predict(input_scaled)[0][0])

        svm_label = get_thumb_value(svm_pred)
        xgb_label = get_thumb_value(xgb_pred)
        keras_label = get_thumb_value(keras_pred)

        svm_pie_chart = create_pie_chart(svm_pred, "SVM Prediction")
        xgb_pie_chart = create_pie_chart(xgb_pred, "XGBoost Prediction")
        keras_pie_chart = create_pie_chart(keras_pred, "Keras Prediction")

        shap_explanation = get_shap_explanation(input_scaled)

        predictions_dict = {'svm': svm_pred, 'xgb': xgb_pred, 'keras': keras_pred}
        risk_assessment = calculate_risk_score(predictions_dict)
        lifestyle_analysis = analyze_lifestyle_factors(data)

        return jsonify({
            "shap_impact": shap_explanation["feature_impact_pp"],  # frontend expects this
            "shap_contrib_pp": shap_explanation["feature_impact_pp"],
            "shap_share_percent": shap_explanation["feature_share_percent"],
            "shap_plot": shap_explanation["shap_plot"],
            "shap_summary_text": shap_explanation["shap_summary_text"],

            "svm_prediction": svm_pred,
            "xgb_prediction": xgb_pred,
            "keras_prediction": keras_pred,
            "svm_label": svm_label,
            "xgb_label": xgb_label,
            "keras_label": keras_label,

            "svm_pie_chart": svm_pie_chart,
            "xgb_pie_chart": xgb_pie_chart,
            "keras_pie_chart": keras_pie_chart,

            "risk_assessment": risk_assessment,
            "lifestyle_analysis": lifestyle_analysis,
            "model_predictions": {
                "svm": {"probability": svm_pred, "label": svm_label},
                "xgb": {"probability": xgb_pred, "label": xgb_label},
                "keras": {"probability": keras_pred, "label": keras_label}
            },
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


def get_thumb_value(probability):
    return "Up" if probability >= 0.5 else "Down"


def create_pie_chart(probability, title):
    labels = ["No Risk", "High Risk"]
    sizes = [1 - probability, probability]
    colors = ["green", "red"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax.set_title(title)

    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64


def get_shap_explanation(model, input_scaled, scaler):
    """
    Generate SHAP explanations for a given model and input sample.
    Returns normalized SHAP values, percentage share, SHAP summary, and plot (base64).
    """

    # Initialize SHAP explainer
    explainer = shap.Explainer(model, feature_names=scaler.feature_names_in_)
    shap_values_prob = explainer(input_scaled)

    # Convert SHAP output to numeric array
    individual_prob = shap_values_prob.values[0] * 100.0
    feature_names = scaler.feature_names_in_

    # --- Raw SHAP contributions (before normalization) ---
    contrib_pp = {feature_names[i]: float(individual_prob[i]) for i in range(len(feature_names))}

    # --- ✅ Option 1: Normalize SHAP values to 0–10 range for better interpretability ---
    max_abs = max(abs(v) for v in contrib_pp.values()) or 1.0
    contrib_pp_scaled = {k: (v / max_abs) * 10.0 for k, v in contrib_pp.items()}

    # --- Calculate proportional contribution (share %) for visual bar widths ---
    abs_sum = sum(abs(v) for v in contrib_pp_scaled.values()) or 1.0
    share_percent = {k: abs(v) * 100.0 / abs_sum for k, v in contrib_pp_scaled.items()}

    # --- Generate SHAP summary plot as base64 image ---
    filtered_features = [f for f in contrib_pp_scaled if f not in ['Age', 'Gender']]
    filtered_values = [contrib_pp_scaled[f] for f in filtered_features]

    plt.figure(figsize=(8, 4))
    colors = ['#28a745' if val < 0 else '#dc3545' for val in filtered_values]
    plt.barh(filtered_features, filtered_values, color=colors)
    plt.xlabel("Impact on Risk (Normalized Scale)")
    plt.title("Feature Impact on Heart Disease Risk")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    shap_plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # --- SHAP summary text generation ---
    top_features = sorted(contrib_pp_scaled.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
    summary = ", ".join([
        f"{feat} {'increases' if val > 0 else 'reduces'} risk" for feat, val in top_features
    ])

    # --- Return structured data for frontend consumption ---
    return {
        "feature_impact_pp": contrib_pp_scaled,
        "feature_share_percent": share_percent,
        "shap_plot": shap_plot_base64,
        "shap_summary_text": summary
    }



if __name__ == '__main__':
    app.run(debug=True)
