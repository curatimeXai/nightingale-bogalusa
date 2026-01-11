import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
import shap
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
#         LOAD MODEL + METADATA REQUIRED FOR THE API
# ============================================================

model = joblib.load("heart_model.pkl")
RAW_MAP = joblib.load("raw_feature_map.pkl")
transform_names = joblib.load("transformed_feature_names.pkl")
background_raw = joblib.load("shap_background.pkl")

# XGBoost model reference
xgb_clf = model.named_steps["xgb"]

binary_map = {
    "Male": 1, "Female": 0,
    "Marked": 1, "Not marked": 0,
}

# Mapping for ordinal features (string -> numeric)
# Fruit and Vegetable consumption (1-7 scale)
fruit_veg_map = {
    "Never": 1,
    "Less than once a week": 2,
    "Less than 4 times a week but at least once a week": 3,
    "Less than once a day but at least 4 times a week": 4,
    "Once a day": 5,
    "Twice a day": 6,
    "Three times or more a day": 7,
}

# Smoking behavior (1-6 scale)
smoking_map = {
    "I have never smoked": 1,
    "I used to smoke daily, but now I never smoke": 2,
    "I used to smoke daily, but now smoke not daily": 3,
    "I smoke, but not daily": 4,
    "I smoke daily, 9 or fewer cigarettes": 5,
    "I smoke daily, 10 or more cigarettes": 6,
}

# Alcohol frequency (1-7 scale)
alcohol_map = {
    "Never": 1,
    "Not in the last 12 months": 2,
    "Once a month or less": 3,
    "2-4 days a month": 4,
    "2-3 days a week": 5,
    "5-6 days a week": 6,
    "Every day": 7,
}

BINARY_FEATURES = [
    "Gender",
    "Health problems, last 12 months: high blood pressure",
    "Health problems, last 12 months: diabetes",
    "Problems with accomodation: noise",
]

# NEW : include BMI in the API feature list
ALL_FEATURES = [
    "Gender",
    "Age of respondent, calculated",
    "Do sports or other physical activity, how many of last 7 days",
    "How often eat fruit, excluding drinking juice",
    "How often eat vegetables or salad, excluding potatoes",
    "Cigarette smoking behaviour",
    "How often drink alcohol",
    "Height of respondent (cm)",
    "Weight of respondent (kg)",
    "BMI",   # 🔥 NEW
    "Health problems, last 12 months: high blood pressure",
    "Health problems, last 12 months: diabetes",
    "Problems with accomodation: noise",
]

# ============================================================
#  PREPROCESS BACKGROUND → NUMERIC (SHAP masker requires BMI)
# ============================================================

background_fixed = background_raw.copy()
background_fixed["BMI"] = background_fixed["Weight of respondent (kg)"] / (background_fixed["Height of respondent (cm)"] / 100)**2

# Background data from training is already numeric, no mapping needed
background_numeric = model.named_steps["preprocess"].transform(background_fixed)

# ============================================================
#         SHAP EXPLAINER
# ============================================================

print("Loading SHAP PermutationExplainer...")

masker = shap.maskers.Independent(background_numeric)
xgb_model = model.named_steps["xgb"]

explainer = shap.Explainer(
    lambda X: xgb_model.predict_proba(X)[:, 1],
    masker,
    algorithm="permutation"
)

# ============================================================
#     GROUP SHAP BACK TO ORIGINAL FEATURES
# ============================================================

def group_shap_values(shap_row):
    grouped = {feat: 0.0 for feat in ALL_FEATURES}

    for tname, shap_value in zip(transform_names, shap_row):
        raw = RAW_MAP[tname]
        grouped[raw] += shap_value  # keep sign

    total = sum(abs(v) for v in grouped.values())

    if total > 0:
        return {k: float(v * 100 / total) for k, v in grouped.items()}
    return {k: 0.0 for k in grouped}


# ============================================================
#                  START FASTAPI APP
# ============================================================

app = FastAPI(title="Heart Disease Risk API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://bogalusa.nightingaleheart.com",
        "https://master.d3oamy7whkzfxr.amplifyapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
#                     HEALTH CHECK ENDPOINTS
# ============================================================

@app.get("/")
def root():
    """Root endpoint - API info"""
    return {
        "service": "Heart Disease Risk API",
        "version": "1.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for load balancers"""
    return {"status": "healthy"}

# ============================================================
#                     /predict ENDPOINT
# ============================================================

@app.post("/predict")
def predict(payload: dict):
    try:
        logger.info(f"Received prediction request")

        df = pd.DataFrame([payload])

        # Validate height is not zero
        height = df["Height of respondent (cm)"].iloc[0]
        if height <= 0:
            raise HTTPException(status_code=400, detail="Height must be greater than 0")

        # Compute BMI (API MUST do this)
        df["BMI"] = df["Weight of respondent (kg)"] / (df["Height of respondent (cm)"] / 100)**2

        # Map binary values
        for col in BINARY_FEATURES:
            df[col] = df[col].map(binary_map)

        # Map ordinal string values to numeric (if they are strings)
        fruit_col = "How often eat fruit, excluding drinking juice"
        veg_col = "How often eat vegetables or salad, excluding potatoes"
        smoke_col = "Cigarette smoking behaviour"
        alcohol_col = "How often drink alcohol"

        # Convert strings to numeric if needed
        if df[fruit_col].dtype == object:
            df[fruit_col] = df[fruit_col].map(fruit_veg_map)
        if df[veg_col].dtype == object:
            df[veg_col] = df[veg_col].map(fruit_veg_map)
        if df[smoke_col].dtype == object:
            df[smoke_col] = df[smoke_col].map(smoking_map)
        if df[alcohol_col].dtype == object:
            df[alcohol_col] = df[alcohol_col].map(alcohol_map)

        # Preprocess inputs
        df_num = model.named_steps["preprocess"].transform(df)

        # Predict risk
        risk = xgb_model.predict_proba(df_num)[0, 1]

        # SHAP explanation
        shap_row = explainer(df_num).values[0]
        grouped = group_shap_values(shap_row)

        logger.info(f"Prediction successful: risk={risk:.4f}")

        return {
            "risk": float(risk),
            "risk_percent": f"{risk*100:.2f}%",
            "feature_impacts_percent": grouped
        }

    except HTTPException:
        raise
    except KeyError as e:
        logger.error(f"Missing field: {e}")
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
