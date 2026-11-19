"""Trung bình trượt."""
import numpy as np

from .base import Forecaster


class MovingAverageForecaster(Forecaster):
    def fit(self, y: np.ndarray) -> "MovingAverageForecaster":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        raise NotImplementedError
