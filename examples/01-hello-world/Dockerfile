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