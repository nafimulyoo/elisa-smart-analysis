FROM python:3.9-slim

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


# Install system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV LLM_API_KEY=AIzaSyA-fdOs-FmQ9_r-VCS-n5HuTnr2yAWi-os
ENV EMB_API_KEY=AIzaSyA-fdOs-FmQ9_r-VCS-n5HuTnr2yAWi-os


# Expose port (informational only, actual port is managed by gluetun)
EXPOSE 8080

# Run the application
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]