#!/bin/bash

echo "Building files..."

# Install pip
apt-get update
apt-get install -y python3-pip

# Install Django
pip3 install django

echo "Installing requirements..."
pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations

echo "Migrate..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Files built successfully!"

