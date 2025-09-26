# 06 - Multi-Container Application

Learn how to orchestrate multiple containers using Docker Compose.

## 🎯 Learning Objectives

- Understand Docker Compose and multi-container applications
- Learn about service networking and communication
- Work with databases in containers
- Handle environment variables and secrets
- Understand volume management across services

## 📝 What We'll Build

A complete web application stack consisting of:
- **Frontend**: Nginx serving static files
- **Backend**: Node.js API server
- **Database**: PostgreSQL database
- **Cache**: Redis for session storage
- **Admin**: pgAdmin for database management

## 🐳 Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Nginx     │    │   Node.js   │    │ PostgreSQL  │
│   (Port     │────│   API       │────│  Database   │
│    80)      │    │  (Port      │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                   ┌─────────────┐
                   │    Redis    │
                   │    Cache    │
                   └─────────────┘
```

## 🚀 Quick Start

### Step 1: Launch the Stack

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 2: Access the Application

- **Frontend**: http://localhost:80
- **API**: http://localhost:3000
- **pgAdmin**: http://localhost:5050
  - Email: admin@example.com
  - Password: admin

### Step 3: Test the Services

```bash
# Test API endpoints
curl http://localhost:3000/api/health
curl http://localhost:3000/api/users

# Check service status
docker-compose ps
```

## 🔍 Understanding Docker Compose

### docker-compose.yml Structure

```yaml
version: '3.8'

services:
  # Web server
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - api

  # API server
  api:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis

  # Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  # Cache
  redis:
    image: redis:alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 🔍 Key Concepts

### Service Communication

- **Internal networking**: Services communicate using service names
- **Environment variables**: Configure service endpoints
- **Health checks**: Ensure services are ready

### Volume Management

- **Named volumes**: Persistent data storage
- **Bind mounts**: Development file sharing
- **Anonymous volumes**: Temporary storage

### Dependency Management

- **depends_on**: Start order (not readiness)
- **Health checks**: Wait for service readiness
- **Restart policies**: Handle service failures

## 🧪 Useful Commands

### Development Workflow

```bash
# Start services
docker-compose up -d

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f api

# Scale services
docker-compose up -d --scale api=3

# Restart service
docker-compose restart api

# Stop all services
docker-compose down
```

### Database Operations

```bash
# Execute SQL commands
docker-compose exec postgres psql -U user -d myapp

# Backup database
docker-compose exec postgres pg_dump -U user myapp > backup.sql

# Restore database
docker-compose exec -T postgres psql -U user myapp < backup.sql
```

### Monitoring and Debugging

```bash
# Check service status
docker-compose ps

# View resource usage
docker-compose top

# Access service shell
docker-compose exec api sh
docker-compose exec postgres bash

# View networks
docker network ls
docker network inspect <network_name>
```

## 🔧 Configuration Files

### Environment Variables

Create `.env` file:

```env
# Database
POSTGRES_DB=myapp
POSTGRES_USER=user
POSTGRES_PASSWORD=securepassword

# API
NODE_ENV=production
PORT=3000

# pgAdmin
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
```

### Development Override

Create `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  api:
    build:
      dockerfile: Dockerfile.dev
    volumes:
      - ./backend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    ports:
      - "9229:9229"  # Debug port
```

## 🐛 Troubleshooting

### Common Issues

1. **Service not starting**:
   ```bash
   docker-compose logs <service_name>
   ```

2. **Database connection failed**:
   ```bash
   docker-compose exec api ping postgres
   ```

3. **Port conflicts**:
   ```bash
   docker-compose ps
   netstat -tulpn | grep :80
   ```

4. **Volume issues**:
   ```bash
   docker volume ls
   docker volume inspect <volume_name>
   ```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove containers, volumes, and images
docker-compose down -v --rmi all
```

## ➡️ Next Steps

Ready to learn about data persistence? Head to `07-volumes` to master Docker volume management!