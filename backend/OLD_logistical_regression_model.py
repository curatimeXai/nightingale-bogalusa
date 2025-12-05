import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# ============================
#     FEATURE DEFINITIONS
# ============================

NUMERIC_FEATURES = [
    "Age of respondent, calculated",
    "Do sports or other physical activity, how many of last 7 days",
    "Height of respondent (cm)",
    "Weight of respondent (kg)",
]

BINARY_FEATURES = [
    "Gender",  # Male/Female
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

# ============================
#     LOAD DATA
# ============================

df = pd.read_csv("dataset.csv")

# Keep only needed columns
ALL_FEATURES = (
    NUMERIC_FEATURES
    + BINARY_FEATURES
    + ORDINAL_FEATURES
    + SMOKING_FEATURE
    + ALCOHOL_FEATURE
)

df = df.dropna(subset=ALL_FEATURES + [TARGET])

# ============================
#   PREPROCESSING MAPPINGS
# ============================

# Binary mapping
binary_map = {
    "Male": 1, "Female": 0,
    "Marked": 1, "Not marked": 0,
}

for col in BINARY_FEATURES:
    df[col] = df[col].map(binary_map)

# Target mapping
df[TARGET] = df[TARGET].map(binary_map)

# Ordinal order (same for fruit & vegetables)
ordinal_order = [
    "Never",
    "Less than once a week",
    "Less than 4 times a week but at least once a week",
    "Less than once a day but at least 4 times a week",
    "Once a day",
    "Twice a day",
    "Three times or more a day",
]

ordinal_encoder = OrdinalEncoder(categories=[ordinal_order, ordinal_order], handle_unknown="use_encoded_value", unknown_value=-1)

# ============================
#    COLUMN TRANSFORMER
# ============================

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("bin", "passthrough", BINARY_FEATURES),
        ("ord", ordinal_encoder, ORDINAL_FEATURES),
        ("smoke", OneHotEncoder(handle_unknown="ignore"), SMOKING_FEATURE),
        ("alcohol", OneHotEncoder(handle_unknown="ignore"), ALCOHOL_FEATURE),
    ]
)

# ============================
#       MODEL PIPELINE
# ============================

model = Pipeline([
    ("preprocess", preprocessor),
    ("logreg", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

# ============================
#    TRAIN / TEST SPLIT
# ============================

X = df[ALL_FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================
#        TRAIN MODEL
# ============================

model.fit(X_train, y_train)

# ============================
#        EVALUATION
# ============================

from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC:", roc_auc_score(y_test, y_proba))
print(classification_report(y_test, y_pred))

# ============================
#      NEW PERSON PREDICTION
# ============================

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

# Apply binary mapping
for col in BINARY_FEATURES:
    new_person[col] = new_person[col].map(binary_map)

# Predict risk
risk = model.predict_proba(new_person)[0, 1]
print(f"\nPredicted heart/circulation risk: {risk:.2%}")
