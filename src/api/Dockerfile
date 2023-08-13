# Use the official image for Python 3.8
FROM python:3.8

# Install some opencv deps
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Set the working directory inside the container
WORKDIR /app

# Copy the local files to the working directory
COPY ./templates ./templates
COPY ./tools ./tools
COPY app.py ./app.py
COPY settings.py ./settings.py
COPY requirements.txt ./requirements.txt
COPY uwsgi.ini ./uwsgi.ini

# Optionally, you might want to install any required packages
RUN pip install -r ./requirements.txt --no-cache-dir

# Command to run your application
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
