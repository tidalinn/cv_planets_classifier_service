import logging
from typing import Dict, List

import cv2 as cv
import numpy as np
import onnxruntime

from src.configs import ProjectConfig

logger = logging.getLogger(__name__)


class Classificator:

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.session = onnxruntime.InferenceSession(
            self.config.classificator.path_model,
            providers=self.config.onnx.providers,
        )
        self.input_name = self.session.get_inputs()[0].name
        logger.info(self.input_name)
        self._get_model_input_output()

    @property
    def classes(self) -> list:
        return list(self.config.classificator.classes)

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        image = cv.resize(image, self.config.data.img_size)
        image = image / 255.0  # noqa: WPS432
        image = image.astype(np.float32)
        image = np.transpose(image, (2, 0, 1))
        return np.expand_dims(image, axis=0)

    def predict(self, image: np.ndarray) -> List[str]:
        image = self.preprocess(image)
        preds = self.session.run(None, {self.input_name: image})[0]
        preds = preds[0] > self.config.classificator.threshold
        return [tag for tag, prob in zip(self.classes, preds) if prob]

    def predict_proba(self, image: np.ndarray) -> Dict[str, float]:
        image = self.preprocess(image)
        preds = self.session.run(None, {self.input_name: image})[0]
        return {tag: f'{self._sigmoid(pred):.4f}' for tag, pred in zip(self.classes, preds[0])}

    def _get_model_input_output(self):
        for index, input in enumerate(self.session.get_inputs()):
            logger.info(f'Input {index} | name = {input.name} | shape = {input.shape} | type = {input.type}')

        for index, output in enumerate(self.session.get_outputs()):
            logger.info(f'Output {index} | name = {output.name} | shape = {output.shape} | type = {output.type}')

    def _sigmoid(self, preds: np.ndarray) -> float:
        return 1 / (1 + np.exp(-preds))
