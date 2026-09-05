#!/bin/sh

set -e

echo "Waiting for PostgreSQL (timeout: 60s)..."

TIMEOUT=60
ELAPSED=0
while ! nc -z db 5432 2>/dev/null; do
    sleep 1
    ELAPSED=$((ELAPSED + 1))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "ERROR: PostgreSQL not reachable after ${TIMEOUT}s. Exiting."
        exit 1
    fi
done

echo "Database Ready"

mkdir -p logs staticfiles media

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding admin..."
python manage.py seed_admin || true

echo "Seeding presentations..."
python manage.py seed_presentations || true

echo "Starting server..."
exec "$@"