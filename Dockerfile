# Stage 1: Build the frontend (Vue.js)
FROM node:18 AS frontend

# Set the working directory for frontend
WORKDIR /app/frontend

# Copy package.json and package-lock.json (if exists) to ensure consistent installs
COPY ./frontend/package.json frontend/package-lock.json ./

# Install node dependencies (node_modules)
RUN npm install

# Copy the rest of the frontend files (including any local assets)
COPY ./frontend/ ./


# Build the Vue.js app
RUN npm run build

# Stage 2: Set up the backend (Flask)
FROM python:3.10 AS backend

# Set the working directory for backend
WORKDIR /app/backend

# Set environment variable to disable GPU
ENV CUDA_VISIBLE_DEVICES=-1  

# Copy backend files and install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt
RUN pip install gunicorn  
# Run model training before starting the app
COPY backend/train_model.py ./
COPY backend/brfss13.csv ./
RUN python train_model.py

# Copy the Flask app files
COPY backend/app.py ./

# Copy frontend build output to the backend (Flask will serve it as static files)
COPY --from=frontend /app/frontend/dist /app/backend/static

# Expose Flask port
EXPOSE 5000

# Start Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

