# Use a Python base image
FROM python:3-alpine

# Install any required dependencies (if any)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy your Python application into the container
COPY . /app/

# Specify the command to run your Python application
CMD ["python", "lidgrosyncer.py"]
