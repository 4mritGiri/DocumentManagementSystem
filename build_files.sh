#!/usr/bin/env bash

echo "Building files..."

# Manually install libzbar-devel
echo "Installing libzbar-devel..."
# Example commands, modify as per your specific version and source code location
wget https://github.com/mchehab/zbar/archive/master.zip
unzip master.zip
cd zbar-master
./configure
make
make install

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations --noinput

echo "Migrate..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Files built successfully!"
