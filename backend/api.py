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

binary_map = {
    "Male": 1, "Female": 0,
    "Marked": 1, "Not marked": 0,
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

for col in BINARY_FEATURES:
    background_fixed[col] = background_fixed[col].map(binary_map)

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
