#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

until python manage.py shell -c "
from django.db import connection
connection.ensure_connection()
" >/dev/null 2>&1
do
    echo "Database unavailable - sleeping..."
    sleep 1
done

echo "PostgreSQL is ready."