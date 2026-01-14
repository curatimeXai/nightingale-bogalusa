FROM python:3.10-slim

WORKDIR /app

# Set environment variable to disable GPU
ENV CUDA_VISIBLE_DEVICES=-1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 80

# Start FastAPI app using Uvicorn (pas Gunicorn!)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]