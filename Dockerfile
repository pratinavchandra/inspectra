# Dockerfile
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY inspectra.py /app/

# Install necessary Python libraries
RUN pip install requests yara-python

# Default command
ENTRYPOINT ["python", "inspectra.py"]
