import multiprocessing
import os

# Gunicorn configuration for Sayil

# Bind to 0.0.0.0:8000 by default (so Docker wrapper works out of the box)
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')

# Use 1 worker for SQLite/dev depending on resources, but in prod (PostgreSQL) we can spawn more.
# Using standard 2*cores + 1 formula if not explicitly via env
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv('GUNICORN_THREADS', 2))

# General performance settings
timeout = 120
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
