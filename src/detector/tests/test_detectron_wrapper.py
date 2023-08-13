import numpy as np

from tools.detector import Detector


def test_detectron_wrapper_detects_objects(test_frame_data: np.ndarray,
                                           detectron_wrapper: Detector):
    """Check that Detector correctly detects objects on image"""
    result = detectron_wrapper.detect(test_frame_data)

    assert len(result) == 1
    assert 'dog' in result
