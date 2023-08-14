import os
import pytest


@pytest.fixture
def tests_root():
    """Returns current working directory"""
    return os.path.dirname(__file__)


