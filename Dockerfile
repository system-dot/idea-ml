# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies required for packages like moviepy, Pillow
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code into the container
COPY . .

# Expose Flask port
EXPOSE 5000

# Command to run your app (or switch to gunicorn for production)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
