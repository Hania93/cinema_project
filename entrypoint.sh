#!/bin/sh

python manage.py migrate

python manage.py shell -c "

python manage.py collectstatic --no-input

python manage.py import_movies

exec gunicorn cinema_project.wsgi:application --bind 0.0.0.0:8000