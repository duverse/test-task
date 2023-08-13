"""Detector client library"""
import logging

import numpy as np
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor


logger = logging.getLogger(__name__)


class Detector:  # pylit: disable=R0903
    """Detectron2 helper that predicts objects on the given image"""
    def __init__(self, threshold: float = 0.5, device: str = "cpu"):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(
            model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))

        self.cfg.MODEL.DEVICE = device
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
            "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

        logger.info('Initializing Detectron2 with THRESHOLD=%d, DEVICE=%s', threshold, device)
        self.model = DefaultPredictor(self.cfg)

    def detect(self, image: np.ndarray) -> dict:
        """Returns dict with detected objects on the image"""
        logger.info('Predicting objects...')
        outputs = self.model(image)
        decoded = self._decode_prediction(outputs)

        return decoded

    def _decode_prediction(self, outputs):
        """Decode model prediction classes names"""
        logger.info('Decoding model output...')
        instances = outputs["instances"]
        model_metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])
        prediction = {}
        for i in range(len(instances)):
            class_id = instances.pred_classes[i].item()
            class_name = model_metadata.thing_classes[class_id]
            confidence_score = instances.scores[i].item()
            prediction[class_name] = confidence_score
        logger.info('Got output: %s', str(prediction))
        return prediction
