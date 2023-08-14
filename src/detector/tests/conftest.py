import os
import pickle

import numpy as np
import pytest

from tools.detector import Detector

import settings


@pytest.fixture
def tests_root() -> str:
    """Returns current working directory"""
    return os.path.dirname(__file__)


@pytest.fixture(scope="session")
def detectron_wrapper() -> Detector:
    """Returns configured Detector instance"""
    return Detector(
        threshold=settings.DETECTRON_THRESHOLD,
        device=settings.DETECTRON_DEVICE
    )


@pytest.fixture
def test_frame_path(tests_root) -> str:
    """Returns path to the valid test frame"""
    return os.path.join(tests_root, 'resources', 'frame.pkl')


@pytest.fixture
def test_frame_data(test_frame_path) -> np.ndarray:
    """Returns ready to use frame array"""
    with open(test_frame_path, 'rb') as frame_file:
        return pickle.load(frame_file)


@pytest.fixture
def valid_video(tests_root):
    """Returns path to the valid test video"""
    return os.path.join(tests_root, 'resources', 'video.mp4')


@pytest.fixture
def invalid_video(tests_root):
    """Returns path to some invalid file (not video)"""
    return os.path.join(tests_root, '__init__.py')
