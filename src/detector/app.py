"""Detectron celery worker app"""
import logging
import pickle

from celery import Celery

import settings
from tools import detector


logger = logging.getLogger(__name__)

app = Celery('detectron', broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_RESULTS_BACKEND)

model = detector.Detector(
    threshold=settings.DETECTRON_THRESHOLD,
    device=settings.DETECTRON_DEVICE
)


@app.task()
def detect_objects(image_path: str) -> dict:
    """Objects detection task"""
    logger.info('Received new image to be processed: %s', image_path)
    with open(image_path, 'rb') as image_file:
        image_arr = pickle.load(image_file)
        logger.info('Loaded image data')

    prediction = model.detect(image_arr)
    logger.info('Prediction task finished. Result: %s', prediction)
    return prediction
