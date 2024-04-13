# Use the official Python Alpine image as the base image
FROM python:3.11.6-alpine3.18

# Set environment variables to ensure Python runs in unbuffered mode and doesn't write bytecode
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /code

# Install necessary system dependencies
RUN apk add --no-cache \
    build-base \
    python3 \
    py3-pip \
    openssl-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    libpng-dev \
    libffi-dev \
    zbar-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Run Django migrations and collect static files
RUN python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python3 manage.py collectstatic --noinput

# Expose the port on which Django runs
EXPOSE 8000

# Command to start the Django server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
