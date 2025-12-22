# **Nightingale Bogalusa — Heart Disease Prediction App**

A web application powered by machine learning that predicts a user's **risk of heart disease** and provides interactive explanations using **SHAP interpretability**.

This project combines:

-   a **Vue.js frontend** for data collection and results visualization,
    
-   a **FastAPI backend** hosting a trained XGBoost model,
    
-   a **complete ML training pipeline** using the European Social Survey dataset.
    

The application gives both a **numerical risk score** and a **breakdown of contributing factors**, allowing users to understand *why* the model made its prediction.

---

# 📚 **Table of Contents**

-   [Tech Stack](#tech-stack)
    
-   Project Overview
    
-   [Getting Started](#getting-started)
    
    -   Frontend Setup
        
    -   Backend Setup
        
    -   Training the Model
        
-   Design System
    
-   Machine Learning Overview
    
    -   Features Used
        
    -   Modeling Pipeline
        
    -   SHAP Explainability
        
-   Best Practices
    
-   [Do’s and Don’ts](#dos-and-donts)
    

---

# 🧠 **Project Overview**

### 🎯 **What the app does**

The *Nightingale Bogalusa Heart Disease Prediction App*:

1.  Collects health and lifestyle information from the user.
    
2.  Sends the data to a backend API built with FastAPI.
    
3.  Predicts the probability of heart disease using an XGBoost classifier.
    
4.  Computes SHAP values to explain which factors influence the prediction.
    
5.  Displays both the **risk score** and the **positive/negative contributing factors**.
    

### 🧩 **Architecture Summary**

#### **Frontend (Vue.js)**

-   Collects user input through an interactive form
    
-   Sends data via Axios to FastAPI
    
-   Displays:
    
    -   Global risk score
        
    -   SHAP-based factor contributions
        
    -   Informative charts and explanations
        

#### **Backend (FastAPI + Python)**

Divided into two parts:

1.  **Training Pipeline**
    
    -   Loads ESS dataset
        
    -   Preprocesses data
        
    -   Computes BMI
        
    -   Encodes categorical features
        
    -   Trains XGBoost model
        
    -   Generates SHAP explainability metadata
        
    -   Saves everything as `.pkl` files
        
2.  **Prediction API**
    
    -   Receives user data
        
    -   Computes BMI
        
    -   Preprocesses input
        
    -   Runs prediction
        
    -   Computes SHAP values
        
    -   Returns risk score + per-feature contributions
        

#### **Dataset**

-   **European Social Survey (ESS)**
    
-   ~40,000 respondents
    
-   Dataset NOT included in repository due to file size limitations
    

---

# ⚙️ **Tech Stack**

### **Frontend**

-   Vue.js 3
    
-   Axios
    
-   SCSS / CSS
    
-   (WIP) Component design system
    

### **Backend**

-   Python 3
    
-   FastAPI
    
-   Uvicorn
    
-   XGBoost
    
-   Scikit-learn
    
-   SHAP
    
-   Pandas / NumPy
    
-   Joblib
    

### **Deployment**

-   **WIP — not deployed yet**
    

---

# 🚀 **Getting Started**

## 🔵 **Frontend Setup**

```bash
npm install
npm run serve
```

Frontend runs at:

```arduino
http://localhost:8080
```

---

## 🟢 **Backend Setup**

### 1\. Create and activate virtual environment

**Windows**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 2\. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3\. (Optional) Retrain the ML model

⚠️ Requires the ESS dataset — **not included in the repo**.

```bash
python xgboost_shap_model.py
```

This script:

-   preprocesses data
    
-   computes BMI
    
-   trains XGBoost
    
-   generates SHAP background data
    
-   saves model and metadata (`heart_model.pkl`, `raw_feature_map.pkl`, etc.)
    

---

### 4\. Start the API

```bash
python api.py
```

API runs at:

```arduino
http://localhost:8000
```

---

# 🎨 **Design System**

### Color Palette

WIP — colors not finalized yet.

### Typography

WIP — dependent on frontend design decisions.

---

# 🧬 **Machine Learning Overview**

## 💡 Purpose of the Model

Predict whether an individual is at risk of developing **heart or circulation disease** based on:

-   Biometric data
    
-   Lifestyle habits
    
-   Addictions (smoking, alcohol)
    
-   Medical conditions
    
-   Environmental exposures
    

---

# 🔧 **Features Used**

### **Numeric**

-   Age
    
-   Days of physical activity
    
-   Height (cm)
    
-   Weight (kg)
    
-   **BMI (computed automatically)**
    

### **Binary**

-   Gender
    
-   High blood pressure
    
-   Diabetes
    
-   Noise exposure
    

### **Ordinal Features**

-   Frequency of fruit consumption
    
-   Frequency of vegetable consumption
    

### **Categorical (One-Hot Encoded)**

-   Smoking behavior
    
-   Alcohol consumption frequency
    

---

# 🏗️ **Modeling Pipeline**

1.  Data cleaning
    
2.  BMI computation
    
3.  `ColumnTransformer` preprocessing
    
    -   StandardScaler
        
    -   OrdinalEncoder
        
    -   OneHotEncoder
        
    -   passthrough for binary features
        
4.  XGBoost model training
    
5.  SHAP permutation explainer
    
6.  Export of model and metadata
    

---

# 🔍 **SHAP Explainability**

The API returns, for each prediction:

-   **positive SHAP values** → factors increasing the risk
    
-   **negative SHAP values** → factors decreasing the risk
    
-   percentages normalized across all features
    

Example:

```json
{
  "risk": 0.12,
  "risk_percent": "12.00%",
  "feature_impacts_percent": {
    "Age": 42.1,
    "BMI": -5.3,
    "Smoking": 18.4,
    ...
  }
}
```

This helps users understand *why* they received this particular score.

---

# 🗂️ **Best Practices**

-   Use explicit function names
    
-   Keep utilities separate in `/utils`
    
-   Keep components small and single-purpose
    
-   Write clear commit messages in English
    
-   Add comments only when necessary
    
-   Document intent in the README, not in the code
    

---

# ✔️ **Do’s and Don’ts**

### ✔️ Do

-   Use descriptive function and variable names
    
-   Keep the ML pipeline modular
    
-   Keep the repository clean and structured
    
-   Write consistent commit messages
    
-   Ensure reproducibility via `requirements.txt`
    

### ❌ Don’t

-   Push the ESS dataset
    
-   Add unnecessary comments
    
-   Overuse abbreviations
    
-   Mix model training code with API logic
    
-   Include local machine paths in code
    

---

# 🧩 **Project Status**

| Component | Status |
| --- | --- |
| Frontend | ✔️ Functional |
| Backend API | ✔️ Operational |
| Machine Learning Model | ✔️ Trained |
| BMI Integration | ✔️ Working |
| SHAP Explainability | ✔️ Fully integrated |
| Deployment | 🟡 Work In Progress |
| Documentation | 🟢 Improved / ongoing |