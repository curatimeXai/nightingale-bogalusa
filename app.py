from flask import Flask, request, jsonify, send_from_directory
import os
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
import xgboost as xgb
import tensorflow as tf
from backend.common_preprocess import preprocess_df, FEATURES

app = Flask(__name__, static_folder="static")
CORS(app,
     resources={r"/*": {
         "origins": [
             "https://master.d3oamy7whkzfxr.amplifyapp.com",
             "https://nightingame-2048.com",
             "https://www.nightingame-2048.com",
             "https://bogalusafrontend.nightingaleheart.com"
         ],
         "allow_headers": ["Content-Type"],
         "methods": ["POST", "GET", "OPTIONS"],
         "supports_credentials": False
     }})
# Load trained models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")

svm_model = joblib.load(os.path.join(MODELS_DIR, "svm_model.pkl"))
xgb_model = xgb.XGBClassifier()
xgb_model.load_model(os.path.join(MODELS_DIR, "xgb_model.json"))

keras_model = tf.keras.models.load_model(
    os.path.join(MODELS_DIR, "keras_savedmodel")
)

scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))

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
    return {'message': 'Backend is running successfully!'}


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Use the shared preprocessor for consistency
        df_raw = pd.DataFrame([{
            'Gender': data['Gender'],
            'Age': data['Age'],
            'BMI': data['BMI'],
            'Smoking': data['Smoking'],
            'Alcohol': data['Alcohol'],
            'Sleep': data['Sleep'],
            'Exercise': data['Exercise'],
            'Fruit': data['Fruit'],
            'Diabetes': 'Yes' if data['Diabetes'] else 'No',
            'Kidney': 'Yes' if data['Kidney'] else 'No',
            'Stroke': 'Yes' if data['Stroke'] else 'No',
        }])
        
        # Preprocess using shared function
        X_input = preprocess_df(df_raw)
        
        # Fill NaNs with training medians
        feature_medians = joblib.load('models/feature_medians.pkl')
        X_input = X_input.fillna(feature_medians)
        
        # Scale
        input_scaled = scaler.transform(X_input)

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

        # Get SHAP explanation with all required arguments
        shap_explanation = get_shap_explanation(xgb_model, input_scaled, X_input.columns.tolist())

        predictions_dict = {'svm': svm_pred, 'xgb': xgb_pred, 'keras': keras_pred}
        risk_assessment = calculate_risk_score(predictions_dict)
        lifestyle_analysis = analyze_lifestyle_factors(data)

        return jsonify({
            "shap_impact": shap_explanation["feature_impact_pp"],
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
    plt.close(fig)
    return img_base64


def get_shap_explanation(model, input_scaled, feature_names):
    """
    Generate SHAP explanations for a given model and input sample.
    Returns normalized SHAP values, percentage share, SHAP summary, and plot (base64).
    """
    try:
        # Initialize SHAP explainer for XGBoost
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_scaled)
        
        # Handle different SHAP value formats
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # For binary classification, take positive class
        
        # Convert SHAP output to numeric array (in percentage points)
        individual_prob = shap_values[0] * 100.0

        # --- Raw SHAP contributions (before normalization) ---
        contrib_pp = {feature_names[i]: float(individual_prob[i]) for i in range(len(feature_names))}

        # --- Normalize SHAP values to 0–10 range for better interpretability ---
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
    except Exception as e:
        print(f"SHAP explanation error: {e}")
        import traceback
        traceback.print_exc()
        # Return empty/default values if SHAP fails
        return {
            "feature_impact_pp": {},
            "feature_share_percent": {},
            "shap_plot": "",
            "shap_summary_text": "SHAP explanation unavailable"
        }

@app.after_request
def add_cors_headers(response):
    # IMPORTANT: Replace "*" with your frontend URLs if you want to restrict access
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    return response

# ---- HEALTH CHECK ENDPOINT ----
@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}, 200


# ---- RUN CONFIGURATION ----
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)

# ---- REQUIRED FOR ELASTIC BEANSTALK ----
application = app
