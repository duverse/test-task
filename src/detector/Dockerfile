# Use the official image for Python 3.8
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the local files to the working directory
COPY app.py ./app.py
COPY settings.py ./settings.py
COPY detector.py ./detector.py
COPY requirements.txt ./requirements.txt
COPY requirements.detectron.txt ./requirements.detectron.txt

# Optionally, you might want to install any required packages
RUN pip install -r ./requirements.txt --no-cache-dir
RUN pip install -r ./requirements.detectron.txt --no-cache-dir

# Command to run your application
CMD ["celery", "-A", "app.app", "worker", "--concurrency=1", "--pool", "solo", "--loglevel=info"]
