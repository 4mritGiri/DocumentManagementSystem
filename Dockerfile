FROM python:3.11

# Print the Docker is running
RUN echo "Docker is running..."

# Install necessary libraries including libzbar and libgl1-mesa-glx
RUN apt-get update && apt-get install -y \
    libzbar-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Expose the port on which Django runs
EXPOSE 8000

RUN echo "Python is installed..."
# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
