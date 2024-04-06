#!/bin/bash

echo "Building files..."

echo "Installing requirements..."
pip3 install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations

echo "Migrate..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Files built successfully!"

