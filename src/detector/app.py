"""Detectron celery worker app"""
import logging
import os
import pickle

from redis import Redis
from celery import Celery

import settings
from tools import detector, frame_reader, pipeline


logger = logging.getLogger(__name__)

# Initialize Celery APP
app = Celery('detectron', broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_RESULTS_BACKEND)

# Load detectron2 model wrapper
model = detector.Detector(
    threshold=settings.DETECTRON_THRESHOLD,
    device=settings.DETECTRON_DEVICE
)

# Initialize pipeline manager
pm = pipeline.PipelineManager(
    celery=app,
    redis=Redis.from_url(settings.PIPELINE_DB)
)


@app.task()
def init_pipeline(video_path: str) -> str:
    """Start video processing pipeline"""
    # Create new pipeline state
    logger.info('Creating new pipeline for video: %s', video_path)
    state = pm.create_state()

    # Schedule frames extraction task
    app.send_task('app.extract_frames', args=[
        state.id,
        video_path
    ])

    return state.id


@app.task()
def extract_frames(state_id: str, video_path: str):
    """Extract video frames and schedule objects detection"""
    # Get pipeline state
    state = pm.get_state(state_id)

    # Read video, extract frames and dump them into separate files
    logger.info('Extracting frames from video: %s', video_path)
    frames = frame_reader.VideoFrameReader(video_path=video_path).read()

    # Update state
    state.frames_count = len(frames)
    state.commit()

    # Schedule objects detection for each frame
    logger.info('Scheduling %d frames for object prediction', len(frames))
    for frame_id, frame_path in enumerate(frames):
        app.send_task('app.detect_objects', args=[
            state_id,
            frame_id,
            frame_path
        ])

    # Delete source video
    os.remove(video_path)


@app.task()
def detect_objects(state_id: str, frame_id: int, image_path: str):
    """Objects detection task"""
    # Get pipeline state
    state = pm.get_state(state_id)

    try:
        # Read image
        logger.info('Received new image #%d in pipe %s', frame_id, state_id)
        with open(image_path, 'rb') as image_file:
            image_arr = pickle.load(image_file)
            logger.info('Loaded image data')

        # Predict objects
        prediction = model.detect(image_arr)
        state.append_frame({'id': frame_id, 'objects': prediction, 'error': None})
        logger.info('Prediction task finished. Result: %s', prediction)

        # Delete image
        os.remove(image_path)
    except Exception as e:
        # Log error instead of frame detection result. This way, we can be
        # sure that the pipeline job is finished.
        state.append_frame({'id': frame_id, 'objects': None,
                            'error': f'{type(e).__name__}: {e}'})

        raise e
