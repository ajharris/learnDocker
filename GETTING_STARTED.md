# 🚀 Getting Started with Docker Learning

Welcome to your Docker learning journey! This guide will help you get up and running quickly.

## 🔧 Prerequisites

1. **Install Docker Desktop**:
   - [Windows](https://docs.docker.com/desktop/windows/install/)
   - [macOS](https://docs.docker.com/desktop/mac/install/)  
   - [Linux](https://docs.docker.com/desktop/linux/install/)

2. **Verify Installation**:
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Test Docker**:
   ```bash
   docker run hello-world
   ```

## 📚 Learning Path

Follow these examples in order for the best learning experience:

### 🟢 Beginner Level
1. **[01-hello-world](examples/01-hello-world/)** - Your first container
2. **[02-basic-web-app](examples/02-basic-web-app/)** - Static website with Nginx
3. **[03-python-app](examples/03-python-app/)** - Python Flask application

### 🟡 Intermediate Level  
4. **[04-node-app](examples/04-node-app/)** - Node.js Express application
5. **[05-nginx](examples/05-nginx/)** - Advanced web server configuration
6. **[06-multi-container](examples/06-multi-container/)** - Full-stack application

### 🔴 Advanced Level
7. **[07-volumes](examples/07-volumes/)** - Data persistence
8. **[08-networking](examples/08-networking/)** - Container communication
9. **[09-best-practices](examples/09-best-practices/)** - Production-ready techniques

## ⚡ Quick Start

1. **Clone this repository**:
   ```bash
   git clone https://github.com/ajharris/learnDocker.git
   cd learnDocker
   ```

2. **Start with Hello World**:
   ```bash
   cd examples/01-hello-world
   docker build -t hello-docker .
   docker run hello-docker
   ```

3. **Try the web application**:
   ```bash
   cd ../02-basic-web-app
   docker build -t basic-web-app .
   docker run -d -p 8080:80 basic-web-app
   ```
   Visit: http://localhost:8080

4. **Explore multi-container app**:
   ```bash
   cd ../06-multi-container
   cp .env.example .env
   docker-compose up -d
   ```
   Visit: http://localhost

## 🎯 Learning Tips

- **Hands-on practice**: Run every example yourself
- **Read the READMEs**: Each example has detailed explanations
- **Experiment**: Modify the examples to see what happens
- **Check logs**: Use `docker logs <container>` for debugging
- **Clean up**: Remove containers/images when done to save space

## 🧹 Cleanup Commands

```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove everything (use with caution!)
docker system prune -a
```

## ❓ Need Help?

- Check the individual README files in each example
- Review Docker's [official documentation](https://docs.docker.com/)
- Look at the **09-best-practices** example for troubleshooting tips

## 🎉 Ready to Start?

Head over to **[examples/01-hello-world](examples/01-hello-world/)** and begin your Docker learning adventure!

Happy containerizing! 🐳