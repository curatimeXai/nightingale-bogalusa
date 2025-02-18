# Heart Disease Prediction 

This project consists of two main components:
- **Backend (Flask API)**: It receives user input, processes it, and returns heart disease risk predictions using machine learning models (SVM, XGBoost, Keras).
- **Frontend (Vue.js)**: A user interface that allows users to input their health data and displays the risk predictions and charts.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x** (for the backend)
- **Node.js and npm** (for the frontend)
- **Vue CLI** (for frontend development)
- **Required Python libraries** (for backend)

## Setup Instructions

### Step 1: Set Up the Backend (Flask API)

1. Clone the repository:

   ```bash
   git clone https://github.com/IvyAnalisa/XAI_heart_disease.git
   

2. Set up a virtual environment for Python (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # On Windows use `venv\Scripts\activate`
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   **requirements.txt** should include the following libraries:
   - Flask
   - Flask-CORS
   - scikit-learn
   - xgboost
   - keras
   - joblib
   - numpy
   - pandas
   - matplotlib

4. Place the trained models (`svm_model.pkl`, `xgb_model.pkl`, `keras_model.h5`, `scaler.pkl`) in the `models/` folder.
   
6. Run the Flask application:

   ```bash
   python app.py
   ```
run python train_model.py
   The Flask API will be running on `http://localhost:5000`.

### Step 2: Set Up the Frontend (Vue.js)

1. Navigate to the `frontend/` folder:

   ```bash
   cd frontend
   ```

2. Install the required dependencies:

   ```bash
   npm install
   ```
   npm install chart.js (for displaying chart on frontend)

3. Run the Vue.js development server:

   ```bash
   npm run serve
   ```

   The frontend will be available at `http://localhost:8080`.

### Step 3: Using the Application

1. Open your browser and go to `http://localhost:8080`.
2. Enter the required health data in the "Enter Measurements" section.
3. Submit the form, and the backend will predict the risk percentages for heart disease using the models (SVM, XGBoost, Keras).
4. The frontend will display:
   - Pie charts showing predictions for each model.
   - A text summary of the predicted risk percentages from each model.

### Step 4: Testing the API (Optional)

To test the backend independently, you can use any API testing tool like Postman, or use `curl`:

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{
  "Gender": "Male",
  "AgeCategory": "40-44",
  "Weight": 70,
  "Height": 175,
  "Smoking": "Sometimes",
  "Alcohol": 2,
  "Sleep": 8,
  "Exercise": 150,
  "Fruit": 2,
  "Diabetes": false,
  "Kidney": false,
  "Stroke": false
}'
```

This will return the risk predictions and the corresponding pie chart images.


Added original frontend folder as frontend_copy. To run locate to folder:
```bash
cd frontend_copy

npm install

// npm audit fix , if necessary

npm run dev
```

