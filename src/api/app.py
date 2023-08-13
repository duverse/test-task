"""Main Flask application"""
import os
import time
import string
import logging

import nanoid
from flask import Flask, render_template, request, jsonify

import settings
from tools import frame_reader, detectron_client


logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
def home():
    """Render a home page"""
    template_name = 'index.html'

    return render_template(
        template_name_or_list=template_name
    )


@app.route('/detector/', methods=['POST'])
def detector():
    """Detect cats and dogs API"""
    request_start = time.time()
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
    temp_video_path = f'{nanoid.generate(string.ascii_letters, size=12)}.mp4'
    uploaded_file.save(temp_video_path)

    # Read & Process frames
    with frame_reader.VideoFrameReader(temp_video_path) as video_frames_reader:
        logger.info('New objects detection task received.')
        logger.info('Video frames count: %d', len(video_frames_reader.frame_files))
        response = detectron_client.detect_batch(video_frames_reader.frame_files)

    # Remove temp video file
    os.remove(temp_video_path)

    return jsonify(
        time=time.time() - request_start,
        frames_count=len(response),
        objects=response,
    )


if __name__ == '__main__':
    app.run()
