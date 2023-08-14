# Use the official image for Python 3.8
FROM python:3.8

# Install some opencv deps
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Set the working directory inside the container
WORKDIR /app

# Copy the local files to the working directory
COPY tools/ ./tools
COPY app.py ./app.py
COPY settings.py ./settings.py
COPY requirements.txt ./requirements.txt
COPY requirements.detectron.txt ./requirements.detectron.txt

# Install project dependencies
RUN pip install -r ./requirements.txt --no-cache-dir

# Install Detectron2 last to avoid dependencies undefined errors
RUN pip install -r ./requirements.detectron.txt --no-cache-dir

# Run celery worker with pool solo, as it works well with detectron
CMD ["celery", "-A", "app.app", "worker", "--pool", "solo", "--loglevel=info"]
