# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Git and other system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the FastAPI app on port 8080 (Cloud Run's default)
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]