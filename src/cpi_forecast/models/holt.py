"""(Mở rộng) Làm mịn mũ Holt (có xu hướng)."""
import numpy as np

from .base import Forecaster


class HoltForecaster(Forecaster):
    def fit(self, y: np.ndarray) -> "HoltForecaster":
        raise NotImplementedError

    def predict(self, h: int) -> np.ndarray:
        raise NotImplementedError
