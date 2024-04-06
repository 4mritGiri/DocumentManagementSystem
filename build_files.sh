#!/usr/bin/env bash

echo "Building files..."

# Manually install libzbar-devel using yum
echo "Installing libzbar-devel..."
sudo yum install -y zbar-devel

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations --noinput

echo "Migrate..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Files built successfully!"
