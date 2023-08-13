"""Detectron client library"""
import logging
import typing

from celery import Celery

import settings


logger = logging.getLogger(__name__)

celery_app = Celery('detectron', broker=settings.CELERY_BROKER_URL,
                    backend=settings.CELERY_RESULTS_BACKEND)


def detect(image_array_path: str) -> dict:
    """Detects objects on the given image"""
    logger.info('Scheduling task to recognize objects on image')
    task = celery_app.send_task(
        name='app.detect_objects',
        args=[image_array_path],
    )

    return task.get()


def detect_batch(images_array_paths: typing.List[str]) -> typing.List[dict]:
    """Detect objects for each given frame"""
    logger.info('Scheduling task to recognize objects on %d images', len(images_array_paths))
    tasks = [celery_app.send_task(
        name='app.detect_objects',
        args=[image_path],
    ) for image_path in images_array_paths]

    return [task.get() for task in tasks]


__all__ = ['detect_batch', 'detect']
