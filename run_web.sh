#!/bin/sh

python manage.py collectstatic --noinput&&python manage.py migrate&&/usr/local/bin/gunicorn telegram_users_add.wsgi:application --reload -w 2 -b :8000 --timeout 600
