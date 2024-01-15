#!/bin/bash

# wait for db to start
echo "Wait for db to start..."
echo ====================================
sleep 5


echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
python manage.py runserver ${APP_HOST}:${APP_PORT}