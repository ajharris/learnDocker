# 09 - Docker Best Practices

Learn Docker security, optimization, and production-ready techniques.

## 🎯 Learning Objectives

- Understand Docker security best practices
- Learn image optimization techniques
- Master production deployment strategies  
- Implement proper logging and monitoring
- Handle secrets and configuration management

## 📋 Best Practices Overview

### 🔒 Security Best Practices

#### 1. Use Non-Root Users
```dockerfile
# Bad - Running as root
FROM node:18-alpine
COPY . /app
WORKDIR /app
CMD ["node", "app.js"]

# Good - Using non-root user
FROM node:18-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001 -G nodejs
WORKDIR /app
COPY --chown=nodeuser:nodejs . .
USER nodeuser
CMD ["node", "app.js"]
```

#### 2. Use Specific Image Tags
```dockerfile
# Bad - Using latest tag
FROM node:latest

# Good - Using specific version
FROM node:18.17.1-alpine3.18
```

#### 3. Scan Images for Vulnerabilities
```bash
# Using Docker Scout
docker scout cves <image-name>

# Using Trivy
trivy image <image-name>

# Using Snyk
snyk container test <image-name>
```

### 🚀 Performance Optimization

#### 1. Multi-Stage Builds
```dockerfile
# Stage 1: Build dependencies
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build application
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Runtime
FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package*.json ./
USER nodeuser
CMD ["node", "dist/app.js"]
```

#### 2. Layer Optimization
```dockerfile
# Bad - Creates unnecessary layers
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y nodejs
RUN apt-get clean

# Good - Minimizes layers
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y curl nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

#### 3. Use .dockerignore
```dockerignore
# Version control
.git/
.gitignore

# Dependencies
node_modules/
npm-debug.log*

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db

# Build artifacts
dist/
build/
*.log
```

### 🏗️ Production-Ready Configurations

#### 1. Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1
```

#### 2. Signal Handling
```dockerfile
# Install init system for proper signal handling
RUN apk add --no-cache dumb-init

# Use dumb-init as entrypoint
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "app.js"]
```

#### 3. Resource Limits
```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M
```

### 🔧 Configuration Management

#### 1. Environment Variables
```dockerfile
# Set default values
ENV NODE_ENV=production \
    PORT=3000 \
    LOG_LEVEL=info

# Use runtime configuration
CMD ["sh", "-c", "node --max-old-space-size=${MAX_MEMORY:-512} app.js"]
```

#### 2. Secrets Management
```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
```

### 📊 Logging and Monitoring

#### 1. Structured Logging
```javascript
// app.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

// Log structured data
logger.info('User created', { 
  userId: user.id, 
  email: user.email,
  timestamp: new Date().toISOString()
});
```

#### 2. Container Monitoring
```yaml
# docker-compose.yml with monitoring
services:
  app:
    image: myapp
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    labels:
      - "com.example.service=api"
      - "com.example.environment=production"
```

## 🔍 Security Checklist

- [ ] Use non-root users in containers
- [ ] Use specific image tags, not `latest`
- [ ] Regularly scan images for vulnerabilities
- [ ] Use minimal base images (Alpine, Distroless)
- [ ] Don't store secrets in images
- [ ] Use multi-stage builds to reduce attack surface
- [ ] Implement proper health checks
- [ ] Use read-only file systems where possible
- [ ] Limit container capabilities
- [ ] Use container image signing

## 🚀 Performance Checklist

- [ ] Use multi-stage builds
- [ ] Optimize Dockerfile layer caching
- [ ] Use .dockerignore to reduce build context
- [ ] Choose appropriate base images
- [ ] Implement proper resource limits
- [ ] Use init systems for signal handling
- [ ] Optimize application for containers
- [ ] Use volume caching for dependencies

## 📋 Production Checklist

- [ ] Implement comprehensive health checks
- [ ] Configure proper logging
- [ ] Set up monitoring and alerting
- [ ] Use secrets management
- [ ] Implement graceful shutdown
- [ ] Configure resource limits
- [ ] Use container orchestration (Kubernetes, Docker Swarm)
- [ ] Implement backup and disaster recovery
- [ ] Use CI/CD for automated deployments
- [ ] Regular security updates

## 🧪 Example: Optimized Dockerfile

```dockerfile
# Multi-stage build for a Node.js application
FROM node:18-alpine AS base
RUN apk add --no-cache dumb-init
WORKDIR /app
COPY package*.json ./

# Development stage
FROM base AS development
RUN npm ci
COPY . .
USER node
EXPOSE 3000
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "run", "dev"]

# Production dependencies
FROM base AS dependencies
RUN npm ci --only=production && npm cache clean --force

# Build stage
FROM base AS build
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Production stage
FROM node:18-alpine AS production
RUN apk add --no-cache dumb-init curl && \
    addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001 -G nodejs

WORKDIR /app
COPY --from=dependencies --chown=nodeuser:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=nodeuser:nodejs /app/dist ./dist
COPY --chown=nodeuser:nodejs package*.json ./

USER nodeuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/app.js"]
```

## 🎓 Congratulations!

You've completed the Docker learning journey! You now understand:

- ✅ Docker fundamentals and container concepts
- ✅ Writing efficient Dockerfiles
- ✅ Multi-container applications with Docker Compose
- ✅ Security and optimization best practices
- ✅ Production-ready deployments

## 🔗 Further Learning

- [Docker Official Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Container Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Docker Certified Associate](https://training.mirantis.com/dca-certification-exam/)

Keep practicing and building with Docker! 🐳