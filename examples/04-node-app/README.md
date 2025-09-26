# 04 - Node.js Express App

Learn how to containerize a Node.js web application using Express.

## 🎯 Learning Objectives

- Containerize a Node.js application
- Understand npm package management in Docker
- Learn about Node.js-specific optimizations
- Work with development vs production builds
- Handle file watching and hot reload

## 📝 What We'll Build

An Express.js web application that:
- Serves a REST API
- Includes static file serving
- Demonstrates environment-based configuration
- Shows Node.js best practices in Docker

## 🐳 Step-by-Step Guide

### Step 1: Examine the Application

Files in this directory:
- `app.js`: Express application
- `package.json`: Node.js dependencies and scripts
- `Dockerfile`: Production container
- `Dockerfile.dev`: Development container with hot reload
- `.dockerignore`: Files to exclude

### Step 2: Build and Run (Production)

```bash
# Build production image
docker build -t node-express-app .

# Run the container
docker run -d -p 3000:3000 --name express-app node-express-app
```

### Step 3: Test the Application

```bash
# Test the API
curl http://localhost:3000/
curl http://localhost:3000/api/users
curl http://localhost:3000/api/info
```

### Step 4: Development Mode with Hot Reload

```bash
# Build development image
docker build -f Dockerfile.dev -t node-express-app:dev .

# Run with volume mounting for live reload
docker run -d -p 3000:3000 -v $(pwd):/app -v /app/node_modules --name express-dev node-express-app:dev
```

## 🔍 Understanding the Production Dockerfile

```dockerfile
# Multi-stage build
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runtime
WORKDIR /app

# Copy dependencies from previous stage
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001
USER nodejs

EXPOSE 3000
CMD ["node", "app.js"]
```

## 🔍 Key Docker Concepts for Node.js

- **Multi-stage builds**: Separate dependency installation from runtime
- **Layer optimization**: `package*.json` copied first for better caching
- **Production dependencies**: `npm ci --only=production`
- **Security**: Non-root user execution
- **Volume mounting**: Development hot reload

## 🧪 Experiments to Try

1. **Production vs Development**:
   ```bash
   # Production build (optimized)
   docker build -t node-app:prod .
   
   # Development build (with dev tools)
   docker build -f Dockerfile.dev -t node-app:dev .
   ```

2. **Environment Variables**:
   ```bash
   docker run -p 3000:3000 -e NODE_ENV=production -e PORT=3000 node-express-app
   ```

3. **Live Development**:
   ```bash
   # Mount source code for live editing
   docker run -p 3000:3000 -v $(pwd):/app -v /app/node_modules node-express-app:dev
   ```

4. **Package Management**:
   ```bash
   # Install new packages
   docker exec -it express-app npm install lodash
   ```

## 🔧 Development Workflow

For active development, use the dev container:

```bash
# Start development container
docker-compose -f docker-compose.dev.yml up

# Or manually:
docker run -it -p 3000:3000 -v $(pwd):/app -v /app/node_modules node-express-app:dev
```

## 🐛 Debugging Tips

- **View logs**: `docker logs express-app`
- **Interactive shell**: `docker exec -it express-app sh`
- **Node.js debugging**: `docker run -p 3000:3000 -p 9229:9229 node-express-app node --inspect=0.0.0.0:9229 app.js`
- **Package audit**: `docker exec express-app npm audit`

## 🧹 Cleanup

```bash
# Stop and remove containers
docker stop express-app express-dev
docker rm express-app express-dev

# Remove images
docker rmi node-express-app node-express-app:dev
```

## ➡️ Next Steps

Ready to learn about web servers? Head to `05-nginx` to see advanced Nginx configurations and reverse proxy setups!