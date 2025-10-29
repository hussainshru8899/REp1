# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ghostscript \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libxml2-dev libxslt1-dev \
    libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy app
COPY . /app

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
