FROM python:3.10-slim

WORKDIR /app

# Set environment variable to disable GPU
ENV CUDA_VISIBLE_DEVICES=-1

# Install debugging tools
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    wget \
    net-tools \
    procps \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 80

# Start Flask app using Gunicorn
CMD ["gunicorn", "api:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]
