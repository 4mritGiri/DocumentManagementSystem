#!/usr/bin/env bash

echo "Building files..."

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations

echo "Migrate..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Files built successfully!"

