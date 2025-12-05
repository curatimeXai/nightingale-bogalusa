▶️ Run the API

Start the server with:

uvicorn api:app --reload


The API is now live on:

📌 http://127.0.0.1:8000

Interactive documentation (Swagger UI):

📌 http://127.0.0.1:8000/docs

🧪 Testing the API

You can test directly in the Swagger UI, or use cURL:

🔹 POST /predict

Request body:

{
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
  "Problems with accomodation: noise": "Not marked"
}

🔹 cURL example
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d @sample.json

📤 Example Response
{
  "risk": 0.0498,
  "risk_percent": "4.98%",
  "feature_impacts_percent": {
    "Gender": 2.20,
    "Age of respondent, calculated": 44.63,
    "Do sports or other physical activity, how many of last 7 days": 6.53,
    "How often eat fruit, excluding drinking juice": 0.65,
    "How often eat vegetables or salad, excluding potatoes": 0.25,
    "Cigarette smoking behaviour": 3.90,
    "How often drink alcohol": 5.31,
    "Height of respondent (cm)": 6.45,
    "Weight of respondent (kg)": 6.99,
    "Health problems, last 12 months: high blood pressure": 14.01,
    "Health problems, last 12 months: diabetes": 0.58,
    "Problems with accomodation: noise": 0.12
  }
}

🧠 How the Model Works
🟦 1. Preprocessing Pipeline

Before training, the API applies:

StandardScaler → numeric features

Binary mapping → gender & yes/no markers

OrdinalEncoder → fruit/vegetable frequency

OneHotEncoding → smoking & alcohol categories

This ensures that XGBoost receives clean, numeric, meaningful data.

🟥 2. XGBoost Classifier

The trained model uses:

400 boosted trees

Depth = 5

Learning rate = 0.05

Class imbalance correction (scale_pos_weight)

It predicts the probability that a person has suffered a heart or circulation problem.

🟨 3. SHAP Explainability

Explainability uses:

✔ PermutationExplainer → works on ANY model
✔ Inputs = numeric transformed features
✔ SHAP values are grouped back to your 12 original human features

This is what builds "feature_impacts_percent".