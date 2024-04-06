#!/usr/bin/env bash

echo "Building files..."

# Check if Python 3.11.6 is installed, if not, install it
if ! command -v python3.11.6 &>/dev/null; then
    echo "Installing Python 3.11.6..."
    # Replace the URL below with the appropriate Python 3.11.6 installation package URL
    curl -O https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz
    tar -xf Python-3.11.6.tgz
    cd Python-3.11.6 || exit
    ./configure
    make
    make install
    cd ..
    rm -rf Python-3.11.6*
else
    echo "Python 3.11.6 is already installed."
fi

# Check Python 3.11.6 version
echo "Checking Python 3.11.6 version..."
python3.11.6 --version

echo "Installing pip..."
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.11.6 get-pip.py

# Install libzbar-devel using curl to download the RPM package and yum to install it
echo "Installing libzbar-devel..."
yum install -y curl
curl -O http://example.com/path/to/zbar-devel.rpm
yum install -y ./zbar-devel.rpm

echo "Installing requirements..."
python3.11.6 -m pip install -r requirements.txt

echo "Make migrations..."
python3.11.6 manage.py makemigrations --noinput

echo "Migrate..."
python3.11.6 manage.py migrate --noinput

echo "Collecting static files..."
python3.11.6 manage.py collectstatic --noinput --clear

echo "Files built successfully!"
