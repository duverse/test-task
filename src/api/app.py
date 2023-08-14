"""Main Flask application"""
import string
import logging

import nanoid
from celery import Celery
from flask import Flask, render_template, request, jsonify
from redis.client import Redis

import settings
from tools.task import TaskManager, UndefinedTaskID


logger = logging.getLogger(__name__)

# Initialize flask application
app = Flask(__name__, template_folder='templates')

# Initialize celery application
celery = Celery('detectron', broker=settings.CELERY_BROKER_URL,
                backend=settings.CELERY_RESULTS_BACKEND)

# Initialize task manager
task_manager = TaskManager(celery, Redis.from_url(settings.PIPELINE_DB))


@app.route('/', methods=['GET'])
def home():
    """Render a home page"""
    template_name = 'index.html'

    return render_template(
        template_name_or_list=template_name
    )


@app.route('/detector/', methods=['POST'])
def detector():
    """Schedule a task to detect objects on video"""
    uploaded_file = request.files.get('video')

    # Validate file format
    if not uploaded_file or not uploaded_file.filename.lower().endswith('.mp4'):
        return jsonify(
            error=100,
            message="Invalid file format. Supported format: mp4"
        ), 400

    # Validate file size
    if uploaded_file.content_length > settings.MAX_UPLOADED_FILE_SIZE * pow(10, 6):
        return jsonify(
            error=101,
            message=f"Too large file size. Maximum: {settings.MAX_UPLOADED_FILE_SIZE}MB"
        ), 400

    # Save uploaded file
    temp_video_path = f'/tmp/{nanoid.generate(string.ascii_letters, size=12)}.mp4'
    uploaded_file.save(temp_video_path)

    # Schedule video processing
    task_state = task_manager.create_task(video_path=temp_video_path)

    return jsonify(
        task_id=task_state.id,
    )


@app.route('/detector/<string:task_id>', methods=['GET'])
def detector_result(task_id: str):
    """Retrieve task state"""
    try:
        task = task_manager.get_task(task_id)
    except UndefinedTaskID:
        return jsonify(
            error=102,
            message=f"Task with ID \"{task_id}\" is not defined"
        ), 400

    # Build a response
    response = task.to_dict()
    response['frames_processed'] = task.processed_frames_count()
    response['frames'] = list(sorted(task.list_frames(), key=lambda x: x['id']))

    return jsonify(response)


if __name__ == '__main__':
    app.run()
