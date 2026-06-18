#!/bin/sh

python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='TwojeMocneHaslo123!'
    )
"

python manage.py collectstatic --no-input

python manage.py import_movies

exec gunicorn cinema_project.wsgi:application --bind 0.0.0.0:8000