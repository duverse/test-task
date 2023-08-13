"""Detector client library"""
import os
import pickle
import string
import typing
import logging

import cv2
import nanoid
import numpy as np


logger = logging.getLogger(__name__)


class ReadVideoException(Exception):
    """If video is not possible to read correctly"""


class VideoFrameReader:
    """
    Video frame reader context manager that helps to deal with
    batch of frames saved in temp dir.
    """
    # Frames temp directory
    temp_root = '/tmp'

    def __init__(self, video_path: str):
        self.video_path = video_path

        self._frames_files = []

    def __enter__(self) -> 'VideoFrameReader':
        """Read specified video, save frames and return itself"""
        for i, frame_arr in enumerate(self._read_video_frames(self.video_path)):
            frame_file_name = self._create_frame_name()
            with open(frame_file_name, 'wb') as frame_file:
                pickle.dump(frame_arr, frame_file)
                self._frames_files.append(frame_file_name)

                logger.debug('Saved frame #%d to %s', i, frame_file_name)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean temp files"""
        for frame_file in self._frames_files:
            os.remove(frame_file)

        self._frames_files = []

    @property
    def frame_files(self) -> typing.List[str]:
        """Returns a list of dumped frame files"""
        return self._frames_files

    def _create_frame_name(self) -> str:
        """Generates a random frame file name"""
        return os.path.join(self.temp_root, f'{nanoid.generate(string.ascii_letters, 12)}.pkl')

    @staticmethod
    def _read_video_frames(video_path) -> typing.Generator[np.ndarray, None, None]:
        """Video frames generator"""
        cap = cv2.VideoCapture(video_path)  # pylint: disable=E1101
        if not cap.isOpened():
            raise ReadVideoException('Failed to read video')

        while True:
            is_read, frame = cap.read()
            if is_read is False:
                break

            yield frame
