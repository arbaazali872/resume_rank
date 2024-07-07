#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run Django migrations and collectstatic (optional for production)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
