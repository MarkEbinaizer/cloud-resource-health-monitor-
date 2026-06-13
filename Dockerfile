# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make the health_monitor.py executable
RUN chmod +x health_monitor.py

# Run the health monitor when the container launches
CMD ["python3", "health_monitor.py"]