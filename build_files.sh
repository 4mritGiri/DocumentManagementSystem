# Build files.sh for vercel deployment
echo "Building files..."

echo "Installing requirements..."
pipenv install -r requirements.txt

echo "Make migrations..."
python3.11 manage.py makemigrations

echo "Migrate..."
python3.11 manage.py migrate

echo "Collecting static files..."
python3.11 manage.py collectstatic --noinput --clear

echo "Files built successfully!"

