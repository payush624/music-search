FROM python:3.11-slim

# this is creating a folder in virtual machine ig ?
WORKDIR /app

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src folder into the container
COPY src/ ./src/

# Stand INSIDE the src folder
WORKDIR /app/src

# If the compose command fails, this is the backup
CMD ["python", "app.py"]