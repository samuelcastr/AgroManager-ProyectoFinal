web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT -w 4 --timeout 120 --access-logfile -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
