# 01 - Hello World Docker

Your first Docker container! This example demonstrates the absolute basics of Docker.

## 🎯 Learning Objectives

- Understand what a Docker image and container are
- Learn basic Docker commands
- Create your first Dockerfile
- Build and run your first container

## 📝 What We'll Build

A simple container that prints "Hello, Docker!" when run.

## 🐳 Step-by-Step Guide

### Step 1: Examine the Dockerfile

Look at the `Dockerfile` in this directory:

```dockerfile
# Use the official Alpine Linux image (very lightweight)
FROM alpine:latest

# Set the working directory inside the container
WORKDIR /app

# Copy our script into the container
COPY hello.sh /app/

# Make the script executable
RUN chmod +x hello.sh

# Set the default command to run when the container starts
CMD ["./hello.sh"]
```

### Step 2: Examine the Script

Look at `hello.sh`:

```bash
#!/bin/bash
echo "🐳 Hello, Docker!"
echo "Container is running successfully!"
echo "Current date: $(date)"
```

### Step 3: Build the Docker Image

```bash
# Build the image and tag it as "hello-docker"
docker build -t hello-docker .
```

### Step 4: Run the Container

```bash
# Run the container
docker run hello-docker
```

### Step 5: List Images and Containers

```bash
# List all Docker images
docker images

# List running containers
docker ps

# List all containers (including stopped ones)
docker ps -a
```

## 🔍 Understanding the Commands

- `FROM alpine:latest`: Uses Alpine Linux as the base image (only ~5MB!)
- `WORKDIR /app`: Sets the working directory inside the container
- `COPY hello.sh /app/`: Copies the script from your host to the container
- `RUN chmod +x hello.sh`: Executes a command during the build process
- `CMD ["./hello.sh"]`: Specifies what command runs when the container starts

## 🧪 Experiments to Try

1. **Modify the script**: Change the message in `hello.sh` and rebuild
2. **Interactive mode**: Run `docker run -it hello-docker sh` to explore inside the container
3. **Different base image**: Try changing `alpine:latest` to `ubuntu:latest`

## 🧹 Cleanup

Remove the container and image when done:

```bash
# Remove all stopped containers
docker container prune

# Remove the image
docker rmi hello-docker
```

## ➡️ Next Steps

Once you've mastered this example, move on to `02-basic-web-app` to learn about exposing ports and serving web content!