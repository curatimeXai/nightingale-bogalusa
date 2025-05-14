![alt text](frontend/src/assets/logoJGU.svg)

# Heart Disease Prediction

This project consists of two main components:

Backend (Flask API): It receives user input, processes it, and returns heart disease risk predictions using machine learning models (SVM, XGBoost, Keras).
Frontend (Vue.js): A user interface that allows users to input their health data and displays the risk predictions and charts.
<hr>

## Table of content

- [Heart Disease Prediction](#heart-disease-prediction)
  - [Table of content](#table-of-content)
  - [Tech Stack](#tech-stack)
      - [Frontend (Client-Side)](#frontend-client-side)
      - [Backend (Server-side)](#backend-server-side)
      - [Hosting \& Deployment](#hosting--deployment)
      - [Development Tools](#development-tools)
  - [Getting Started](#getting-started)
      - [Step 1: Set up Backend (Flask API)](#step-1-set-up-backend-flask-api)
      - [Step 2: Set up Frontend (Vue.js)](#step-2-set-up-frontend-vuejs)
      - [Deployment](#deployment)
  - [Training Model Overview](#training-model-overview)     
  - [Design section](#design-section)
    - [Color Palette](#color-palette)
  - [Functions](#functions)

<hr>

## Tech Stack

Before running the project, ensure you have the following installed:

Python 3.x (for the backend)
Node.js and npm (for the frontend)
Vue CLI (for frontend development)
Required Python libraries (for backend)

#### Frontend (Client-Side)

- HTML
- CSS
- JavaScript
- **Frameworks/Libraries:**
  - Express.js (Node.js)
  - Vue

#### Backend (Server-side)

- **Languages**: Node.js (JavaScript), Python 3.x
- **Frameworks:**: Flask

- **APIs:** REST, GraphQL


#### Hosting & Deployment

- **Platforms:** Google Cloud Run (temporary)

#### Development Tools

- **Version Control:** Git + GitHub
- **Package Managers:** npm, yarn
- **Linters/Formatters:**

## Getting Started

#### Step 1: Set up Backend (Flask API)

1. To begin, clone the repository to your local machine:

            git clone https://github.com/curatimeXai/XAI-heart-disease.git
    
2. Set up and run a virtual environment for Python (optional but recommended):
    
            python3 -m venv venv
            source venv/bin/activate
            # On Windows use `venv\Scripts\activate`

3. Navigate into the backend/ directory:

        cd .\backend\

4. Install the required Python packages:

        pip install -r requirements.txt


requirements.txt should include the following libraries:

pandas
scikit-learn
shap
joblib
numpy
Flask-CORS
scikit-learn
xgboost
keras
joblib
numpy
pandas
matplotlib
tensorflow
seaborn

5. Train AI model

        python train_model.py

6. Run Backend

        python app.py

#### Step 2: Set up Frontend (Vue.js)

1. Navigate to the frontend/ directory:
> **Note:** `cd ..` moves you up one directory level*
   
        cd frontend

2. Install the required dependencies:
   
        npm install

3. Run Frontend
   
        npm run serve


#### Deployment
For deployment we run a dockerfile where the docker image contains both backend and frontend.
Make sure you have Docker installed and run Docker Desktop if needed.

Build and run the Docker container with the following commands:
    
        docker build -t xai-heart-disease-app .
        docker run -p 5000:5000 xai-heart-disease-app

[Back to top](#table-of-content)

<hr>
## Training Model Overview
### Trained Models:
#### Support Vector Machine (SVM)
- A powerful classification model that finds the optimal hyperplane for separating classes.
- Trained with probability estimation enabled for confidence scoring.
#### XGBoost Classifier
- A gradient boosting model optimized for structured data.
- Uses log loss as the evaluation metric to improve classification accuracy.
#### Keras Deep Learning Model
- A neural network with two hidden layers:
   64 neurons (ReLU activation)
   32 neurons (ReLU activation)
- Final output layer uses sigmoid activation for binary classification (Heart Disease: Yes/No).
### Training Pipeline:
#### Step 1: Data Preprocessing
- Handling missing values
- Encoding categorical features
- Scaling numeric features
#### Step 2: Train-Test Split
- Splitting dataset into 80% training / 20% testing
#### Step 3: Model Training
- Each model is trained on scaled data
#### Step 4: Model Saving
- Trained models are saved for future use (.pkl for SVM/XGBoost, .h5 for Keras)
#### Step 5: Feature Importance Analysis
- SHAP values and feature importance are computed for XGBoost to improve model interpretability
[Back to top](#table-of-content)

<hr>
## Design section

We decided to follow the Nightingale projects theme usins red colors for alot of the backgrounds and text. Both green and red colors are used to clarify whether the results are positive or negative.

The fonts used are Montserrat for headings and Roboto for text.

### Color Palette


| Color | Colorcode    | Usage   | Location               |
| ----- | ------------ | ------- | ---------------------- |
| Red (variants)   | #c53030, #a02121, #dc3545, #f8d4d4, #FF0000, #ffa2a2 | Background, Text, Input | [HomePage.vue](./frontend/src/views/HomePage.vue) |
| Green (variants) | #008000, #d4f8d4, #4CAF50 | Background, Text | [HomePage.vue](./frontend/src/views/HomePage.vue) |
| Blue (variants) | #0d6efd, #bcdff1, #e7f3fe, #007bff | Risk summary background | [HomePage.vue](./frontend/src/views/HomePage.vue) |
| Grey (variants) | #333333, #414141, #515152 | Background, Placeholder | [HomePage.vue](./frontend/src/views/HomePage.vue) |

<hr>

## Functions

[Back to top](#table-of-content)
