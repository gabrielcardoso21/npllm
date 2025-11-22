# Dockerfile for npllm
# Optimized for 4 vCPU + 8GB RAM

FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs models/cache models/embeddings_cache data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ENV=production

# Expose metrics port
EXPOSE 9090

# Run application
CMD ["python", "-m", "src.main", "--config", "config/production.yaml"]

