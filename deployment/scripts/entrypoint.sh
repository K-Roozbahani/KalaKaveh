#!/bin/sh

set -e

echo "Starting Django container..."

# منتظر آماده شدن دیتابیس
/deployment/scripts/wait_for_db.sh

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django development server..."

exec "$@"