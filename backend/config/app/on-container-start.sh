python manage.py makemigrations
python manage.py migrate --run-syncdb

mkdir static && chmod 077 static
python manage.py collectstatic --noinput

gunicorn --reload emotions-and-me-backend.wsgi:application -b 0.0.0.0:8000