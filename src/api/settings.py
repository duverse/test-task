"""API Settings"""
import os

# Maximum uploaded file size (MB)
MAX_UPLOADED_FILE_SIZE = 10

# Celery broker URL
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')

# Celery results backend
CELERY_RESULTS_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

# Pipeline db for tasks states
PIPELINE_DB = os.getenv('PIPELINE_DB')
