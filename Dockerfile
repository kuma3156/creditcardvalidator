# Use official Python 3.14 slim image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Buffer stdout/stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY ./app ./app

# Expose FastAPI port
EXPOSE 8000

# Command to run the app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
