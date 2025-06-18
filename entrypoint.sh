#!/bin/sh

set -e 

#wait for postgres 
echo "Waiting for postgres to be ready..."

while ! nc -z postgres 5432; do 
  sleep 1
done

echo "Postgres is active"

python3 manage.py makemigrations 
python manage.py migrate 

exec "$@"
