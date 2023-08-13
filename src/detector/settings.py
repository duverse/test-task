"""API Settings"""
import os

# Celery broker URL
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')

# Celery results backend
CELERY_RESULTS_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

# Detectron model device
DETECTRON_DEVICE = os.getenv('DETECTRON_DEVICE', 'cpu')

# Detectron model threshold
DETECTRON_THRESHOLD = float(os.getenv('DETECTRON_THRESHOLD', '0.5'))
