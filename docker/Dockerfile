# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Copy the static file
COPY static/ /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose port for the Flask server
EXPOSE 5000

# Command to run the server and client
#CMD ["sh", "-c", "flask run --host=0.0.0.0 & python client.py"]
CMD ["sh", "-c", "flask run --host=0.0.0.0"]
