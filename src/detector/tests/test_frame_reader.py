import os.path
import random

import pytest

from tools.frame_reader import VideoFrameReader, ReadVideoException


def test_raises_error_on_invalid_format(invalid_video):
    """Check VideoFrameReader raises error if format is invalid"""
    with pytest.raises(ReadVideoException):
        VideoFrameReader(invalid_video).read()


def test_reads_frames_from_video(valid_video):
    """
    Check that VideoFrameReader reads video frames without issues.
    """
    frames = VideoFrameReader(valid_video).read()

    assert len(frames) > 0
