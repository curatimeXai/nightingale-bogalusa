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
##### Training and Parameters:
- Kernel: RBF (Radial Basis Function) was chosen because preliminary tests showed that the data was not linearly separable.
- C (Regularization parameter): Set to 1.0 to balance between bias and variance.
- Gamma: Set to 'scale', which means the value is adjusted based on the standard deviation of the variables.
- Scaler: StandardScaler was used before training to ensure the SVM performs optimally
SVM maps the input data into a higher-dimensional space and finds a hyperplane that maximizes the margin between the two classes (presence or absence of heart disease). The model is trained to predict class labels, and the setting probability=True allows it to estimate class probabilities, which contributes to the final outcome.  
#### XGBoost Classifier
- A gradient boosting model optimized for structured data.
- Uses log loss as the evaluation metric to improve classification accuracy.
##### Training and Parameters:
- n_estimators: 100 – the number of trees built in the model.
- max_depth: 4 – limited the depth of the trees to reduce the risk of overfitting.
- learning_rate: 0.1 – to make the training more stable.
- subsample: 0.8 – to prevent overfitting by training on only a subset of the data.
- random_state: 42 – used to ensure the results can be reproduced.
XGBoost uses an ensemble method where each tree improves the predictions made by the previous one. The model assigns importance scores to features, helping us understand how each feature contributes to decision-making. In this app, XGBoost predicts the probability of heart disease based on patterns learned during training.

#### Keras Deep Learning Model
##### Model Architecture:
- Input Layer: Number of nodes corresponds to the number of features (approximately 12)
- Hidden Layers: Two layers with 32 and 16 neurons respectively, using ReLU activation function
- Dropout: 0.2 after each layer to reduce overfitting
- Output Layer: 1 neuron with sigmoid activation (since this is binary classification)
##### Training and Parameters:
- Loss function: binary_crossentropy
- Optimizer: Adam with a learning rate of 0.001
- Epochs: 50
- Batch size: 32
The layers of the neural network consist of fully connected neurons that process the input through activation functions. The model is trained using the Adam optimizer and binary cross-entropy loss to minimize the error between predicted and actual labels. The final output layer uses a sigmoid activation to produce a probability between 0 and 1, representing the likelihood of heart disease.
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
### SHAP Integration
#### How SHAP Was Implemented
**a) Creating the SHAP explainer:**
- For the **XGBoost model** ,'shap.TreeExplainer'  was used to leverage the efficiency and accuracy of tree-based models.
- For the **neural network model (Keras)**, 'shap.Explainer' was used in combination with keras.models.load_model to generate SHAP values based on the model's structure and weights.
  
**b) Generating SHAP values:**
- When a user submits data to /predict, the input is converted into a DataFrame and normalized.
- SHAP values are then calculated for that specific observation — meaning the model explains how much each individual factor influenced the result, either positively or negatively.
  
**c) Visualization of SHAP Results:**
- Two types of charts are generated to illustrate the impact:
  + A bar chart showing SHAP values for the most influential features.
  + A pie chart illustrating the proportion of influence from different features.
- These charts are generated in the backend using matplotlib and shap.plots, saved as PNGs in memory, converted to Base64 strings, and sent to the frontend as part of the JSON response.
  
 **d) Text-Based Summary:**
SHAP values are also used to generate a textual explanation that summarizes which factors had the greatest impact on the decision.

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
