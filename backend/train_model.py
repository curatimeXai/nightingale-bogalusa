import json
from typing import Counter
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
import shap
import re

# Ensure models directory exists for saving trained models and results
os.makedirs("models", exist_ok=True)

# Load the dataset from CSV file. But this 
df = pd.read_csv("brfss13.csv")

# Display initial dataset size for reference
print(f"Original dataset size: {df.shape}")

# Convert 'Heartdis' to binary (1 = Yes, 0 = No)
df["Heartdis"] = df["Heartdis"].map({"Yes": 1, "No": 0})
# Remove any rows where 'Heartdis' is still missing after mapping
df.dropna(subset=["Heartdis"], inplace=True)

# Convert Age to numeric and handle missing values
# Parse age from CSV (Age 50 to 54 => 52)
def parse_age_range(value):
    if isinstance(value, str):
        # Look for two numbers in the string
        numbers = re.findall(r'\d+', value)
        print(numbers)
        if len(numbers) == 2:
            # Get the average of those 2
            low, high = map(int, numbers)
            return (low + high) / 2
    return np.nan  # Return NaN else

# Convert Age ranges to numeric midpoints
df["Age"] = df["Age"].apply(parse_age_range)

# Fill out NaN with median
df["Age"].fillna(df["Age"].median(), inplace=True)

# Define relevant features to be used for prediction
features = ["Gender","Age", "BMI", "Smoking", "Alcohol", "Sleep", "Exercise", "Fruit", "Diabetes", "Kidney", "Stroke"]

# Extract feature variables (x) and target variable (y)
X = df[features]
y = df["Heartdis"]

# I choose to manually set instead of using LabelEncoder to be certain of consistency through the app
gender_map = {'Male': 1, 'Female': 0}
smoking_map = {'Not at all': 0, 'Sometimes': 1, 'Every day': 2}
bool_map = {'No': 0, 'Yes': 1}

X['Gender'] = X['Gender'].map(gender_map)
X['Smoking'] = X['Smoking'].map(smoking_map)
X['Alcohol'] = pd.to_numeric(X['Alcohol'], errors='coerce')  # if already numeric
X['Diabetes'] = X['Diabetes'].map(bool_map)
X['Kidney'] = X['Kidney'].map(bool_map)
X['Stroke'] = X['Stroke'].map(bool_map)


# Fill any remaining missing values in the dataset with median
X = X.fillna(X.median(numeric_only=True))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize feature values using StandardScaler features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) # fit and transform training data
X_test_scaled = scaler.transform(X_test) # Transform test data using same scaler

# Save the scaler for later use 
joblib.dump(scaler, "models/scaler.pkl")

# Train Support Vector Machine SVM Model
svm_model = SVC(kernel="rbf",C=1.0,gamma="scale",probability=True, random_state=42,class_weight='balanced') # Initialize SVM with probability estimation
svm_model.fit(X_train_scaled, y_train) # Train the model on the training set
joblib.dump(svm_model, "models/svm_model.pkl")  # Save the trained SVM model

# Train XGBoost Model
xgb_model = xgb.XGBClassifier(n_estimators=100,
                              max_depth=4,
                              learning_rate=0.1,
                              subsample=0.8,
                              eval_metric="logloss",
                                random_state=42,
                               )
xgb_model.fit(X_train_scaled, y_train)
joblib.dump(xgb_model, "models/xgb_model.pkl")

# Train Keras Model
keras_model = Sequential([
    # First hidden layer with 64 neurons
    Dense(64, input_dim=X_train_scaled.shape[1], activation="relu"),
    Dense(32, activation="relu"),# Second hidden layer with 32 neurons
    Dense(1, activation="sigmoid"),# Output layer with sigmoid activation for binary classification
])
# Compile the model using Adam optimizer and binary cross-entropy loss
keras_model.compile(optimizer=Adam(), loss="binary_crossentropy", metrics=["accuracy"])
# Train the neural network model for 10 epochs with batch size of 32
keras_model.fit(X_train_scaled, y_train, epochs=10, batch_size=32, verbose=1)

# Save the trained Keras model
keras_model.save("models/keras_model.h5")

# Feature Importance Plot (for XGBoost)
# Extract feature importance scores from XGBoost
feature_importance = xgb_model.feature_importances_
# Store feature names for labeling
feature_names = X.columns

# Plot the feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance, y=feature_names) # Create a bar plot of feature importance
plt.title("Feature Importance (XGBoost)")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.tight_layout()
plt.savefig("models/feature_importance.png") # Save the plot

# SHAP (SHapley Additive exPlanations) for Model Interpretability
# SHAP Values Calculation (Using XGBoost model)
explainer = shap.TreeExplainer(xgb_model)
# Compute SHAP values for training data
shap_values = explainer.shap_values(X_train_scaled)
# # Generate a SHAP summary plot to visualize feature contributions
shap.summary_plot(shap_values, X_train_scaled, feature_names=X.columns)
plt.savefig("models/shap_summary.png") # Save the SHAP summary plot

# Calculating the impact of each feature for the first instance in the training data
individual_shap_values = shap_values[0]  # Getting SHAP values for the first data point
feature_impact = {X.columns[i]: individual_shap_values[i] for i in range(len(X.columns))}
# Save SHAP values for frontend use
with open("models/shap_results.json", "w") as json_file:
    json.dump({k: float(v) for k, v in feature_impact.items()}, json_file)
# Print out the calculated feature impact for the first instance
print("Feature Impact for the first instance:", feature_impact)

# Save SHAP values and feature impact for future use
joblib.dump(feature_impact, "models/feature_impact.pkl")
joblib.dump(shap_values, "models/shap_values.pkl")

print("✅ Training completed. Models saved successfully!")



