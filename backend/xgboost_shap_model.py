import pandas as pd
import numpy as np
from tabulate import tabulate
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from xgboost import XGBClassifier
import shap


# ============================================================
#                    FEATURE DEFINITIONS
# ============================================================

NUMERIC_FEATURES = [
    "Age of respondent, calculated",
    "Do sports or other physical activity, how many of last 7 days",
    "Height of respondent (cm)",
    "Weight of respondent (kg)",
]

BINARY_FEATURES = [
    "Gender",
    "Health problems, last 12 months: high blood pressure",
    "Health problems, last 12 months: diabetes",
    "Problems with accomodation: noise",
]

ORDINAL_FEATURES = [
    "How often eat fruit, excluding drinking juice",
    "How often eat vegetables or salad, excluding potatoes",
]

SMOKING_FEATURE = ["Cigarette smoking behaviour"]
ALCOHOL_FEATURE = ["How often drink alcohol"]

TARGET = "Health problems, last 12 months: heart or circulation problem"

ALL_FEATURES = (
    NUMERIC_FEATURES +
    BINARY_FEATURES +
    ORDINAL_FEATURES +
    SMOKING_FEATURE +
    ALCOHOL_FEATURE
)


# ============================================================
#                 LOAD & CLEAN DATA
# ============================================================

df = pd.read_csv("dataset.csv")
df = df.dropna(subset=ALL_FEATURES + [TARGET])

binary_map = {
    "Male": 1, "Female": 0,
    "Marked": 1, "Not marked": 0,
}

# Apply binary mapping
for col in BINARY_FEATURES:
    df[col] = df[col].map(binary_map)

df[TARGET] = df[TARGET].map(binary_map)


# Ordinal encoder
ordinal_order = [
    "Never",
    "Less than once a week",
    "Less than 4 times a week but at least once a week",
    "Less than once a day but at least 4 times a week",
    "Once a day",
    "Twice a day",
    "Three times or more a day",
]

ordinal_encoder = OrdinalEncoder(
    categories=[ordinal_order, ordinal_order],
    handle_unknown="use_encoded_value",
    unknown_value=-1
)


# ============================================================
#                 PREPROCESSING PIPELINE
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("bin", "passthrough", BINARY_FEATURES),
        ("ord", ordinal_encoder, ORDINAL_FEATURES),
        ("smoke", OneHotEncoder(handle_unknown="ignore"), SMOKING_FEATURE),
        ("alcohol", OneHotEncoder(handle_unknown="ignore"), ALCOHOL_FEATURE),
    ]
)


# ============================================================
#               XGBOOST MODEL
# ============================================================

xgb = XGBClassifier(
    n_estimators=400,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    scale_pos_weight=7369 / 946,
    use_label_encoder=False,
    enable_categorical=False,
    tree_method="hist"
)

model = Pipeline([
    ("preprocess", preprocessor),
    ("xgb", xgb)
])


# ============================================================
#                    TRAIN MODEL
# ============================================================

X = df[ALL_FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model.fit(X_train, y_train)


# ============================================================
#                    EVALUATION
# ============================================================

from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n=========== MODEL PERFORMANCE ===========")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC:", roc_auc_score(y_test, y_proba))
print(classification_report(y_test, y_pred))


# ============================================================
#             SHAP EXPLAINER (NUMERIC ONLY)
# ============================================================

print("\nInitializing SHAP...")

X_train_num = model.named_steps["preprocess"].transform(X_train)

def model_predict_numeric(X_num):
    return model.named_steps["xgb"].predict_proba(X_num)[:, 1]

explainer = shap.Explainer(
    model_predict_numeric,
    X_train_num,
    algorithm="permutation"
)


# ============================================================
#      BUILD MAPPING: transformed feature → raw feature
# ============================================================

transform_names = preprocessor.get_feature_names_out()

RAW_MAP = {}

for name in transform_names:
    if name.startswith("num__"):
        RAW_MAP[name] = name.replace("num__", "")
    elif name.startswith("bin__"):
        RAW_MAP[name] = name.replace("bin__", "")
    elif name.startswith("ord__"):
        RAW_MAP[name] = name.replace("ord__", "")
    elif name.startswith("smoke__"):
        RAW_MAP[name] = "Cigarette smoking behaviour"
    elif name.startswith("alcohol__"):
        RAW_MAP[name] = "How often drink alcohol"


# ============================================================
#             PREPARE PERSON (binary mapping)
# ============================================================

def prepare_person(person_df):
    p = person_df.copy()
    for col in BINARY_FEATURES:
        p[col] = p[col].map(binary_map)
    return model.named_steps["preprocess"].transform(p)


# ============================================================
#           EXPLAIN PERSON (PER-FEATURE SHAP)
# ============================================================

def explain_person(person_df):
    """Explain prediction with one SHAP value per original human feature."""

    p = person_df.copy()
    for col in BINARY_FEATURES:
        p[col] = p[col].map(binary_map)

    p_num = model.named_steps["preprocess"].transform(p)

    shap_vals = explainer(p_num).values[0]

    # Aggregate SHAP by raw (human) feature name
    grouped = {}
    for tname, sval in zip(transform_names, shap_vals):
        base = RAW_MAP[tname]
        grouped.setdefault(base, 0)
        grouped[base] += abs(sval)

    # Normalize to %
    total = sum(grouped.values())
    result = [(feat, 100 * grouped[feat] / total) for feat in grouped]
    result = sorted(result, key=lambda x: x[1], reverse=True)

    print("\n=========== PER-FEATURE SHAP IMPACT (%) ===========")
    print(tabulate(result, headers=["Feature", "Impact (%)"], tablefmt="grid"))

    return result


# ============================================================
#               EXAMPLE PERSON PREDICTION
# ============================================================
'''
new_person = pd.DataFrame([{
    "Gender": "Male",
    "Age of respondent, calculated": 45,
    "Do sports or other physical activity, how many of last 7 days": 3,
    "How often eat fruit, excluding drinking juice": "Once a day",
    "How often eat vegetables or salad, excluding potatoes": "Once a day",
    "Cigarette smoking behaviour": "I smoke daily, 9 or fewer cigarettes",
    "How often drink alcohol": "2-3 times a month",
    "Height of respondent (cm)": 178,
    "Weight of respondent (kg)": 78,
    "Health problems, last 12 months: high blood pressure": "Not marked",
    "Health problems, last 12 months: diabetes": "Not marked",
    "Problems with accomodation: noise": "Not marked",
}])

processed = prepare_person(new_person)
risk = model.named_steps["xgb"].predict_proba(processed)[0, 1]

print(f"\nPredicted risk for this person: {risk:.2%}")
explain_person(new_person)
'''


# ============================================================
#                          SAVE MODEL
# ============================================================


# Save model pipeline
joblib.dump(model, "heart_model.pkl")

# Save SHAP objects you'll need later
joblib.dump(RAW_MAP, "raw_feature_map.pkl")
joblib.dump(transform_names, "transformed_feature_names.pkl")

# Save a SHAP background dataset (used by the API)
background = X_train.sample(200, random_state=42)
joblib.dump(background, "shap_background.pkl")

print("Model saved as heart_model.pkl")
