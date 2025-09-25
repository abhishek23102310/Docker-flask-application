# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install Node.js (for frontend build)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy backend requirements and install
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt

# Copy backend and frontend source code
COPY backend /app/backend
COPY frontend /app/frontend

# Build frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Move frontend build to backend static folder
RUN rm -rf /app/backend/static
RUN mv /app/frontend/build /app/backend/static

# Set workdir to backend for running Flask app
WORKDIR /app/backend

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
