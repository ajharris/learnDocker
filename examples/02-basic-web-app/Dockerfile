# Use the official Nginx image based on Alpine Linux
FROM nginx:alpine

# Copy our static files to the Nginx html directory
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Nginx runs automatically when the container starts