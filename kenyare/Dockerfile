# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory for nested structure
WORKDIR /app/kenyare

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=server.py \
    FLASK_PORT=5000 \
    FLASK_ENV=production \
    APP_VERSION=1.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better cache usage
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir requests healthcheck

# Create necessary directories
RUN mkdir -p /app/kenyare/logs /app/kenyare/static/outputs

# Create a non-root user and set permissions
RUN useradd -m backendserviceacc && \
    chown -R backendserviceacc:backendserviceacc /app

# Copy the application code
COPY . .

# Set final permissions
RUN chown -R backendserviceacc:backendserviceacc /app

# Switch to non-root user
USER backendserviceacc

# Configure logging
ENV LOG_PATH=/app/kenyare/logs/app.log

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application with logging
CMD ["sh", "-c", "python -u server.py > /app/kenyare/logs/app.log 2>&1"]
