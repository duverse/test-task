import os.path
import random

import pytest

from tools.frame_reader import VideoFrameReader, ReadVideoException


def test_raises_error_on_invalid_format(invalid_video):
    """Check VideoFrameReader raises error if format is invalid"""
    with pytest.raises(ReadVideoException):
        with VideoFrameReader(invalid_video) as _:
            pass


def test_reads_frames_from_video(valid_video):
    """
    Check that VideoFrameReader reads video frames without issues.
    """
    with VideoFrameReader(valid_video) as vfr:
        assert len(vfr.frame_files) > 0


def test_removes_temp_files_after_context_is_closed(valid_video):
    """
    Check that VideoFrameReader removes temp files after context is closed.
    """
    with VideoFrameReader(valid_video) as vfr:
        frames_to_check = random.choices(vfr.frame_files, k=10)

    for frame in frames_to_check:
        assert os.path.exists(frame) is False
