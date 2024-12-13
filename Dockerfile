# Use the official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV JWT_SECRET_KEY="your_super_secret_key"
ENV JWT_ALGORITHM="HS256"
#ENV RATE_LIMIT_REDIS_URL="redis://redis:6379/0"  # Use Docker Compose Redis service

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libglib2.0-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the FastAPI application
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "dicom_converter_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
