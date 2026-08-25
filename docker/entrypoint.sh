#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
    sleep 1
done

echo "Database Ready"

mkdir -p logs staticfiles media

python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py seed_admin

exec "$@"