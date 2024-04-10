FROM python:3.11.6-alpine3.18

# Print the Docker is running
RUN echo "Docker is running..."

# Install necessary libraries including libzbar and libgl1-mesa-glx
RUN apk update && apk add --no-cache \
    mesa-gl \
    && rm -rf /var/cache/apk/*

# Manually install libzbar-dev
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    make \
    musl-dev \
    libffi-dev \
    zlib-dev \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxcb-dev \
    libxkb-dev \
    libxslt-dev \
    libxml2-dev \
    && apk add --no-cache libzbar-dev \
    && rm -rf /var/cache/apk/* \
    && apk del .build-deps


# Setting the environment variable
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Run the Django migrations and migrate the database
RUN python3 manage.py makemigrations && \
    python3 manage.py migrate

# Collect the static files
RUN python3 manage.py collectstatic --noinput

# Expose the port on which Django runs
EXPOSE 8000

# Run the Django server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# End of Dockerfile
RUN echo "Completed running the Dockerfile..."
