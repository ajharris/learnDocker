# 02 - Basic Web App

Learn how to serve a static website using Docker and Nginx.

## 🎯 Learning Objectives

- Serve static content with Docker
- Understand port mapping
- Use Nginx as a web server
- Learn about container networking

## 📝 What We'll Build

A simple HTML website served by Nginx running in a Docker container.

## 🐳 Step-by-Step Guide

### Step 1: Examine the Files

This example includes:
- `Dockerfile`: Instructions to build our web server
- `index.html`: A simple HTML page
- `style.css`: Basic styling
- `nginx.conf`: Nginx configuration

### Step 2: Build the Docker Image

```bash
# Build the image
docker build -t basic-web-app .
```

### Step 3: Run the Container

```bash
# Run the container and map port 80 inside container to port 8080 on host
docker run -d -p 8080:80 --name my-web-app basic-web-app
```

### Step 4: View Your Website

Open your browser and go to: `http://localhost:8080`

You should see a colorful "Welcome to Docker!" page.

### Step 5: Check Container Status

```bash
# See running containers
docker ps

# View container logs
docker logs my-web-app

# Execute commands inside the running container
docker exec -it my-web-app sh
```

## 🔍 Understanding the Dockerfile

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

- `FROM nginx:alpine`: Uses the lightweight Nginx Alpine image
- `COPY`: Copies our files into the container
- `EXPOSE 80`: Documents that the container uses port 80
- Nginx automatically serves files from `/usr/share/nginx/html/`

## 🔍 Understanding Port Mapping

`-p 8080:80` means:
- `8080`: Port on your host machine
- `80`: Port inside the container
- Traffic to `localhost:8080` gets forwarded to port `80` inside the container

## 🧪 Experiments to Try

1. **Change the content**: Modify `index.html`, rebuild, and run again
2. **Different port**: Try `-p 3000:80` and access `localhost:3000`
3. **Multiple containers**: Run multiple instances on different ports
4. **Live editing**: Use volume mounting to edit files without rebuilding

### Volume Mounting Example
```bash
# Mount current directory to serve files directly (for development)
docker run -d -p 8080:80 -v $(pwd):/usr/share/nginx/html nginx:alpine
```

## 🧹 Cleanup

```bash
# Stop and remove the container
docker stop my-web-app
docker rm my-web-app

# Remove the image
docker rmi basic-web-app
```

## ➡️ Next Steps

Ready for something more dynamic? Move on to `03-python-app` to learn about running Python applications in containers!