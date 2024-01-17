#!/bin/bash

# wait for db to start
echo "Wait for db to start..."
echo ====================================
sleep 5

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting tests..."
python manage.py test 
echo ====================================

echo "Creating Superuser..."
python manage.py createsuperuser --no-input 
echo ====================================

echo "Starting Server..."
python manage.py runserver ${APP_HOST}:${APP_PORT}