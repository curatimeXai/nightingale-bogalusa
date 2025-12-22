# Stage 1: Build the frontend (Vue.js)
FROM node:18 AS frontend

WORKDIR /app/frontend
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend/ ./
RUN npm run build


# Stage 2: Set up the backend (Flask)
FROM python:3.10 AS backend

WORKDIR /app/backend

ENV CUDA_VISIBLE_DEVICES=-1  

# Copy backend dependencies and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt
RUN pip install gunicorn  

# Copy backend source code
COPY backend/*.py ./
COPY backend/brfss13.csv ./
COPY backend/models ./models

COPY backend/common_preprocess.py ./

# Optionally retrain model if needed
# RUN python train_model.py

# Copy frontend build output to be served by Flask
COPY --from=frontend /app/frontend/dist ./static

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
