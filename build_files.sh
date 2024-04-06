#!/usr/bin/env bash

echo "Building files..."

echo "Installing pip..."
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Install libzbar-devel using curl to download the RPM package and yum to install it
echo "Installing libzbar-devel..."
yum install -y curl
curl -O https://rpmfind.net/linux/fedora/linux/development/rawhide/Everything/x86_64/os/Packages/z/zbar-devel-0.23.93-2.fc40.x86_64.rpm
yum install -y ./zbar-devel-0.23.93-2.fc40.x86_64

# check python3 version
echo "Checking python3 version..."
python3 --version

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations --noinput

echo "Migrate..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Files built successfully!"
