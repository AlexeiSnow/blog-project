#!/bin/sh
set -e

echo "Applying migrations..."
python manage.py migrate --no-input

echo "Loading initial data..."
python manage.py loaddata initial_data.json || echo "Skipping fixture load"

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
