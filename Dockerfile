# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Create a virtual environment
RUN python -m venv /opt/venv

# Copy requirements and install dependencies into the venv
COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy the entire virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Make sure we use the venv by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY app.py .
COPY templates/ ./templates/

# Create non-root user for security
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port 8000
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]