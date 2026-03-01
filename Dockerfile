# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies for psycopg2 and building wheels
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip and build wheels
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final production image
FROM python:3.12-slim

# Create a non-root user
RUN groupadd -r sayil && useradd -r -g sayil sayil

WORKDIR /app

# Runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --find-links=/wheels -r requirements.txt && rm -rf /wheels

# Copy application code
COPY . .

# Create static/media directories
RUN mkdir -p /app/staticfiles /app/media && chown -R sayil:sayil /app


# Copy entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user (done in entrypoint.sh instead to fix volume permissions)

# Expose port
EXPOSE 8000

# Use entrypoint script to handle migrations & start Gunicorn
ENTRYPOINT ["/entrypoint.sh"]