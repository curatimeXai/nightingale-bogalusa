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
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('brfss13.csv')

# Check the initial size of the dataset
print(f"Original dataset size: {df.shape}")

# Check the unique values in 'Heartdis' before cleaning
print(f"Unique values in 'Heartdis' before cleaning: {df['Heartdis'].unique()}")

# Ensure Age is numeric and handle errors (invalid data converted to NaN)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

# Handle missing Age values - we can fill with the median (or another strategy)
if df['Age'].isnull().any():
    print(f"Filling {df['Age'].isnull().sum()} missing Age values with the median.")
    df['Age'].fillna(df['Age'].median(), inplace=True)

# Check the unique values in 'Heartdis' column and handle missing values
if df['Heartdis'].isnull().any():
    print("Warning: There are missing values in 'Heartdis'. These will be dropped.")
    df = df.dropna(subset=['Heartdis'])

# Ensure 'Heartdis' has valid binary values
df['Heartdis'] = df['Heartdis'].apply(lambda x: 1 if x.lower() == 'yes' else 0)

# Create AgeCategory based on Age
def categorize_age(age):
    if 18 <= age <= 24:
        return '18-24'
    elif 25 <= age <= 29:
        return '25-29'
    elif 30 <= age <= 34:
        return '30-34'
    elif 35 <= age <= 39:
        return '35-39'
    elif 40 <= age <= 44:
        return '40-44'
    elif 45 <= age <= 49:
        return '45-49'
    elif 50 <= age <= 54:
        return '50-54'
    elif 55 <= age <= 59:
        return '55-59'
    elif 60 <= age <= 64:
        return '60-64'
    elif 65 <= age <= 69:
        return '65-69'
    elif 70 <= age <= 74:
        return '70-74'
    elif 75 <= age <= 79:
        return '75-79'
    else:
        return '80+'

# Apply age categorization
df['AgeCategory'] = df['Age'].apply(categorize_age)

# Check if there is enough data after cleaning
print(f"After cleaning, dataset size: {df.shape}")

# Verify unique values in target column (Heartdis)
print(f"Unique values in 'Heartdis': {df['Heartdis'].unique()}")

# Select relevant features and target
features = ['Gender', 'AgeCategory', 'BMI', 'Smoking', 'Alcohol', 'Sleep', 'Exercise', 'Fruit', 
            'Diabetes', 'Kidney', 'Stroke']

X = df[features]
y = df['Heartdis']  # Binary target (1 or 0)

# Check for NaN values in the features
print(f"NaN values in features: {X.isnull().sum()}")

# One-hot encoding for categorical features
X = pd.get_dummies(X, drop_first=True)

# Check for NaN values after encoding
print(f"NaN values in features after encoding: {X.isnull().sum()}")

# If there's not enough data after processing, raise an error
if X.shape[0] < 10:
    raise ValueError("Dataset is too small to perform train-test split.")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train and save the SVM model
svm_model = SVC(probability=True)
svm_model.fit(X_train_scaled, y_train)
joblib.dump(svm_model, 'models/svm_model.pkl')

# Train and save the XGBoost model
xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb_model.fit(X_train_scaled, y_train)
joblib.dump(xgb_model, 'models/xgb_model.pkl')

# Train and save the Keras model
keras_model = Sequential()
keras_model.add(Dense(64, input_dim=X_train_scaled.shape[1], activation='relu'))
keras_model.add(Dense(32, activation='relu'))
keras_model.add(Dense(1, activation='sigmoid'))

# Compile the Keras model
keras_model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
keras_model.fit(X_train_scaled, y_train, epochs=10, batch_size=32)

# Save the Keras model
keras_model.save('models/keras_model.h5')

# Save the scaler for future use
joblib.dump(scaler, 'models/scaler.pkl')

# OPTIONAL: Feature importance plot for XGBoost
feature_importance = xgb_model.feature_importances_
features = X.columns

plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance, y=features)
plt.title('Feature Importance (XGBoost)')
plt.xlabel('Importance')
plt.ylabel('Features')
plt.tight_layout()
plt.savefig('models/feature_importance.png')
