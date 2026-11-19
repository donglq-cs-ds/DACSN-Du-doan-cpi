"""(Mở rộng) Làm mịn mũ đơn."""
import numpy as np

from .base import Forecaster


class SimpleExpSmoothing(Forecaster):
    def fit(self, y: np.ndarray) -> "SimpleExpSmoothing":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        raise NotImplementedError
