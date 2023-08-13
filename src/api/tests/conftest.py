import os
import pytest


@pytest.fixture
def tests_root():
    """Returns current working directory"""
    return os.path.dirname(__file__)


@pytest.fixture
def valid_video(tests_root):
    """Returns path to the valid test video"""
    return os.path.join(tests_root, 'resources', 'video.mp4')


@pytest.fixture
def invalid_video(tests_root):
    """Returns path to some invalid file (not video)"""
    return os.path.join(tests_root, '__init__.py')


