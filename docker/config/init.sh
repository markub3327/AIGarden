#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

#gunicorn --bind=0.0.0.0 --timeout 600 --chdir /code/python ai_garden.wsgi

cd /code/ai_garden

python3 manage.py runserver 0:8000

