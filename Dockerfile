FROM --platform=linux/arm64 python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    curl \
    unzip \
    tesseract-ocr \
    poppler-utils \
    xvfb \
    xauth \
    fonts-liberation \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libgtk-3-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create assets directory if it doesn't exist
RUN mkdir -p assets

# Set ownership and permissions
RUN chown -R appuser:appuser /app
RUN chmod -R 755 /app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application with Xvfb
CMD ["sh", "-c", "xvfb-run -a python app.py"] 