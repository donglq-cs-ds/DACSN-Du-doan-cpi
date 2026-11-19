"""Naive: dự báo bằng giá trị quan sát cuối cùng."""
import numpy as np

from .base import Forecaster


class NaiveForecaster(Forecaster):
    def fit(self, y: np.ndarray) -> "NaiveForecaster":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        raise NotImplementedError
