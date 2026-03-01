#!/bin/sh
set -e

# Fix volume permissions for the static and media volumes created by docker
chown -R sayil:sayil /app/staticfiles /app/media

echo "Running migrations..."
gosu sayil python manage.py migrate --noinput

echo "Collecting static files..."
gosu sayil python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gosu sayil gunicorn --config gunicorn.conf.py sayil.wsgi:application