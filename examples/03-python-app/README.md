# 03 - Python Flask App

Learn how to containerize a Python web application using Flask.

## 🎯 Learning Objectives

- Containerize a Python application
- Understand Python package management in Docker
- Learn about multi-stage builds and optimization
- Work with environment variables
- Handle application dependencies

## 📝 What We'll Build

A simple Flask web API that:
- Serves a JSON API
- Counts visits
- Shows environment information
- Demonstrates Python best practices in Docker

## 🐳 Step-by-Step Guide

### Step 1: Examine the Application

Look at the files in this directory:
- `app.py`: Flask application
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container instructions
- `.dockerignore`: Files to exclude from build context

### Step 2: Build the Docker Image

```bash
# Build the image
docker build -t python-flask-app .
```

### Step 3: Run the Container

```bash
# Run with environment variables
docker run -d -p 5000:5000 --name flask-app -e ENVIRONMENT=production python-flask-app
```

### Step 4: Test the Application

```bash
# Test the API endpoints
curl http://localhost:5000/
curl http://localhost:5000/api/info
curl http://localhost:5000/api/health
```

Or open your browser to `http://localhost:5000`

## 🔍 Understanding the Dockerfile

```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application
CMD ["python", "app.py"]
```

## 🔍 Key Docker Concepts

- **Layer Caching**: Requirements are copied first to leverage Docker layer caching
- **Environment Variables**: Using `-e` flag to pass configuration
- **Health Checks**: Container health monitoring
- **Security**: Running as non-root user
- **Multi-stage builds**: Optimizing final image size

## 🧪 Experiments to Try

1. **Environment Variables**:
   ```bash
   docker run -p 5000:5000 -e ENVIRONMENT=development -e DEBUG=true python-flask-app
   ```

2. **Volume Mounting** (for development):
   ```bash
   docker run -p 5000:5000 -v $(pwd):/app python-flask-app
   ```

3. **Interactive Debugging**:
   ```bash
   docker run -it python-flask-app sh
   ```

4. **Check Health**:
   ```bash
   docker inspect --format='{{.State.Health.Status}}' flask-app
   ```

## 🐛 Debugging Tips

- **View logs**: `docker logs flask-app`
- **Real-time logs**: `docker logs -f flask-app`
- **Execute commands**: `docker exec -it flask-app sh`
- **Environment variables**: `docker exec flask-app env`

## 🧹 Cleanup

```bash
# Stop and remove container
docker stop flask-app
docker rm flask-app

# Remove image
docker rmi python-flask-app
```

## ➡️ Next Steps

Ready to learn Node.js in containers? Head to `04-node-app` to see how JavaScript applications work in Docker!