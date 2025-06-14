# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create uploads directory
RUN mkdir -p tmp/uploads

# Expose the Streamlit port
EXPOSE 8501

# Set the Streamlit entrypoint
CMD ["streamlit", "run", "newui.py", "--server.port=8501", "--server.address=0.0.0.0"]
