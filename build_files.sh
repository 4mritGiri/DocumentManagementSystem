#!/usr/bin/env bash

echo "Building files..."

# Install libzbar-devel using curl to download the RPM package and yum to install it
echo "Installing libzbar-devel..."
yum install -y curl
curl -O http://example.com/path/to/zbar-devel.rpm
yum install -y ./zbar-devel.rpm

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations --noinput

echo "Migrate..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Files built successfully!"
