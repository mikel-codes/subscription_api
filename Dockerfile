# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /subscription_api

# Install system dependencies for SQLAlchemy and MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . .

# Environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Expose Flask port
EXPOSE 5000

# Run Flask in container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
