FROM --platform=linux/arm64 python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DEBIAN_FRONTEND=noninteractive
# Configure Chrome
ENV CHROME_VERSION=114.0.5735.90
ENV CHROME_BIN=/usr/bin/chromium 
ENV CHROME_PATH=/usr/lib/chromium/

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
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify installations
RUN which chromium && \
    which chromedriver && \
    chromium --version && \
    chromedriver --version

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

# Create a debug script
RUN echo '#!/bin/bash\n\
echo "Testing ChromeDriver setup..."\n\
which chromedriver\n\
chromedriver --version\n\
ls -la /usr/bin/chromedriver\n\
echo "Testing Chromium setup..."\n\
which chromium\n\
chromium --version\n\
echo "Environment:"\n\
printenv | grep CHROME\n\
' > /app/debug_chrome.sh && chmod +x /app/debug_chrome.sh

# Set ownership and permissions
RUN chown -R appuser:appuser /app
RUN chmod -R 755 /app
RUN chmod 755 /usr/bin/chromedriver || true

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application with Xvfb
CMD ["sh", "-c", "xvfb-run -a python app.py"] 