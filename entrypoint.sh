#!/bin/sh

python manage.py migrate

python manage.py collectstatic --no-input

exec gunicorn cinema_project.wsgi:application --bind 0.0.0.0:8000