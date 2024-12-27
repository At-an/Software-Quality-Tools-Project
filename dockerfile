# Use official Python 3.12.5 image as base
FROM python:3.12.5-slim

# Set working directory to /app
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Run command to start Flask application
CMD ["python", "app.py"]