# train_model.py (your old file, lightly edited)
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC 
import xgboost as xgb
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys, subprocess
import shap

# NEW: import the shared preprocessor and schema
from common_preprocess import preprocess_df, FEATURES

os.makedirs("models", exist_ok=True)

# --- Load
df = pd.read_csv("brfss13.csv")
print(f"Original dataset size: {df.shape}")

# Target mapping
df["Heartdis"] = df["Heartdis"].map({"Yes": 1, "No": 0})
df.dropna(subset=["Heartdis"], inplace=True)

# --- Features via shared preprocessor
X = preprocess_df(df)                 # <— unified mapping here
y = df["Heartdis"].astype(int)

# Fill NaNs consistently & persist medians for API parity
feature_medians = X.median(numeric_only=True).to_dict()
X = X.fillna(feature_medians)
joblib.dump(FEATURES, "models/features.pkl")
joblib.dump(feature_medians, "models/feature_medians.pkl")

# --- Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Scale (kept as in your old script for all models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)
joblib.dump(scaler, "models/scaler.pkl")

# --- SVM
svm_model = SVC(kernel="rbf", C=1.0, gamma="scale", probability=True,
                random_state=42, class_weight='balanced')
svm_model.fit(X_train_scaled, y_train)
joblib.dump(svm_model, "models/svm_model.pkl")

# --- XGBoost (still on scaled features, same as your old code)
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.8,
    eval_metric="logloss",
    random_state=42,
)
xgb_model.fit(X_train_scaled, y_train)
xgb_model.save_model("models/xgb_model.json")


# --- Keras
keras_model = Sequential([
    Dense(64, input_dim=X_train_scaled.shape[1], activation="relu"),
    Dense(32, activation="relu"),
    Dense(1, activation="sigmoid"),
])
keras_model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])
keras_model.fit(X_train_scaled, y_train, epochs=10, batch_size=32, verbose=1)
keras_model.save("models/keras_model.h5")

# --- XGB Feature Importance (same as before)
feature_importance = xgb_model.feature_importances_
plt.figure(figsize=(10, 6))
order = np.argsort(feature_importance)
plt.barh(np.array(FEATURES)[order], feature_importance[order])
plt.title("Feature Importance (XGBoost)")
plt.tight_layout()
plt.savefig("models/feature_importance.png")
plt.close()

# ---- SHAP (interventional + raw output) ----
# 1) Background sample for interventional explainer
rng = np.random.RandomState(42)
bg_idx = rng.choice(len(X_train_scaled), size=min(2000, len(X_train_scaled)), replace=False)
background = X_train_scaled[bg_idx]

# 2) Use a sample for speed and wrap as DataFrame so SHAP knows column names
sample_idx = rng.choice(len(X_train_scaled), size=min(5000, len(X_train_scaled)), replace=False)
X_shap = X_train_scaled[sample_idx]
X_shap_df = pd.DataFrame(X_shap, columns=FEATURES)   # <-- real feature names

# Create explainer - use 'raw' output with interventional
explainer = shap.TreeExplainer(
    xgb_model,
    data=background,
    feature_perturbation="interventional",
    model_output="raw",  # Changed from "probability" to "raw"
)

plot_path = os.path.abspath("models/shap_summary.png")  # absolute path

# 3) Try modern API first; fall back to summary_plot
try:
    explanation = explainer(X_shap_df)               # <-- pass DataFrame, not ndarray
    shap.plots.beeswarm(explanation, show=False, max_display=min(20, len(FEATURES)))
    fig = plt.gcf()
    fig.savefig(plot_path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Saved SHAP summary (beeswarm) to {plot_path}")
except Exception as e:
    print(f"Beeswarm failed ({e}), falling back to summary_plot()")
    shap_values = explainer.shap_values(X_shap_df)   # ndarray in raw units
    shap.summary_plot(shap_values, X_shap_df, feature_names=FEATURES, show=False, max_display=min(20, len(FEATURES)))
    fig = plt.gcf()
    fig.savefig(plot_path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Saved SHAP summary (summary_plot) to {plot_path}")

# 4) Save single-row impact (raw units converted to percentage points for display)
#    (If modern API worked, reuse 'explanation'; else recompute shap_values)
try:
    # modern API path
    one_pp = explanation.values[0] * 100.0
except NameError:
    # fallback path
    one_pp = shap_values[0] * 100.0

feature_impact = {FEATURES[i]: float(one_pp[i]) for i in range(len(FEATURES))}
with open("models/shap_results.json", "w") as f:
    json.dump(feature_impact, f, indent=2)

joblib.dump(feature_impact, "models/feature_impact.pkl")
# Persist a small sample of SHAP values for later (don't dump the whole training if large)
try:
    joblib.dump(explanation.values, "models/shap_values_sample.pkl")
except NameError:
    joblib.dump(shap_values, "models/shap_values_sample.pkl")

# 5) Auto-open the PNG with the system viewer (only if NOT in Docker/headless environment)
try:
    if sys.platform.startswith("win"):
        os.startfile(plot_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", plot_path], check=False)
    else:
        subprocess.run(["xdg-open", plot_path], check=False)
except Exception as e:
    print(f"Could not auto-open plot (likely running in Docker): {e}")

print("✅ Training completed. Models and SHAP plot saved.")