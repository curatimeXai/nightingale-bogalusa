import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
import xgboost as xgb
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Load the dataset
df = pd.read_csv("brfss13.csv")

# Display initial dataset size
print(f"Original dataset size: {df.shape}")

# Convert 'Heartdis' to binary (1 = Yes, 0 = No)
df["Heartdis"] = df["Heartdis"].map({"Yes": 1, "No": 0})
df.dropna(subset=["Heartdis"], inplace=True)

# Convert Age to numeric and handle missing values
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Age"].fillna(df["Age"].median(), inplace=True)

# Define relevant features
features = ["Gender", "BMI", "Smoking", "Alcohol", "Sleep", "Exercise", "Fruit", "Diabetes", "Kidney", "Stroke"]
X = df[features]
y = df["Heartdis"]

# Encode categorical variables properly
for col in ["Gender", "Smoking", "Alcohol", "Diabetes", "Kidney", "Stroke"]:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))  # Ensures categorical values are numeric

# Fill any remaining NaN values
X.fillna(0, inplace=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the scaler
joblib.dump(scaler, "models/scaler.pkl")

# Train SVM Model
svm_model = SVC(probability=True, random_state=42)
svm_model.fit(X_train_scaled, y_train)
joblib.dump(svm_model, "models/svm_model.pkl")

# Train XGBoost Model
xgb_model = xgb.XGBClassifier(eval_metric="logloss", random_state=42)
xgb_model.fit(X_train_scaled, y_train)
joblib.dump(xgb_model, "models/xgb_model.pkl")

# Train Keras Model
keras_model = Sequential([
    Dense(64, input_dim=X_train_scaled.shape[1], activation="relu"),
    Dense(32, activation="relu"),
    Dense(1, activation="sigmoid"),
])

keras_model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])
keras_model.fit(X_train_scaled, y_train, epochs=10, batch_size=32, verbose=1)

# Save Keras Model
keras_model.save("models/keras_model.h5")

# Feature Importance Plot (for XGBoost)
feature_importance = xgb_model.feature_importances_
feature_names = X.columns

plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance, y=feature_names)
plt.title("Feature Importance (XGBoost)")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.tight_layout()
plt.savefig("models/feature_importance.png")

print("✅ Training completed. Models saved successfully!")



