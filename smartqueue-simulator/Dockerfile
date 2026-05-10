# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the simulator script
COPY simulator.py .

# Command to run the simulator
CMD ["python", "simulator.py"]